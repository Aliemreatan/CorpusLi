import pandas as pd, re, os, textwrap, json, math, numpy as np, csv, pathlib

in_path = "C:\Users\aliem\Documents\corpus_manipulator\conllu-to-csv\tr_kenet-ud-dev.conllu"


rows = []
sent_id = None
sent_text = None
sent_idx = 0

def is_mwt_or_empty(token_id: str) -> bool:
    return ("-" in token_id) or ("." in token_id)

with open(in_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line.strip():
            # sentence boundary: reset
            sent_id = None
            sent_text = None
            continue
        if line.startswith("#"):
            # capture common metadata
            if line.startswith("# sent_id ="):
                sent_id = line.split("=", 1)[1].strip()
            elif line.startswith("# text ="):
                sent_text = line.split("=", 1)[1].strip()
            continue
        
        parts = line.split("\t")
        if len(parts) != 10:
            # malformed row; keep as-is with padding so it doesn't break export
            parts = (parts + [""] * 10)[:10]
        
        token_id, form, lemma, upos, xpos, feats, head, deprel, deps, misc = parts
        sent_idx += 1 if token_id == "1" else 0  # rough sentence counter
        
        rows.append({
            "sent_id": sent_id,
            "text": sent_text,
            "id": token_id,
            "form": form,
            "lemma": lemma,
            "upos": upos,
            "xpos": xpos,
            "feats": feats,
            "head": head,
            "deprel": deprel,
            "deps": deps,
            "misc": misc,
            "is_mwt_or_empty": is_mwt_or_empty(token_id),
        })

df_all = pd.DataFrame(rows)

# Tokens-only view: keep numeric integer IDs only
def is_int_id(x):
    return bool(re.fullmatch(r"\d+", str(x)))

df_tokens = df_all[df_all["id"].apply(is_int_id)].copy()
df_tokens["id"] = df_tokens["id"].astype(int)

# Write CSVs
base = os.path.splitext(in_path)[0]
out_all = base + ".allrows.csv"
out_tokens = base + ".tokens.csv"

df_all.to_csv(out_all, index=False, encoding="utf-8")
df_tokens.to_csv(out_tokens, index=False, encoding="utf-8")

(df_all.head(12), out_tokens, out_all, len(df_tokens), len(df_all))
