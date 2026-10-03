"""Section Jaringan: Bipartite graph, Force-Directed, Geo-Network, dan Adjacency Matrix."""
import networkx as nx
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from src import data, style

FONT = "Inter, Arial, sans-serif"

# KAMUS KOORDINAT
KOORDINAT_NEGARA = {
    "China": (35.8617, 104.1954), "Japan": (36.2048, 138.2529), 
    "Korea Republic Of": (35.9078, 127.7669), "Hong Kong": (22.3193, 114.1694),
    "Taiwan": (23.6978, 120.9605), "Macau": (22.1987, 113.5439), 
    "Mongolia": (46.8625, 103.8467), "Malaysia": (4.2105, 101.9758), 
    "Singapore": (1.3521, 103.8198), "Thailand": (15.8700, 100.9925), 
    "Viet Nam": (14.0583, 108.2772), "Philippines": (12.8797, 121.7740), 
    "Myanmar": (21.9162, 95.9560), "Cambodia": (12.5657, 104.9910), 
    "Brunei Darussalam": (4.5353, 114.7277), "Lao Peoples Dem. Rep.": (19.8563, 102.4955), 
    "East Timor": (-8.8742, 125.7275), "India": (20.5937, 78.9629), 
    "Pakistan": (30.3753, 69.3451), "Bangladesh": (23.6850, 90.3563), 
    "Sri Lanka": (7.8731, 80.7718), "Nepal": (28.3949, 84.1240), 
    "Maldives": (3.2028, 73.2207), "Afghanistan": (33.9391, 67.7100), 
    "Bhutan": (27.5142, 90.4336), "Kazakhstan": (48.0196, 66.9237), 
    "Uzbekistan": (41.3775, 64.5853), "Kyrgyzstan": (41.2044, 74.7661), 
    "Tajikistan": (38.8610, 71.2761), "Turkmenistan": (38.9697, 59.5563),
    "Saudi Arabia": (23.8859, 45.0792), "United Arab Emirates": (23.4241, 53.8478),
    "Turkey": (38.9637, 35.2433), "Iran (Islamic Republic Of)": (32.4279, 53.6880),
    "Iraq": (33.2232, 43.6793), "Israel": (31.0461, 34.8516), 
    "Qatar": (25.3548, 51.1839), "Kuwait": (29.3117, 47.4818), 
    "Oman": (21.5126, 55.9233), "Bahrain": (26.0667, 50.5577), 
    "Jordan": (30.5852, 36.2384), "Lebanon": (33.8547, 35.8623), 
    "Syria Arab Republic": (34.8021, 38.9968), "Yemen": (15.5527, 48.5164), 
    "Palestina": (31.9522, 35.2332), "Cyprus": (35.1264, 33.4299),
    "Armenia": (40.0691, 45.0382), "Azerbaijan": (40.1431, 47.5769),
    "Georgia": (42.3154, 43.3569), "Netherlands": (52.1326, 5.2913), 
    "Germany Fed. Rep. Of": (51.1657, 10.4515), "Italy": (41.8719, 12.5674), 
    "Spain": (40.4637, -3.7492), "United Kingdom": (55.3781, -3.4360), 
    "France": (46.2276, 2.2137), "Belgium": (50.5039, 4.4699), 
    "Switzerland": (46.8182, 8.2275), "Poland": (51.9194, 19.1451), 
    "Russia Federation": (61.5240, 105.3188), "Ukraine": (48.3794, 31.1656), 
    "Romania": (45.9432, 24.9668), "Greece": (39.0742, 21.8243), 
    "Austria": (47.5162, 14.5501), "Czech Republic": (49.8153, 15.4730), 
    "Hungary": (47.1625, 19.5033), "Sweden": (60.1282, 18.6435), 
    "Norway": (60.4720, 8.4689), "Denmark": (56.2639, 9.5018), 
    "Finland": (61.9241, 25.7482), "Ireland": (53.1424, -7.6921), 
    "Portugal": (39.3999, -8.2245), "Bulgaria": (42.7339, 25.4858), 
    "Croatia": (45.1000, 15.2000), "Serbia": (44.0165, 21.0059), 
    "Slovakia": (48.6690, 19.6990), "Belarus": (53.7098, 27.9534), 
    "Lithuania": (55.1694, 23.8813), "Latvia": (56.8796, 24.6032), 
    "Estonia": (58.5953, 25.0136), "Slovenia": (46.1512, 14.9955), 
    "Bosnia And Herzegovina": (43.9159, 17.6791), "Moldova Republic Of": (47.4116, 28.3699), 
    "Rep. Of Macedonia": (41.6086, 21.7453), "Albania": (41.1533, 20.1683), 
    "Luxembourg": (49.8153, 6.1296), "Iceland": (64.9631, -19.0208), 
    "Malta": (35.9375, 14.3754), "Montenegro": (42.7087, 19.3744), 
    "Andorra": (42.5063, 1.5218), "San Marino": (43.9424, 12.4578), 
    "Kosovo": (42.6026, 20.9030), "United States": (37.0902, -95.7129), 
    "Canada": (56.1304, -106.3468), "Mexico": (23.6345, -102.5528), 
    "Brazil": (-14.2350, -51.9253), "Argentina": (-38.4161, -63.6167), 
    "Chile": (-35.6751, -71.5430), "Peru": (-9.1900, -75.0152), 
    "Colombia": (4.5709, -74.2973), "Ecuador": (-1.8312, -78.1834), 
    "Venezuela": (9.1899, -69.8395), "Uruguay": (-32.5228, -55.7658), 
    "Paraguay": (-23.4425, -58.4438), "Bolivia": (-16.2902, -63.5887), 
    "Guyana": (4.8604, -58.9302), "Suriname": (3.9193, -56.0278), 
    "Panama": (8.5380, -80.7821), "Costa Rica": (9.7489, -83.7534), 
    "Guatemala": (15.7835, -90.2308), "Honduras": (15.2000, -86.2419), 
    "El Salvador": (13.7942, -88.8965), "Nicaragua": (12.8654, -85.2072), 
    "Dominican Republic": (18.7357, -70.1627), "Cuba": (21.5218, -77.7812), 
    "Haiti": (18.9712, -72.2852), "Jamaica": (18.1096, -77.2975), 
    "Puerto Rico": (18.2208, -66.5901), "Egypt": (26.8206, 30.8025), 
    "South Africa": (-30.5595, 22.9375), "Nigeria": (9.0820, 8.6753), 
    "Morocco": (31.7917, -7.0926), "Algeria": (28.0339, 1.6596), 
    "Kenya": (-0.0236, 37.9062), "Ghana": (7.9465, -1.0232), 
    "Tanzania United Rep. Of": (-6.3690, 34.8888), "Uganda": (1.3733, 32.2903), 
    "Senegal": (14.4974, -14.4524), "Cote Divoire": (7.5400, -5.5471), 
    "Cameroon": (3.8480, 11.5021), "Angola": (-11.2027, 17.8739), 
    "Mozambique": (-18.6657, 35.5296), "Madagascar": (-18.7669, 46.8691), 
    "Mauritius": (-20.3484, 57.5522), "Zimbabwe": (-19.0154, 29.1549), 
    "Zambia": (-13.1339, 27.8493), "Democratic Rep. Of The Congo": (-4.0383, 21.7587), 
    "Libyan Arab Jamahiriya": (26.3351, 17.2283), "Tunisia": (33.8869, 9.5375), 
    "Sudan": (12.8628, 30.2176), "Ethiopia": (9.1450, 40.4897), 
    "Australia": (-25.2744, 133.7751), "New Zealand": (-40.9006, 174.8860), 
    "Papua New Guinea": (-6.3149, 143.9555), "Fiji": (-17.7134, 178.0650), 
    "Solomon Islands": (-9.6457, 160.1562), "Vanuatu": (-15.3767, 166.9592), 
    "Samoa": (-13.7590, -172.1046), "Guam": (13.4443, 144.7937),
    "Negara lainnya": (0.0000, 0.0000)
}

