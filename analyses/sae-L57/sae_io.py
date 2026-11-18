"""Minimal, dependency-light loader for the alxcspr/stationhouse TopK SAEs (sparsify format).

Memory-maps sae.safetensors (no torch needed) and converts bf16/f16 to float32 on demand.
"""
import json, struct, numpy as np

DT = {'F32': np.float32, 'F16': np.float16, 'BF16': np.uint16}


class SAE:
    def __init__(self, path):
        with open(path, 'rb') as f:
            n = struct.unpack('<Q', f.read(8))[0]
            self.header = json.loads(f.read(n))
        self.base = 8 + n
        self.path = path
        self.meta = self.header.pop('__metadata__', None)

    def keys(self):
        return {k: (v['dtype'], v['shape']) for k, v in self.header.items()}

    def raw(self, key):
        h = self.header[key]
        a, b = h['data_offsets']
        return np.memmap(self.path, dtype=DT[h['dtype']], mode='r', offset=self.base + a,
                         shape=tuple(h['shape'])), h['dtype']

    def get(self, key, rows=None):
        """float32 copy of a tensor (optionally a row subset)."""
        m, dt = self.raw(key)
        x = np.asarray(m if rows is None else m[rows])
        if dt == 'BF16':
            return (x.astype(np.uint32) << 16).view(np.float32)
        return x.astype(np.float32)
