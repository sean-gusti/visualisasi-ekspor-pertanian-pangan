"""Section Aliran: Sankey + Flow Map Geospasial. Komoditas -> Negara tujuan. Sumber: BPS."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src import data, style

FONT = "Inter, Arial, sans-serif"

KOORDINAT_NEGARA = {
    # Asia Timur & Tenggara
    "China": (35.8617, 104.1954), "Japan": (36.2048, 138.2529), 
    "Korea Republic Of": (35.9078, 127.7669), "Hong Kong": (22.3193, 114.1694),
    "Taiwan": (23.6978, 120.9605), "Macau": (22.1987, 113.5439), 
    "Mongolia": (46.8625, 103.8467),
    "Malaysia": (4.2105, 101.9758), "Singapore": (1.3521, 103.8198), 
    "Thailand": (15.8700, 100.9925), "Viet Nam": (14.0583, 108.2772), 
    "Philippines": (12.8797, 121.7740), "Myanmar": (21.9162, 95.9560), 
    "Cambodia": (12.5657, 104.9910), "Brunei Darussalam": (4.5353, 114.7277), 
    "Lao Peoples Dem. Rep.": (19.8563, 102.4955), "East Timor": (-8.8742, 125.7275),
    
    # Asia Selatan & Tengah
    "India": (20.5937, 78.9629), "Pakistan": (30.3753, 69.3451), 
    "Bangladesh": (23.6850, 90.3563), "Sri Lanka": (7.8731, 80.7718), 
    "Nepal": (28.3949, 84.1240), "Maldives": (3.2028, 73.2207), 
    "Afghanistan": (33.9391, 67.7100), "Bhutan": (27.5142, 90.4336),
    "Kazakhstan": (48.0196, 66.9237), "Uzbekistan": (41.3775, 64.5853),
    "Kyrgyzstan": (41.2044, 74.7661), "Tajikistan": (38.8610, 71.2761),
    "Turkmenistan": (38.9697, 59.5563),

    # Asia Barat & Timur Tengah
    "Saudi Arabia": (23.8859, 45.0792), "United Arab Emirates": (23.4241, 53.8478),
    "Turkey": (38.9637, 35.2433), "Iran (Islamic Republic Of)": (32.4279, 53.6880),
    "Iraq": (33.2232, 43.6793), "Israel": (31.0461, 34.8516), 
    "Qatar": (25.3548, 51.1839), "Kuwait": (29.3117, 47.4818), 
    "Oman": (21.5126, 55.9233), "Bahrain": (26.0667, 50.5577), 
    "Jordan": (30.5852, 36.2384), "Lebanon": (33.8547, 35.8623), 
    "Syria Arab Republic": (34.8021, 38.9968), "Yemen": (15.5527, 48.5164), 
    "Palestina": (31.9522, 35.2332), "Cyprus": (35.1264, 33.4299),
    "Armenia": (40.0691, 45.0382), "Azerbaijan": (40.1431, 47.5769),
    "Georgia": (42.3154, 43.3569),

    # Eropa (Barat, Timur, Utara, Selatan)
    "Netherlands": (52.1326, 5.2913), "Germany Fed. Rep. Of": (51.1657, 10.4515),
    "Italy": (41.8719, 12.5674), "Spain": (40.4637, -3.7492),
    "United Kingdom": (55.3781, -3.4360), "France": (46.2276, 2.2137),
    "Belgium": (50.5039, 4.4699), "Switzerland": (46.8182, 8.2275),
    "Poland": (51.9194, 19.1451), "Russia Federation": (61.5240, 105.3188),
    "Ukraine": (48.3794, 31.1656), "Romania": (45.9432, 24.9668),
    "Greece": (39.0742, 21.8243), "Austria": (47.5162, 14.5501),
    "Czech Republic": (49.8153, 15.4730), "Hungary": (47.1625, 19.5033),
    "Sweden": (60.1282, 18.6435), "Norway": (60.4720, 8.4689),
    "Denmark": (56.2639, 9.5018), "Finland": (61.9241, 25.7482),
    "Ireland": (53.1424, -7.6921), "Portugal": (39.3999, -8.2245),
    "Bulgaria": (42.7339, 25.4858), "Croatia": (45.1000, 15.2000),
    "Serbia": (44.0165, 21.0059), "Slovakia": (48.6690, 19.6990),
    "Belarus": (53.7098, 27.9534), "Lithuania": (55.1694, 23.8813),
    "Latvia": (56.8796, 24.6032), "Estonia": (58.5953, 25.0136),
    "Slovenia": (46.1512, 14.9955), "Bosnia And Herzegovina": (43.9159, 17.6791),
    "Moldova Republic Of": (47.4116, 28.3699), "Rep. Of Macedonia": (41.6086, 21.7453),
    "Albania": (41.1533, 20.1683), "Luxembourg": (49.8153, 6.1296),
    "Iceland": (64.9631, -19.0208), "Malta": (35.9375, 14.3754),
    "Montenegro": (42.7087, 19.3744), "Andorra": (42.5063, 1.5218),
    "San Marino": (43.9424, 12.4578), "Kosovo": (42.6026, 20.9030),

    # Amerika Utara & Latin
    "United States": (37.0902, -95.7129), "Canada": (56.1304, -106.3468),
    "Mexico": (23.6345, -102.5528), "Brazil": (-14.2350, -51.9253),
    "Argentina": (-38.4161, -63.6167), "Chile": (-35.6751, -71.5430),
    "Peru": (-9.1900, -75.0152), "Colombia": (4.5709, -74.2973),
    "Ecuador": (-1.8312, -78.1834), "Venezuela": (9.1899, -69.8395),
    "Uruguay": (-32.5228, -55.7658), "Paraguay": (-23.4425, -58.4438),
    "Bolivia": (-16.2902, -63.5887), "Guyana": (4.8604, -58.9302),
    "Suriname": (3.9193, -56.0278), "Panama": (8.5380, -80.7821),
    "Costa Rica": (9.7489, -83.7534), "Guatemala": (15.7835, -90.2308),
    "Honduras": (15.2000, -86.2419), "El Salvador": (13.7942, -88.8965),
    "Nicaragua": (12.8654, -85.2072), "Dominican Republic": (18.7357, -70.1627),
    "Cuba": (21.5218, -77.7812), "Haiti": (18.9712, -72.2852),
    "Jamaica": (18.1096, -77.2975), "Puerto Rico": (18.2208, -66.5901),

    # Afrika
    "Egypt": (26.8206, 30.8025), "South Africa": (-30.5595, 22.9375),
    "Nigeria": (9.0820, 8.6753), "Morocco": (31.7917, -7.0926),
    "Algeria": (28.0339, 1.6596), "Kenya": (-0.0236, 37.9062),
    "Ghana": (7.9465, -1.0232), "Tanzania United Rep. Of": (-6.3690, 34.8888),
    "Uganda": (1.3733, 32.2903), "Senegal": (14.4974, -14.4524),
    "Cote Divoire": (7.5400, -5.5471), "Cameroon": (3.8480, 11.5021),
    "Angola": (-11.2027, 17.8739), "Mozambique": (-18.6657, 35.5296),
    "Madagascar": (-18.7669, 46.8691), "Mauritius": (-20.3484, 57.5522),
    "Zimbabwe": (-19.0154, 29.1549), "Zambia": (-13.1339, 27.8493),
    "Democratic Rep. Of The Congo": (-4.0383, 21.7587),
    "Libyan Arab Jamahiriya": (26.3351, 17.2283), "Tunisia": (33.8869, 9.5375),
    "Sudan": (12.8628, 30.2176), "Ethiopia": (9.1450, 40.4897),
    
    # Oseania & Wilayah Kecil
    "Australia": (-25.2744, 133.7751), "New Zealand": (-40.9006, 174.8860),
    "Papua New Guinea": (-6.3149, 143.9555), "Fiji": (-17.7134, 178.0650),
    "Solomon Islands": (-9.6457, 160.1562), "Vanuatu": (-15.3767, 166.9592),
    "Samoa": (-13.7590, -172.1046), "Guam": (13.4443, 144.7937),
    
    # Titik Cadangan
    "Negara lainnya": (0.0000, 0.0000)
}

LAT_ASAL, LON_ASAL = -6.2088, 106.8456

def _ambil_koordinat(nama_negara):
    if not nama_negara:
        return (0, 0)
    
    # 1. Cek langsung dengan nama asli di data
    if nama_negara in KOORDINAT_NEGARA:
        return KOORDINAT_NEGARA[nama_negara]
        
    # 2. Cek fleksibel
    for k, v in KOORDINAT_NEGARA.items():
        if k.lower() in nama_negara.lower() or nama_negara.lower() in k.lower():
            return v
            
    return (0, 0)

def _potong(s, maks=26):
    """Potong label panjang agar muat di node Sankey."""
    return s if len(s) <= maks else s[:maks - 1].rstrip() + "…"


def _siap(tahun, ambang, topn):
    """Siapkan data aliran: komoditas → negara, setelah filter ambang dan topN."""
    cn = data.chapter_negara_tahun()
    d = cn[cn["tahun"] == tahun].copy()
    total = d["nilai_usd"].sum()
    n_neg = d["negara"].nunique()

    # Komoditas di bawah ambang % digabung jadi "Komoditas lainnya"
    ch = d.groupby(["hs2", "nama_chapter", "seksi"], as_index=False)["nilai_usd"].sum()
    ch["pct"] = ch["nilai_usd"] / total * 100
    besar = set(ch.loc[ch["pct"] >= ambang, "hs2"])

    d["ch_label"] = d.apply(
        lambda r: r["nama_chapter"] if r["hs2"] in besar
        else "Komoditas lainnya", axis=1)
    d["ch_seksi"] = d.apply(
        lambda r: r["seksi"] if r["hs2"] in besar else "X", axis=1)

    # Negara di luar top-N digabung
    neg = d.groupby("negara")["nilai_usd"].sum().sort_values(ascending=False)
    top_neg = set(neg.head(topn).index)
    d["neg_label"] = d["negara"].where(d["negara"].isin(top_neg), "Negara lainnya")

    alir = (d.groupby(["ch_label", "ch_seksi", "neg_label"], as_index=False)["nilai_usd"]
              .sum()
              .query("nilai_usd > 0")
              .sort_values("nilai_usd", ascending=False))
    return alir, total, neg, n_neg


# ---- Sankey ----

def _fig_sankey(alir, total):
    """Diagram Sankey: komoditas (kiri) → negara tujuan (kanan)."""
    sumber = sorted(alir["ch_label"].unique(),
                    key=lambda x: (x == "Komoditas lainnya", x))
    tujuan = sorted(alir["neg_label"].unique(),
                    key=lambda x: (x == "Negara lainnya", x))
    nodes = list(sumber) + list(tujuan)
    idx = {n: i for i, n in enumerate(nodes)}

    seksi_map = dict(alir.drop_duplicates("ch_label")[["ch_label", "ch_seksi"]].values)
    palet = style.OKABE_ITO
    w_seksi = {"I": palet[0], "II": palet[1], "III": palet[2],
               "IV": palet[3], "X": "#C0C0C0"}
    src_colors = [w_seksi.get(seksi_map.get(s, "X"), "#C0C0C0") for s in sumber]
    tgt_colors = ["#A3E4D7"] * len(tujuan)
    node_colors = src_colors + tgt_colors

    def rgba(hex_c, a=0.35):
        r, g, b = int(hex_c[1:3], 16), int(hex_c[3:5], 16), int(hex_c[5:7], 16)
        return f"rgba({r},{g},{b},{a})"

    link_src = [idx[r.ch_label] for r in alir.itertuples()]
    link_tgt = [idx[r.neg_label] for r in alir.itertuples()]
    link_val = alir["nilai_usd"].tolist()
    link_col = [rgba(w_seksi.get(seksi_map.get(r.ch_label, "X"), "#C0C0C0"), 0.4)
                for r in alir.itertuples()]

    node_tot = {}
    for r in alir.itertuples():
        node_tot[r.ch_label] = node_tot.get(r.ch_label, 0) + r.nilai_usd
        node_tot[r.neg_label] = node_tot.get(r.neg_label, 0) + r.nilai_usd
    node_hover = [f"{n}<br>{style.format_usd(node_tot.get(n, 0))} "
                  f"({node_tot.get(n, 0) / total:.1%})" for n in nodes]

    link_hover = [f"{r.ch_label} → {r.neg_label}<br>"
                  f"{style.format_usd(r.nilai_usd)} ({r.nilai_usd / total:.1%})"
                  for r in alir.itertuples()]

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=18, thickness=22,
            line=dict(color="#FFFFFF", width=1),
            label=[_potong(n) for n in nodes],
            color=node_colors,
            customdata=node_hover,
            hovertemplate="%{customdata}<extra></extra>",
        ),
        link=dict(
            source=link_src, target=link_tgt, value=link_val,
            color=link_col,
            customdata=link_hover,
            hovertemplate="%{customdata}<extra></extra>",
        ),
    ))
    fig.update_layout(
        height=580, margin=dict(l=0, r=0, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, size=12, color=style.TEKS),
    )
    return fig


# ---- Flow Map (Peta Aliran Geospasial) ----

def _fig_flow_map(alir, total):
    """Peta Aliran (Flow Map): Menampilkan garis ekspor dari Indonesia ke negara tujuan."""
    df_map = alir.groupby("neg_label", as_index=False)["nilai_usd"].sum()
    df_map = df_map[df_map["neg_label"] != "Negara lainnya"].sort_values("nilai_usd", ascending=False)
    
    fig = go.Figure()

    for r in df_map.itertuples():
        negara = r.neg_label
        lat_tuj, lon_tuj = _ambil_koordinat(negara)
        if (lat_tuj, lon_tuj) == (0, 0):
            continue
        
        lw = max(1, min(12, (r.nilai_usd / df_map["nilai_usd"].max()) * 12))
        
        fig.add_trace(go.Scattergeo(
            lat=[LAT_ASAL, lat_tuj],
            lon=[LON_ASAL, lon_tuj],
            mode='lines',
            line=dict(width=lw, color='#009E73'),
            opacity=0.6,
            hoverinfo='text',
            text=f"Ekspor ke {negara}: {style.format_usd(r.nilai_usd)} ({r.nilai_usd/total:.1%})"
        ))

    for r in df_map.itertuples():
        negara = r.neg_label
        lat_tuj, lon_tuj = _ambil_koordinat(negara)
        if (lat_tuj, lon_tuj) == (0, 0):
            continue
        marker_size = max(6, min(25, (r.nilai_usd / df_map["nilai_usd"].max()) * 25))

        fig.add_trace(go.Scattergeo(
            lat=[lat_tuj],
            lon=[lon_tuj],
            mode='markers+text',
            text=[negara if r.nilai_usd > df_map["nilai_usd"].quantile(0.5) else ""],
            textposition="top right",
            marker=dict(
                size=marker_size,
                color='#E69F00',
                line=dict(width=1, color='#FFFFFF')
            ),
            hoverinfo='text',
            textfont=dict(size=10, color=style.TEKS),
            hovertext=f"<b>{negara}</b><br>Nilai Ekspor: {style.format_usd(r.nilai_usd)}<br>Porsi: {r.nilai_usd/total:.1%}"
        ))

    fig.add_trace(go.Scattergeo(
        lat=[LAT_ASAL],
        lon=[LON_ASAL],
        mode='markers+text',
        text=["🇮🇩 Indonesia"],
        textposition="bottom right",
        marker=dict(size=12, color='#D55E00', symbol='star'),
        hoverinfo='text',
        hovertext="Pusat Ekspor: Indonesia"
    ))

    fig.update_layout(
        height=550,
        margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            showland=True,
            landcolor="#F8F9FA",
            subunitcolor="#E0E0E0",
            countrycolor="#D3D3D3",
            showocean=True,
            oceancolor="#E8F4F8",
            projection_type="natural earth",
        ),
        font=dict(family=FONT, size=12, color=style.TEKS),
        showlegend=False
    )
    return fig

# ---- Render utama ----

def render_aliran(tahun: int):
    ambang, topn = style.kontrol_negara("aliran")
    alir, total, neg, n_negara = _siap(tahun, ambang, topn)

    neg_top = neg.index[0]
    neg_top_val = neg.iloc[0]
    top5_share = neg.head(5).sum() / total
    
    st.caption(
        f"**Panduan Filter:** "
        f"\n - Ambang Kontribusi (%): Komoditas dengan porsi di bawah nilai ini akan otomatis diringkas menjadi 'Komoditas lainnya'. "
        f"\n - Jumlah Negara Teratas (negara): Membatasi rute visualisasi peta dan Sankey hanya pada {topn} negara tujuan utama untuk menghindari kepadatan visual (*visual clutter*)."
    )
    
    st.subheader(f"{neg_top} adalah tujuan ekspor pangan terbesar "
                 f"({neg_top_val / total:.0%})")
    
    st.caption(f"Total {style.format_usd(total)} ke {n_negara} negara "
               f"| Komoditas di bawah {ambang}% digabung "
               f"| {topn} negara teratas ditampilkan")

    k1, k2, k3 = st.columns(3)
    k1.markdown(style.kartu("Tujuan terbesar", f"{neg_top_val / total:.0%}", neg_top, "#007656"),
                unsafe_allow_html=True)
    k2.markdown(style.kartu("Konsentrasi 5 negara teratas", f"{top5_share:.0%}",
                            style.format_usd(neg.head(5).sum())), unsafe_allow_html=True)
    k3.markdown(style.kartu("Negara tujuan aktif", str(n_negara), "menerima ekspor pangan"),
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Sankey ----
    st.markdown("**Diagram Sankey**")
    st.caption("Kiri = komoditas, kanan = negara tujuan. Lebar pita = nilai ekspor.")
    st.plotly_chart(_fig_sankey(alir, total), use_container_width=True)
    style.chart_footer("USD")
    with st.expander("Panduan membaca Sankey", expanded=False):
        st.markdown(
            "- **Cara baca:** pita menghubungkan komoditas (kiri) ke negara tujuan (kanan). "
            "Makin lebar pita, makin besar nilai ekspor. Warna pita mengikuti kelompok komoditas.\n"
            "- **Interaksi:** arahkan kursor ke pita atau kotak untuk melihat nilai dan porsi; "
            "kotak bisa digeser untuk merapikan tampilan.\n"
            "- **Filter:** ubah ambang kontribusi dan jumlah negara teratas di atas grafik.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Flow Map ----
    st.markdown("**Peta Aliran (Flow Map Ekspor)**")
    st.caption("Garis dari Indonesia ke negara tujuan. Ketebalan garis dan ukuran titik = nilai ekspor.")
    st.plotly_chart(_fig_flow_map(alir, total), use_container_width=True)
    style.chart_footer("USD")
    with st.expander("Panduan membaca Peta Aliran", expanded=False):
        st.markdown(
            "- **Cara baca:** setiap garis adalah rute ekspor dari Indonesia ke satu negara. "
            "Garis tebal dan titik besar berarti nilai ekspor besar.\n"
            "- **Interaksi:** arahkan kursor ke titik negara untuk melihat nilai dan porsi; "
            "geser dan zoom peta dengan mouse.\n"
            "- **Catatan:** negara tanpa koordinat dan kelompok 'Negara lainnya' tidak digambar di peta.")