def _ambil_koordinat(nama_negara):
    if not nama_negara: return (0, 0)
    if nama_negara in KOORDINAT_NEGARA: return KOORDINAT_NEGARA[nama_negara]
    for k, v in KOORDINAT_NEGARA.items():
        if k.lower() in nama_negara.lower() or nama_negara.lower() in k.lower():
            return v
    return (0, 0)

# PEMROSESAN DATA JARINGAN
def _siap(tahun, ambang_usd):
    """Menyiapkan edge list komoditas-negara di atas ambang batas (syarat filter edge)."""
    cn = data.chapter_negara_tahun()
    d = cn[cn["tahun"] == tahun].copy()
    d = d[d["nilai_usd"] >= ambang_usd]
    
    G = nx.Graph()
    for _, baris in d.iterrows():
        komoditas = f"{baris['nama_chapter'][:25]}..." if len(baris['nama_chapter']) > 25 else baris['nama_chapter']
        negara = baris['negara']
        
        G.add_node(komoditas, tipe="komoditas")
        G.add_node(negara, tipe="negara")
        G.add_edge(komoditas, negara, weight=baris["nilai_usd"])
        
    return G, d

# VISUALISASI FORCE-DIRECTED GRAPH
def _fig_network_force(G, node_fokus):
    degree_cent = nx.degree_centrality(G)
    
    G_layout = nx.Graph()
    for u, v in G.edges():
        G_layout.add_edge(u, v, weight=1.0)
        
    pusat_dummy = "GRAVITASI_DUMMY"
    G_layout.add_node(pusat_dummy)
    for node in G.nodes():
        G_layout.add_edge(pusat_dummy, node, weight=0.01) 
        
    pos = nx.spring_layout(G_layout, weight='weight', k=0.5, iterations=100, seed=42)
    del pos[pusat_dummy]
    
    max_weight = max([d['weight'] for u, v, d in G.edges(data=True)]) if G.edges() else 1
    fig = go.Figure()
    
    # 1. Garis Edge
    for u, v, d in G.edges(data=True):
        if node_fokus != "Semua" and u != node_fokus and v != node_fokus:
            warna, tebal = "rgba(200,200,200,0.05)", 0.5
        else:
            warna = "rgba(150,150,150,0.2)" if node_fokus == "Semua" else "#009E73"
            tebal = max(0.5, (d['weight'] / max_weight) * 5) if node_fokus == "Semua" else max(1.5, (d['weight'] / max_weight) * 8)
            
        fig.add_trace(go.Scatter(
            x=[pos[u][0], pos[v][0], None], y=[pos[u][1], pos[v][1], None],
            line=dict(width=tebal, color=warna),
            mode='lines', hoverinfo='none', showlegend=False
        ))

    # 2. Titik Node
    node_x, node_y, node_text, node_size, node_color, node_labels = [], [], [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x); node_y.append(y)
        
        cent_score = degree_cent[node]
        ukuran_node = 10 + (cent_score * 50)
        node_size.append(ukuran_node)
        
        tipe = G.nodes[node]['tipe']
        node_color.append("#009E73" if tipe == "komoditas" else "#E69F00")
        
        mitra = list(G.neighbors(node))
        node_text.append(f"<b>{node}</b><br>Mitra dagang: {len(mitra)}<br>Sentralitas (Degree): {cent_score:.3f}")
        
        if ukuran_node > 15 or len(G.nodes) < 25:
            node_labels.append(node)
        else:
            node_labels.append("")

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y, 
        mode='markers+text',
        text=node_labels, 
        textposition="top center",
        hovertext=node_text, hoverinfo='text',
        marker=dict(size=node_size, color=node_color, line=dict(width=1.5, color='#FFFFFF')),
        textfont=dict(size=10, color=style.TEKS), showlegend=False
    ))

    fig.update_layout(
        height=650, margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor="#FFFFFF", 
        plot_bgcolor="#FFFFFF",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        font=dict(family=FONT, color=style.TEKS)
    )
    return fig

