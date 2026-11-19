"""Held-out check for eval-awareness candidate neurons on Needham et al. 2025 (jjpn2/eval_awareness, gated).

prep:  dataset.json (decrypted) -> transcripts.jsonl, one plain-text transcript per line, truncated for capture.
score: transcripts.jsonl + per-transcript activations -> per-neuron-side AUROC (eval vs real), Spearman with the
       annotators' eval probability, AUROC on single-turn transcripts only, and Spearman with length (a neuron that only tracks length is not eval awareness).

  python eval_transcripts.py prep  dataset.json transcripts.jsonl [--agentic] [--max-tokens 1024]
  python eval_transcripts.py score transcripts.jsonl activations.csv scores.csv

activations.csv: column `id`, then one column per neuron side (e.g. `L42-N5277+`), one row per transcript,
value = that side's mean activation over the transcript's tokens (or max; state which).
Transcripts are licensed CC-BY-NC-SA and GAIA items must stay in a gated repo: share scores, never the text.
"""
import argparse, glob, json, os, sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score


def text_of(content):
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") for p in content if isinstance(p, dict))


def render(messages):
    # ponytail: plain "Role: text" turns; Marin is a base model, so no chat template exists to match
    return "\n\n".join(f"{m['role'].capitalize()}: {text_of(m.get('content', ''))}" for m in messages)


def human_prob(s):
    md = s.get("metadata", {})
    vals = [v for k in ("eval_author1", "eval_author2") for v in (md.get(k), s.get(k)) if v is not None]
    return float(np.mean(vals)) if vals else None


def prep(a):
    tok_file = os.environ.get("TOK") or next(iter(glob.glob(os.path.expanduser(
        "~/.cache/huggingface/hub/models--marin-community--marin-32b-base/snapshots/*/tokenizer.json"))), None)
    if not tok_file:
        sys.exit("Marin tokenizer.json not found in the HF cache; set TOK=/path/to/tokenizer.json")
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(tok_file)
    samples = json.load(open(a.dataset, encoding="utf8"))
    n = 0
    with open(a.out, "w", encoding="utf8") as f:
        for s in samples:
            md = s["metadata"]
            if (md.get("scaffold") is not None) != a.agentic:
                continue
            text = render(s["input"])
            enc = tok.encode(text, add_special_tokens=False)
            full = len(enc.ids)
            if full > a.max_tokens:
                text = text[: enc.offsets[a.max_tokens - 1][1]]
            f.write(json.dumps(dict(id=s["id"], is_eval=bool(md["eval_category"]), eval_type=md.get("eval_type"),
                                    category=md.get("category"), human_prob=human_prob(s),
                                    n_tokens=min(full, a.max_tokens), full_tokens=full,
                                    assistant_turns=sum(m["role"] == "assistant" for m in s["input"]),
                                    text=text)) + "\n")
            n += 1
    print(f"{n} transcripts -> {a.out}")


def auc(y, x):
    return roc_auc_score(y, x) if y.nunique() == 2 else None


def score(a):
    meta = pd.read_json(a.transcripts, lines=True).drop(columns="text")
    df = meta.merge(pd.read_csv(a.activations), on="id", validate="1:1")
    if len(df) != len(meta):
        sys.exit(f"{len(meta) - len(df)} transcripts have no activations")
    y = df["is_eval"].astype(int)
    if y.nunique() < 2:
        sys.exit("need both eval and real transcripts")
    sides = [c for c in pd.read_csv(a.activations, nrows=0).columns if c != "id"]
    hp = df["human_prob"].notna()
    st = df["assistant_turns"] == 0  # real chats are far more often multi-turn: score single-turn ones separately
    rows = [dict(side="(length only)", auroc=roc_auc_score(y, df["n_tokens"]),
                 auroc_single_turn=auc(y[st], df.loc[st, "n_tokens"]),
                 rho_human=spearmanr(df.loc[hp, "n_tokens"], df.loc[hp, "human_prob"])[0] if hp.sum() > 2 else None,
                 rho_length=1.0)]
    for c in sides:
        rows.append(dict(side=c, auroc=roc_auc_score(y, df[c]), auroc_single_turn=auc(y[st], df.loc[st, c]),
                         rho_human=spearmanr(df.loc[hp, c], df.loc[hp, "human_prob"])[0] if hp.sum() > 2 else None,
                         rho_length=spearmanr(df[c], df["n_tokens"])[0]))
    out = pd.DataFrame(rows)
    out = out.reindex((out["auroc"] - 0.5).abs().sort_values(ascending=False).index)
    out.to_csv(a.out, index=False)
    print(f"{len(df)} transcripts ({y.sum()} eval / {len(y) - y.sum()} real), {len(sides)} sides -> {a.out}")
    print(out.head(10).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prep"); p.add_argument("dataset"); p.add_argument("out")
    p.add_argument("--agentic", action="store_true"); p.add_argument("--max-tokens", type=int, default=1024)
    s = sub.add_parser("score"); s.add_argument("transcripts"); s.add_argument("activations"); s.add_argument("out")
    a = ap.parse_args()
    prep(a) if a.cmd == "prep" else score(a)
