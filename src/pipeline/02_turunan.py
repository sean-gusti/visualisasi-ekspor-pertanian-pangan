"""Buat tabel turunan dari data tidy untuk app. Sumber: BPS."""
from pathlib import Path
import pandas as pd

OUT = Path("data/processed")
agg = pd.read_csv(OUT / "ekspor_hs2_tahun_negara_pelabuhan.csv", dtype={"hs2": str})
info = agg[["hs2", "nama_chapter", "seksi", "nama_seksi"]].drop_duplicates()


def tambah_yoy(df, kunci):
    """Pertumbuhan y-o-y (%) per kunci. NaN bila tahun sebelumnya tidak ada atau 0."""
    p = df.pivot_table(index=kunci, columns="tahun", values="nilai_usd",
                       aggfunc="sum", fill_value=0)
    tahun = sorted(p.columns)
    baris = []
    for i, t in enumerate(tahun):
        d = p[t].rename("nilai_usd").reset_index()
        d["tahun"] = t
        if i == 0:
            d["yoy_pct"] = float("nan")
        else:
            prev = p[tahun[i - 1]].values
            d["yoy_pct"] = [(c - b) / b * 100 if b > 0 else float("nan")
                            for c, b in zip(p[t].values, prev)]
        baris.append(d)
    return pd.concat(baris, ignore_index=True)


ch = agg.groupby(["tahun", "hs2"], as_index=False)["nilai_usd"].sum()
ch = tambah_yoy(ch, ["hs2"]).merge(info, on="hs2")
ch.to_csv(OUT / "chapter_tahun.csv", index=False)

cn = agg.groupby(["tahun", "hs2", "negara"], as_index=False)["nilai_usd"].sum()
cn = tambah_yoy(cn, ["hs2", "negara"]).merge(info, on="hs2")
cn = cn[cn["nilai_usd"] > 0]
cn.to_csv(OUT / "chapter_negara_tahun.csv", index=False)

ng = agg.groupby(["tahun", "negara"], as_index=False)["nilai_usd"].sum()
ng = tambah_yoy(ng, ["negara"])
ng.to_csv(OUT / "negara_tahun.csv", index=False)

# ---- Validasi ----
tot = agg.groupby("tahun")["nilai_usd"].sum()
for nama, d in [("chapter_tahun", ch), ("chapter_negara_tahun", cn), ("negara_tahun", ng)]:
    cek = d.groupby("tahun")["nilai_usd"].sum()
    assert ((cek - tot).abs() < 1).all(), f"Total {nama} tidak cocok"
print("Total konsisten di semua tabel.")
print(ch[ch.tahun == 2025].nlargest(5, "nilai_usd")[["hs2", "nama_chapter", "nilai_usd", "yoy_pct"]])
print("Pasangan chapter-negara 2025:", (cn.tahun == 2025).sum())
print("Negara dengan nilai > 0 per tahun:", cn.groupby("tahun")["negara"].nunique().to_dict())
nm = pd.Series(sorted(agg["negara"].unique()))
kunci = nm.str.lower().str.replace(r"[^a-z]", "", regex=True)
print("Kandidat duplikat nama:", nm[kunci.duplicated(keep=False)].tolist())
print("Selesai.")