# GEO-NETWORK MAP
def _fig_network_geo(G, node_fokus):
    degree_cent = nx.degree_centrality(G)
    max_weight = max([d['weight'] for u, v, d in G.edges(data=True)]) if G.edges() else 1
    
    fig = go.Figure()
    komoditas_nodes = [n for n, attr in G.nodes(data=True) if attr['tipe'] == 'komoditas']
    sudut = np.linspace(0, 2 * np.pi, len(komoditas_nodes), endpoint=False)
    koordinat_komoditas = {}
    
    for i, kom in enumerate(komoditas_nodes):
        koordinat_komoditas[kom] = (-12 + 8 * np.sin(sudut[i]), 100 + 8 * np.cos(sudut[i]))

    for u, v, d in G.edges(data=True):
        if G.nodes[u]['tipe'] == 'komoditas':
            kom, neg = u, v
        else:
            kom, neg = v, u
            
        lat_kom, lon_kom = koordinat_komoditas[kom]
        lat_neg, lon_neg = _ambil_koordinat(neg)
        if (lat_neg, lon_neg) == (0, 0): continue
            
        if node_fokus != "Semua" and u != node_fokus and v != node_fokus:
            warna, tebal = "rgba(200,200,200,0.1)", 0.5
        else:
            warna = "rgba(150,150,150,0.4)" if node_fokus == "Semua" else "#009E73"
            tebal = max(0.5, (d['weight'] / max_weight) * 5) if node_fokus == "Semua" else max(2, (d['weight'] / max_weight) * 8)

        fig.add_trace(go.Scattergeo(
            lat=[lat_kom, lat_neg], lon=[lon_kom, lon_neg],
            mode='lines', line=dict(width=tebal, color=warna),
            hoverinfo='none', showlegend=False
        ))

    for node, attr in G.nodes(data=True):
        cent_score = degree_cent[node]
        ukuran = 6 + (cent_score * 40)
        mitra = list(G.neighbors(node))
        teks_hover = f"<b>{node}</b><br>Mitra dagang: {len(mitra)}<br>Sentralitas: {cent_score:.3f}"
        
        if attr['tipe'] == 'komoditas':
            lat, lon = koordinat_komoditas[node]
            warna = "#009E73"
        else:
            lat, lon = _ambil_koordinat(node)
            if (lat, lon) == (0, 0): continue
            warna = "#E69F00"

        opacity = 1.0 if node_fokus == "Semua" or node == node_fokus or node in mitra else 0.2

        fig.add_trace(go.Scattergeo(
            lat=[lat], lon=[lon],
            mode='markers+text' if (attr['tipe'] == 'komoditas' or ukuran > 15) else 'markers',
            text=[node] if attr['tipe'] == 'komoditas' else [""],
            textposition="bottom center",
            hovertext=teks_hover, hoverinfo='text',
            marker=dict(size=ukuran, color=warna, line=dict(width=1, color='#FFFFFF'), opacity=opacity),
            textfont=dict(size=9, color=style.TEKS), showlegend=False
        ))

    fig.update_layout(
        height=650, margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor="#FFFFFF", 
        plot_bgcolor="#FFFFFF",
        geo=dict(showland=True, landcolor="#F8F9FA", countrycolor="#D3D3D3",
                 showocean=True, oceancolor="#E8F4F8", projection_type="natural earth"),
        font=dict(family=FONT, color=style.TEKS)
    )
    return fig

