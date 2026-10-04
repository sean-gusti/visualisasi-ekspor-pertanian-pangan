"""Gabung ekspor HS 2 digit (BPS) ke format tidy.
Grain: hs2 x tahun x bulan x negara x pelabuhan. Sumber: BPS."""
import re
from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

FILES = ["Ekspor_HS_1-12.xlsx", "Ekspor_HS_13-24.xlsx"]
R_NEGARA, R_PELABUHAN, R_BULAN, R_DATA = 1, 2, 3, 5  
C_HS, C_TAHUN, C_DATA = 0, 1, 3                      


def angka_kurung(s):
    m = re.search(r"\[(\d{1,2})\]", str(s))
    return int(m.group(1)) if m else None


def baca_satu(nama):
    raw = pd.read_excel(RAW / nama, header=None, sheet_name=0)
    n = raw.shape[1] - C_DATA

    negara = raw.iloc[R_NEGARA, C_DATA:].ffill().astype(str).str.strip()
    pelabuhan = raw.iloc[R_PELABUHAN, C_DATA:].ffill().astype(str).str.strip()
    bulan = raw.iloc[R_BULAN, C_DATA:].map(angka_kurung)
    meta = pd.DataFrame({"kol": range(n), "negara": negara.values,
                         "pelabuhan": pelabuhan.values, "bulan": bulan.values})

    data = raw.iloc[R_DATA:].copy()
    data["hs2"] = data[C_HS].ffill().map(angka_kurung)
    data["tahun"] = pd.to_numeric(data[C_TAHUN], errors="coerce")
    data = data[data["tahun"].notna() & data["hs2"].notna()]

    vals = data.iloc[:, C_DATA:C_DATA + n].copy()
    vals.columns = range(n)
    vals["hs2"] = data["hs2"].astype(int).astype(str).str.zfill(2)
    vals["tahun"] = data["tahun"].astype(int)

    long = vals.melt(id_vars=["hs2", "tahun"], var_name="kol", value_name="nilai_usd")
    long["nilai_usd"] = pd.to_numeric(long["nilai_usd"], errors="coerce")
    long = long.dropna(subset=["nilai_usd"]).merge(meta, on="kol")

    is_tot = long["negara"].str.lower().str.startswith("total")
    tot = long[is_tot].set_index(["hs2", "tahun"])["nilai_usd"].rename("total_bps")
    detail = long[~is_tot].drop(columns="kol")
    print(nama, "-> baris detail:", len(detail), "| chapter:", sorted(detail["hs2"].unique()))
    return detail, tot


hasil = [baca_satu(f) for f in FILES]
detail = pd.concat([h[0] for h in hasil], ignore_index=True)
totals = pd.concat([h[1] for h in hasil])

# Pembersihan
detail["negara"] = detail["negara"].str.title()
detail["bulan"] = pd.to_numeric(detail["bulan"], errors="coerce").astype("Int64")

# Gabung pemetaan seksi
peta = pd.read_csv("data/mapping/hs_seksi.csv", dtype={"hs2": str})
detail = detail.merge(peta, on="hs2", how="left", validate="m:1")

# ---- Validasi ----
assert detail["hs2"].nunique() == 24, f"Chapter: {detail['hs2'].nunique()}"
assert detail["seksi"].notna().all(), "Ada chapter tanpa seksi"
print("\nBaris dengan bulan kosong:", detail["bulan"].isna().sum())

cek = detail.groupby(["hs2", "tahun"])["nilai_usd"].sum().to_frame("detail").join(totals)
cek["selisih"] = cek["detail"] - cek["total_bps"]
bad = cek[cek["selisih"].abs() > 1]
print("Selisih detail vs Totals BPS (> 1 USD):", len(bad), "dari", len(cek), "chapter-tahun")
if len(bad):
    print(bad.head(10))

# ---- Ringkasan untuk dilaporkan ----
print("\nBulan unik per tahun:\n", detail.groupby("tahun")["bulan"].nunique())
print("Jumlah negara:", detail["negara"].nunique(), "| pelabuhan:", detail["pelabuhan"].nunique())
print("Total per tahun (USD):\n", detail.groupby("tahun")["nilai_usd"].sum().round(0))
print("Top 5 negara:\n", detail.groupby("negara")["nilai_usd"].sum().nlargest(5).round(0))

# ---- Simpan ----
kolom = ["tahun", "bulan", "hs2", "nama_chapter", "seksi", "nama_seksi",
         "negara", "pelabuhan", "nilai_usd"]
detail[kolom].to_csv(OUT / "ekspor_hs2_detail.csv", index=False)

kunci = [k for k in kolom if k not in ("bulan", "nilai_usd")]
agg = detail.groupby(kunci, as_index=False)["nilai_usd"].sum()
agg.to_csv(OUT / "ekspor_hs2_tahun_negara_pelabuhan.csv", index=False)
print("\nSelesai. Baris detail:", len(detail), "| baris agregat:", len(agg))