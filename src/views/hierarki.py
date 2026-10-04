"""Section Hierarki: treemap + sunburst. Kelompok Komoditas > Komoditas > Negara. Sumber: BPS."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src import data, style

FONT = "Inter, Arial, sans-serif"


def _potong(s, maks=22):
    return s if len(s) <= maks else s[:maks - 1].rstrip() + "…"


def _tabel_node(tahun, sembunyi15, k):
    cn = data.chapter_negara_tahun()
    if sembunyi15:
        cn = cn[cn["hs2"] != "15"]
    info = cn[["hs2", "nama_chapter", "seksi", "nama_seksi"]].drop_duplicates()

    a = cn[cn["tahun"] == tahun][["hs2", "negara", "nilai_usd"]].rename(columns={"nilai_usd": "cur"})
    b = cn[cn["tahun"] == tahun - 1][["hs2", "negara", "nilai_usd"]].rename(columns={"nilai_usd": "prev"})
    d = a.merge(b, on=["hs2", "negara"], how="outer").fillna({"cur": 0, "prev": 0})
    d = d.merge(info, on="hs2")

    rank = d.groupby("hs2")["cur"].rank(method="first", ascending=False)
    d["neg"] = d["negara"].where(rank <= k, "Lainnya")

    def agg(by):
        return d.groupby(by, as_index=False)[["cur", "prev"]].sum()

    baris = []
    
    baris.append(("TOTAL", "Semua Komoditas", "", d["cur"].sum(), d["prev"].sum(), "Root", ""))
    
    for r in agg(["seksi", "nama_seksi"]).itertuples():
        baris.append((r.seksi, r.nama_seksi, "TOTAL", r.cur, r.prev, "Kelompok", f"Seksi {r.seksi}"))
    for r in agg(["seksi", "hs2", "nama_chapter"]).itertuples():
        baris.append((f"{r.seksi}/{r.hs2}", r.nama_chapter, r.seksi, r.cur, r.prev,
                      "Komoditas", f"HS {r.hs2}"))
    for r in agg(["seksi", "hs2", "neg"]).itertuples():
        baris.append((f"{r.seksi}/{r.hs2}/{r.neg}", r.neg, f"{r.seksi}/{r.hs2}",
                      r.cur, r.prev, "Negara", ""))

    n = pd.DataFrame(baris, columns=["id", "label", "parent", "cur", "prev", "tingkat", "kode"])
    n = n[n["cur"] > 0].copy()
    n["yoy"] = (n["cur"] - n["prev"]) / n["prev"] * 100
    n.loc[n["prev"] <= 0, "yoy"] = float("nan")
    return n


def _fig(n, jenis, total):
    warna = n["yoy"].clip(-50, 50).fillna(0)
    yoy_txt = n["yoy"].map(lambda v: "tidak ada pembanding" if pd.isna(v)
                           else f"{v:+.1f}%".replace(".", ","))
    porsi = (n["cur"] / total).map(lambda v: f"{v:.1%}".replace(".", ","))
    
    label_pendek = n["label"].apply(lambda s: _potong(s, 22))
    custom = list(zip(n["label"], n["cur"].map(style.format_usd), porsi, yoy_txt, n["kode"], label_pendek))

    kw = dict(
        ids=n["id"], labels=n["label"], parents=n["parent"], values=n["cur"],
        branchvalues="total", customdata=custom, maxdepth=2,
        hovertemplate=("<b>%{customdata[0]}</b> %{customdata[4]}<br>Nilai: %{customdata[1]}"
                       "<br>Porsi dari total: %{customdata[2]}"
                       "<br>Perubahan dari tahun lalu: %{customdata[3]}<extra></extra>"),
        marker=dict(
            colors=warna, colorscale=style.DIVERGEN, cmid=0, cmin=-50, cmax=50,
            line=dict(width=2, color="#FFFFFF"),
            colorbar=dict(title=dict(text="Perubahan (%)", font=dict(family=FONT, size=12)),
                          tickvals=[-50, -25, 0, 25, 50],
                          ticktext=["≤ -50", "-25", "0", "25", "≥ 50"],
                          tickfont=dict(family=FONT, size=12, color=style.TEKS2),
                          thickness=12, len=0.7, outlinewidth=0)),
        textfont=dict(family=FONT, size=13),
    )
    
    if jenis == "treemap":
        fig = go.Figure(go.Treemap(
            texttemplate="<b>%{customdata[5]}</b>", tiling=dict(pad=4),
            pathbar=dict(visible=True, thickness=30, edgeshape=">",
                         textfont=dict(family=FONT, size=13, color=style.TEKS)), **kw))
    else:
        fig = go.Figure(go.Sunburst(
            texttemplate="%{customdata[5]}",
            insidetextorientation="radial", **kw))

    fig.update_layout(
        height=520, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, color=style.TEKS),
        
        uniformtext=dict(minsize=10, mode="hide"),
        
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor=style.BORDER,
                        font=dict(family=FONT, size=13, color=style.TEKS)),
    )
    return fig


def render_hierarki(tahun: int):
    # ---- Temuan utama ----
    penuh = _tabel_node(tahun, False, 5)
    total_penuh = penuh.loc[penuh["tingkat"] == "Kelompok", "cur"].sum()
    km = penuh[penuh["tingkat"] == "Komoditas"].copy()
    top = km.nlargest(1, "cur").iloc[0]
    ada_pembanding = tahun > data.chapter_tahun()["tahun"].min()

    st.subheader(f"{top['label']} menyumbang {top['cur'] / total_penuh:.0%} ekspor pangan {tahun}")
    st.caption(f"Total {style.format_usd(total_penuh)} | Ukuran kotak = nilai ekspor (USD) | "
               "Warna = perubahan dari tahun lalu (hijau naik, oranye turun, abu-abu tidak ada pembanding)")

    if ada_pembanding:
        km["delta"] = km["cur"] - km["prev"]
        naik, turun = km.nlargest(1, "delta").iloc[0], km.nsmallest(1, "delta").iloc[0]
        k1, k2, k3 = st.columns(3)
        
        k1.markdown(style.kartu("Penyumbang terbesar", 
                                f"{top['cur'] / total_penuh:.0%} dari total", 
                                top["label"]),
                    unsafe_allow_html=True)
        
        k2.markdown(style.kartu("Kenaikan nilai terbesar", 
                                f"+{style.format_usd(naik['delta'])}", 
                                naik["label"], 
                                "#007656"),
                    unsafe_allow_html=True)
        
        k3.markdown(style.kartu("Penurunan nilai terbesar", 
                                style.format_usd(turun["delta"]), 
                                turun["label"], 
                                "#D93025"), 
                    unsafe_allow_html=True)
    else:
        st.info("Tahun terawal tidak punya pembanding, jadi warna perubahan tidak tersedia. "
                "Pilih 2024 atau 2025.")

    # ---- Kontrol ----
    st.markdown("**Cara pakai:** \n 1) Lihat ukuran kotak. \n 2) Klik kotak untuk melihat isinya. \n 3) Klik tulisan di bagian atas grafik untuk kembali.")
    sembunyi15 = st.toggle("Sembunyikan minyak sawit agar komoditas lain lebih terlihat",
                           value=False, key="h_s15")
    if sembunyi15:
        st.caption("Lemak dan Minyak disembunyikan: porsi di tooltip dihitung terhadap total tanpa Komoditas Lemak dan Minyak.")
    style.css_segmen()
    with st.container(key="segmen_detail"):
        pilihan = st.radio(
            "Detail negara tujuan per komoditas",
            ["5 negara", "10 negara", "20 negara"],
            index=1, horizontal=True, key="h_detail",
            help="Jumlah negara tujuan terbesar di tiap komoditas; sisanya digabung 'Lainnya'.",
        )
    k = {"5 negara": 5, "10 negara": 10, "20 negara": 20}[pilihan]

    st.caption("**Panduan Filter:** ")
    st.caption(f"Saat sebuah komoditas diklik, grafik hanya memunculkan {k} negara pembeli terbesar untuk komoditas tersebut. Sisa negara lainnya otomatis digabung ke bagian 'Lainnya'.")

    n = _tabel_node(tahun, sembunyi15, k)
    total = n.loc[n["tingkat"] == "Kelompok", "cur"].sum()
    assert abs(n.loc[n["tingkat"] == "Negara", "cur"].sum() - total) < 1, "Total daun tidak cocok"

    st.markdown("**Treemap**")
    st.caption("Klik kotak untuk melihat isinya: kelompok, komoditas, lalu negara tujuan.")
    st.plotly_chart(_fig(n, "treemap", total), use_container_width=True)
    style.chart_footer("USD")
    with st.expander("Panduan membaca Treemap", expanded=False):
        st.markdown(
            "- **Cara baca:** satu kotak = satu kelompok atau komoditas. Makin luas kotak, makin besar nilai ekspor. "
            "Warna menunjukkan perubahan dari tahun lalu (biru naik, oranye turun, abu-abu tidak ada pembanding).\n"
            "- **Interaksi:** klik kotak untuk memperbesar dan melihat negara tujuannya. "
            "Klik tulisan pada jejak di bagian atas grafik untuk kembali.\n"
            "- **Tooltip:** arahkan kursor untuk melihat nama, nilai, porsi, dan perubahan.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Sunburst**")
    st.caption("Lingkaran dalam = kelompok, luar = komoditas. Klik irisan untuk memperbesar.")
    st.plotly_chart(_fig(n, "sunburst", total), use_container_width=True)
    style.chart_footer("USD")
    with st.expander("Panduan membaca Sunburst", expanded=False):
        st.markdown(
            "- **Cara baca:** cincin dalam = kelompok, cincin luar = komoditas. "
            "Makin lebar irisan, makin besar nilai ekspor. Warna sama dengan Treemap.\n"
            "- **Interaksi:** klik irisan untuk memfokuskannya dan membuka lapisan negara tujuan untuk melihat detailnya. "
            "Klik lingkaran di tengah untuk kembali.\n"
            "- **Catatan:** irisan yang terlalu sempit tidak diberi label; arahkan kursor untuk melihat nama dan rinciannya.")