# ADJACENCY MATRIX
def _fig_matrix(df):
    pivot = df.pivot(index='nama_chapter', columns='negara', values='nilai_usd').fillna(0)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns,
        y=[c[:30] + "..." if len(c) > 30 else c for c in pivot.index],
        colorscale="Greens",
        hovertemplate="Komoditas: %{y}<br>Negara: %{x}<br>Nilai Ekspor: %{customdata}<extra></extra>",
        customdata=pivot.values.astype(float)
    ))
    fig.update_layout(
        height=600, margin=dict(l=10, r=10, t=30, b=80),
        xaxis=dict(tickangle=45, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
        font=dict(family=FONT, color=style.TEKS),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig

# RENDER UTAMA JARINGAN
def render_jaringan(tahun: int):
    st.subheader(f"Struktur Jaringan Perdagangan Global {tahun}")
    st.caption("Menganalisis keterhubungan (Bipartite) antara kelompok komoditas dan negara mitra.")

    col_kontrol, col_plot = st.columns([1, 2.5], gap="large")

    with col_kontrol:
        # --- FILTER KONTROL ---
        with st.container(border=True):
            st.markdown("**Pengaturan Filter**")
            
            ambang_juta = st.slider(
                "Ambang Nilai (Juta USD)", 
                min_value=1.0, max_value=500.0, value=20.0, step=5.0
            )
                        
            ambang_usd = ambang_juta * 1_000_000
            
            G, df_filtered = _siap(tahun, ambang_usd)
            jml_node = G.number_of_nodes()
                
            st.success(f"{jml_node} node & {G.number_of_edges()} rute")
            
        with st.expander("Fungsi Filter", expanded=False):
            st.write("Menetapkan batas minimum nilai ekspor. Rute bernilai di bawah batas akan disembunyikan agar terhindar dari kepadatan (clutter).")

        # --- INTERAKSI ---
        with st.container(border=True):
            st.markdown("**Interaksi Visual**")
            
            daftar_node = ["Semua"] + sorted(list(G.nodes()))
            node_fokus = st.selectbox(
                "Sorot Hubungan:", 
                daftar_node
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            pakai_peta = st.toggle("Gunakan Peta Geospasial", value=False)
        
            jenis_layout = "Peta Geospasial" if pakai_peta else "Force-Directed"
            
        with st.expander("Cara Pakai Interaksi", expanded=False):
            st.write("Pilih komoditas/negara spesifik untuk menyalakan jalurnya. Aktifkan toggle untuk mengubah proyeksi ke lokasi asli.")

    with col_plot:
        if jenis_layout == "Force-Directed":
            st.plotly_chart(_fig_network_force(G, node_fokus), use_container_width=True)
        else:
            st.plotly_chart(_fig_network_geo(G, node_fokus), use_container_width=True)
        style.chart_footer("USD")

    # --- Panduan Membaca Graf Keterkaitan ---
    with st.expander("Panduan Membaca Graf Keterkaitan", expanded=False):
        st.markdown("""
        - **Hijau:** Kelompok Komoditas | **Oranye:** Negara Tujuan
        - **Ukuran Titik:** Sentralitas (*Degree Centrality*). Semakin besar titiknya, semakin banyak mitranya. Arahkan kursor ke titik untuk melihat jumlah mitra dan nilai sentralitasnya.
        - **Garis Penghubung:** Menggambarkan aliran keterkaitan antara komoditas dengan negara mitra Ekspor
        - **Hubungan:** Menjelaskan keterkaitan antara komoditas dan negara mitra.
        """)

    st.markdown("---")

    st.markdown("**Tampilan Adjacency Matrix**")
    st.caption("Matriks hubungan komoditas dan negara. Semakin gelap/hijau warna sel, semakin tinggi nilai transaksinya.")
    
    if not df_filtered.empty:
        st.plotly_chart(_fig_matrix(df_filtered), use_container_width=True)
        style.chart_footer("USD")
    else:
        st.info("Tidak ada data yang memenuhi ambang batas filter saat ini.")
        
    # --- Panduan Membaca Matriks ---
    with st.expander("Panduan Membaca Matriks", expanded=False):
        st.markdown("""
        - **Baris:** Kelompok komoditas.
        - **Kolom:** Negara mitra dagang.
        - Titik potong antar baris dan kolom menunjukkan keberadaan jalur perdagangan.
        """)