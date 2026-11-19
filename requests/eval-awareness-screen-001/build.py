"""Expand prompts.yaml into prompts.jsonl with Marin token positions (same row format as probes/capybara-v1).

pairs: every body x every framing; text = framing + "\n" + body. word_pos = the body's tokens, so the paired
contrast compares identical tokens that differ only in what came before them. Stops if a body does not
tokenize identically after every framing.
near_miss / unrelated: free text, [[ ]] marks the scored span (none = last token only).

Tokenizer: Marin's tokenizer.json from the HF cache, or set TOK=/path/to/tokenizer.json.
Run: python -I build.py [prompts.yaml] [out.jsonl]
"""
import glob, json, os, re, sys
import yaml
from tokenizers import Tokenizer

TOK = os.environ.get("TOK") or next(iter(glob.glob(os.path.expanduser(
    "~/.cache/huggingface/hub/models--marin-community--marin-32b-base/snapshots/*/tokenizer.json"))), None)
BOS = "<|begin_of_text|>"
MARK = re.compile(r"\[\[(.+?)\]\]")


def spans_of(raw):
    out, spans, i = [], [], 0
    for m in MARK.finditer(raw):
        out.append(raw[i:m.start()]); start = sum(map(len, out))
        out.append(m.group(1)); spans.append((start, start + len(m.group(1)))); i = m.end()
    out.append(raw[i:])
    return "".join(out), spans


def row(tok, bos, rid, set_, text, spans, **extra):
    enc = tok.encode(text, add_special_tokens=False)
    ids = ([bos] if bos is not None else []) + enc.ids
    off = len(ids) - len(enc.ids)
    word = []
    for a, b in spans:
        hit = [k + off for k, (s, e) in enumerate(enc.offsets) if s < b and e > a]
        if not hit:
            sys.exit(f"{rid}: span {text[a:b]!r} matched no token")
        word += hit
    last = len(ids) - 1
    nxt = (max(word) + 1) if word and max(word) < last else None
    return dict(id=rid, set=set_, **extra, text=text, ids=ids, tokens=[BOS] * off + enc.tokens,
                word_pos=word, next_pos=nxt, last_pos=last)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "prompts.yaml"
    dst = sys.argv[2] if len(sys.argv) > 2 else "prompts.jsonl"
    cfg = yaml.safe_load(open(src, encoding="utf-8"))
    if not TOK:
        sys.exit("Marin tokenizer.json not found in the HF cache; set TOK=/path/to/tokenizer.json")
    tok = Tokenizer.from_file(TOK)
    bos = tok.token_to_id(BOS)
    rows = []
    for q, body in enumerate(cfg["bodies"]):
        body_ids = set()
        for name, f in cfg["framings"].items():
            text = f["text"] + "\n" + body
            r = row(tok, bos, f"q{q:02d}-{name}", "pairs", text, [(len(text) - len(body), len(text))],
                    framing=name, kind=f["kind"], twin=f.get("twin"), body=q)
            body_ids.add(tuple(r["ids"][i] for i in r["word_pos"]))
            rows.append(r)
        if len(body_ids) != 1:  # the whole design rests on this
            sys.exit(f"body {q} tokenizes differently after different framings: {body!r}")
    for name, f in cfg["framings"].items():  # a twin must match its test opening's length, so position cancels
        if f.get("twin"):
            a = tok.encode(f["text"] + "\n", add_special_tokens=False).ids
            b2 = tok.encode(cfg["framings"][f["twin"]]["text"] + "\n", add_special_tokens=False).ids
            if len(a) != len(b2):
                sys.exit(f"{name} and its twin {f['twin']} differ in length: {len(a)} vs {len(b2)} tokens")
    for set_ in ("near_miss", "unrelated"):
        for k, raw in enumerate(cfg.get(set_, [])):
            text, spans = spans_of(raw)
            rows.append(row(tok, bos, f"{set_}{k:02d}", set_, text, spans))
    with open(dst, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    by = {}
    for r in rows:
        by[r["set"]] = by.get(r["set"], 0) + 1
    print(len(rows), "prompts", by, "max len", max(len(r["ids"]) for r in rows),
          "tokens total", sum(len(r["ids"]) for r in rows))


if __name__ == "__main__":
    main()
