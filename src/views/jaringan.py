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

KOORDINAT_PELABUHAN = {
    "ABDULRACHMAN SALEH (U)": (-7.9266, 112.7145), "ACHMAD YANI (U)": (-6.9715, 110.3742),
    "ADI SUCIPTO (U)": (-7.7882, 110.4317), "AMBON": (-3.6954, 128.1814),
    "AMURANG": (1.1772, 124.5800), "ANGGREK": (0.8667, 122.7000),
    "ARUK": (1.4900, 109.1200), "ATAMBUA (U)": (-9.0753, 124.9053),
    "ATAPUPU": (-9.0000, 124.8500), "BADAS SUMBAWA": (-8.5500, 117.3500),
    "BAGAN SIAPI-API": (2.1547, 100.8111), "BALIKPAPAN": (-1.2654, 116.8312),
    "BANDARA UDARA INTERNASIONAL (LOMBOK)": (-8.7573, 116.2767),
    "BANJARMASIN": (-3.3194, 114.5900), "BATAM ISLAND": (1.0456, 104.0305),
    "BATU AMPAR": (1.1667, 104.0000), "BEKAPAI": (-0.9500, 117.4500),
    "BELAKANG PADANG": (1.1833, 103.9333), "BELAWAN": (3.7833, 98.7000),
    "BELITUNG": (-2.7400, 107.6500), "BENETE": (-8.9167, 116.8167),
    "BENGKALIS": (1.4667, 102.1167), "BENGKAYANG": (0.9000, 109.4800),
    "BENGKULU": (-3.8000, 102.2500), "BENOA/LOLOAN": (-8.7500, 115.2167),
    "BERAU (U)": (2.1553, 117.4319), "BITUNG": (1.4440, 125.1917),
    "BLANG BINTANG (U)": (5.5236, 95.4204), "BONTANG": (0.1333, 117.5000),
    "BONTHAN BAY SULAWESI": (-5.5500, 119.9500), "BUNYU": (3.4667, 117.8333),
    "CALANG": (4.6000, 95.6000), "CELUKAN BAWANG": (-8.1667, 114.8000),
    "CIWANDAN": (-5.9833, 106.0000), "DONGGALA (U)": (-0.6700, 119.7400),
    "DUMAI": (1.6833, 101.4500), "ENDE/IPI": (-8.8500, 121.6500),
    "ENTIKONG": (0.9833, 110.3333), "FAK-FAK": (-2.9253, 132.2956),
    "FRANS KASIEPO (U)": (-1.1900, 136.1080), "GORONTALO": (0.5333, 123.0500),
    "GRESIK": (-7.1667, 112.6500), "HALIM PERDANA KUSUMA (U)": (-6.2666, 106.8910),
    "HANG NADIM (U)": (1.1210, 104.1190), "HASANUDDIN (U)": (-5.0616, 119.5540),
    "HUSEIN SASTRANEGARA (U)": (-6.9006, 107.5763), "ILLAGA (U)": (-3.9764, 137.6228),
    "JAGOIBABANG": (1.0000, 109.9500), "JAKARTA / PASAR IKAN": (-6.1275, 106.8089),
    "JALALUDDIN(U)": (0.6371, 122.8497), "JAMBI": (-1.6000, 103.6000),
    "JAYAPURA": (-2.5333, 140.7167), "JAYAPURA / SENTANI (U)": (-2.5769, 140.5163),
    "JUANDA (U)-SURABAYA": (-7.3798, 112.7869), "JUATA TARAKAN": (3.3333, 117.5500),
    "KABIL/PANAU": (1.0667, 104.1167), "KALABAHI": (-8.2167, 124.5167),
    "KALIANGET": (-7.0500, 113.9300), "KARIANGAU": (-1.1667, 116.8000),
    "KENDARI": (-3.9667, 122.5833), "KENDAWANGAN": (-2.5333, 110.2000),
    "KIJANG": (0.9000, 104.6000), "KOKONAO (U)": (-4.7000, 136.4000),
    "KOTABARU": (-3.2333, 116.2167), "KOTABARU (U)": (-3.2333, 116.2167),
    "KUALA ENOK": (-0.1700, 103.1200), "KUALA GAUNG": (-0.2000, 103.4000),
    "KUALA LANGSA": (4.5000, 98.0000), "KUALA NAMU INTERNATIONAL AIRPORT (U)": (3.6422, 98.8853),
    "KUALA TANJUNG": (3.3500, 99.4667), "KUALA TUNGKAL": (-0.8167, 103.4667),
    "KUANDANG": (0.8833, 122.8000), "KUMAI": (-2.7333, 111.7333),
    "KUPANG / EL-TARI (U)": (-10.1716, 123.6711), "LABUANBAJO (U)": (-8.4867, 119.8890),
    "LHOK SEUMAWE": (5.1833, 97.1333), "LINGKAS TARAKAN": (3.4500, 117.6500),
    "LIRUNG": (3.8000, 126.7000), "LOBAM": (1.1000, 104.5000),
    "LUWUK": (-0.9500, 122.7900), "MAKASSAR": (-5.1333, 119.4000),
    "MAMUJU": (-2.6786, 118.8883), "MANADO": (1.4833, 124.8333),
    "MANGGAR-BELITUNG": (-2.8667, 108.2833), "MASAMBA (U)": (-2.5500, 120.3300),
    "MATARAM / SELAPARANG (U)": (-8.5600, 116.0950), "MAUMERE": (-8.6167, 122.2167),
    "MELANGGUANE (U)": (4.0000, 126.7000), "MEMPAWAH": (0.3667, 109.0000),
    "MERAK": (-5.9333, 106.0167), "MERAUKE": (-8.4667, 140.3833),
    "MUARA BERAU": (-0.5500, 117.2000), "MUARA SABAK": (-1.1000, 103.8500),
    "MUSI RIVER/BOOM BARU": (-2.9833, 104.7667), "MUTIARA-PALU (U)": (-0.9185, 119.9100),
    "NANGA BADAU": (1.1000, 111.5000), "NATUNA RANAI": (3.9000, 108.4000),
    "NGURAH RAI(U)": (-8.7482, 115.1675), "NIPAH PANJANG": (-1.0000, 104.2000),
    "NUNUKAN": (4.1333, 117.6500), "OBI ISLAND": (-1.5000, 127.6000),
    "PADANG / TABING (U)": (-0.8750, 100.3500), "PADANG KEMILING (U)": (-3.8600, 102.3400),
    "PADANG/TL.BAYUR": (-1.0000, 100.3700), "PALEMBANG - PLAJU": (-3.0000, 104.8000),
    "PALEMBANG-KERTAPATI": (-2.9900, 104.7800), "PALIMANAN": (-6.7000, 108.4000),
    "PALMERAH/SULTAN THAHA (U)": (-1.6380, 103.6440), "PAMANUKAN JAVA": (-6.2800, 107.8000),
    "PANARU-PALANGKARAYA (U)": (-2.2250, 113.9430), "PANGKAL BALAM": (-2.1000, 106.1000),
    "PANGKAL PINANG (U)": (-2.1622, 106.1390), "PANGKALAN AIR (U)": (-2.7052, 111.6733),
    "PANGKALAN BUN": (-2.7052, 111.6733), "PANIPAHAN": (2.1000, 100.8500),
    "PANJANG": (-5.4667, 105.3167), "PANTOLOAN": (-0.7000, 119.8500),
    "PANTOLOAN SV": (-0.7000, 119.8500), "PATTIMURA/LAHA (U)": (-3.7103, 128.0889),
    "PEKAN BARU": (0.5333, 101.4500), "PEKANBARU (RUMBAI)": (0.6000, 101.4000),
    "PEMANUKAN": (-6.2800, 107.8000), "PERAWANG SUMATRA": (0.6000, 102.0000),
    "PONTIANAK": (-0.0167, 109.3333), "PROBOLINGGO": (-7.7167, 113.2167),
    "PULAU BAAI": (-3.9000, 102.3000), "PULAU LAUT": (-3.7000, 116.2000),
    "PULAU SAMBU": (1.0000, 103.9000), "RENGAT": (-0.4000, 102.5000),
    "SAM RATULANGI (U)": (1.5493, 124.9260), "SAMARINDA": (-0.5000, 117.1500),
    "SAMPIT": (-2.5333, 112.9500), "SAMSUDIN NOOR (U)": (-3.4424, 114.7625),
    "SANANA (U)": (-2.0800, 125.9700), "SANGKULIRANG": (0.9000, 117.9700),
    "SATUI": (-3.8000, 115.4000), "SEI NYAMUK": (4.1000, 117.8000),
    "SEKUPANG": (1.1000, 104.0000), "SELAT PANJANG": (1.0000, 102.7000),
    "SEPINGGAN (U)": (-1.2683, 116.8943), "SERANG": (-6.1000, 106.1500),
    "SERASAN": (2.5000, 109.0000), "SIAK SRI INDRAPURA": (0.8000, 102.0000),
    "SIAK YECHIL RIAU": (0.8000, 102.0000), "SIMPANG TIGA (U)": (0.4608, 101.4445),
    "SINGKAWANG": (0.9000, 108.9800), "SINGKEP- DABO": (-0.5000, 104.5700),
    "SINGKEP/DABO (U)": (-0.4797, 104.5792), "SINTETE": (1.1000, 109.1000),
    "SM. BADARUDDIN (U)": (-2.8983, 104.6998), "SOEKARNO-HATTA (U)": (-6.1256, 106.6559),
    "SOLO/JEBRES/ADI SUMARMO (U)": (-7.5160, 110.7570), "SORONG": (-0.8833, 131.2500),
    "SORONG / JEFMAN (U)": (-0.9264, 131.1210), "SUNGAI GUNTUNG": (-0.1700, 102.9700),
    "SUPADIO (U)": (-0.1507, 109.4040), "SURABAYA (PTT)": (-7.2000, 112.7300),
    "TAHUNA": (3.6000, 125.5000), "TANAH GROGOT": (-1.9000, 116.2000),
    "TANJUNG BALAI ASAHAN": (2.9700, 99.8000), "TANJUNG BALAI KARIMUN": (1.0000, 103.4300),
    "TANJUNG BARA KL": (0.5500, 117.6000), "TANJUNG BATU RIAU": (0.8500, 103.4000),
    "TANJUNG BERINGIN": (3.6000, 99.0000), "TANJUNG EMAS": (-6.9500, 110.4200),
    "TANJUNG KEDABU": (1.1000, 102.5000), "TANJUNG MEDANG": (1.9000, 101.6000),
    "TANJUNG PANDAN": (-2.7500, 107.6500), "TANJUNG PERAK": (-7.2000, 112.7333),
    "TANJUNG PINANG": (0.9167, 104.4500), "TANJUNG PRIOK": (-6.1000, 106.8800),
    "TANJUNG REDEP": (2.1500, 117.5000), "TANJUNG SAMAK": (1.0000, 102.7000),
    "TANJUNG UBAN": (1.0700, 104.2000), "TARAHAN": (-5.5000, 105.3000),
    "TARAKAN (U)": (3.3267, 117.5656), "TARJUN": (-3.3000, 116.2000),
    "TELOK MELANO": (-1.4000, 109.7000), "TEMBILAHAN": (-0.3167, 103.1500),
    "TENAU": (-10.1833, 123.5333), "TEREMPA": (3.2000, 106.2000),
    "TERNATE": (0.7833, 127.3833), "TOBELO": (1.7333, 128.0000),
    "TUAL": (-5.6333, 132.7500), "UJUNGPANDANG": (-5.1300, 119.4100),
    "WOLTER MONGINSIDI (U)": (-4.0816, 122.4180),
    "YOGYAKARTA INTERNATIONAL AIRPORT": (-7.9000, 110.0500),
}

def _ambil_koordinat_pelabuhan(nama):
    return KOORDINAT_PELABUHAN.get(str(nama).strip().upper(), (0, 0))

def _ambil_koordinat(nama_negara):
    if not nama_negara: return (0, 0)
    if nama_negara in KOORDINAT_NEGARA: return KOORDINAT_NEGARA[nama_negara]
    for k, v in KOORDINAT_NEGARA.items():
        if k.lower() in nama_negara.lower() or nama_negara.lower() in k.lower():
            return v
    return (0, 0)

# PEMROSESAN DATA JARINGAN
def _siap(tahun, ambang_usd):
    pn = data.pelabuhan_detail().copy()
    pn["pelabuhan"] = pn["pelabuhan"].str.strip().str.upper()
    d = pn[pn["tahun"] == tahun].copy()
    d = d.groupby(["pelabuhan", "negara"], as_index=False)["nilai_usd"].sum()
    d = d[d["nilai_usd"] >= ambang_usd]

    G = nx.Graph()
    for _, baris in d.iterrows():
        pelabuhan, negara = baris["pelabuhan"], baris["negara"]
        G.add_node(pelabuhan, tipe="pelabuhan")
        G.add_node(negara, tipe="negara")
        G.add_edge(pelabuhan, negara, weight=baris["nilai_usd"])

    return G, d

# VISUALISASI FORCE-DIRECTED GRAPH
def _fig_network_force(G, node_fokus):
    degree_cent = nx.get_node_attributes(G, "cent") or nx.degree_centrality(G)
    
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
        node_color.append("#009E73" if tipe == "pelabuhan" else "#E69F00")
        
        mitra = list(G.neighbors(node))
        node_text.append(f"<b>{node}</b><br>Mitra dagang: {G.nodes[node].get('jml_mitra', len(mitra))}<br>Sentralitas (Degree): {cent_score:.3f}")
        
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
    degree_cent = nx.get_node_attributes(G, "cent") or nx.degree_centrality(G)
    max_weight = max([d['weight'] for u, v, d in G.edges(data=True)]) if G.edges() else 1

    fig = go.Figure()

    for u, v, d in G.edges(data=True):
        if G.nodes[u]['tipe'] == 'pelabuhan':
            pel, neg = u, v
        else:
            pel, neg = v, u

        lat_pel, lon_pel = _ambil_koordinat_pelabuhan(pel)
        lat_neg, lon_neg = _ambil_koordinat(neg)
        if (lat_pel, lon_pel) == (0, 0) or (lat_neg, lon_neg) == (0, 0):
            continue

        if node_fokus != "Semua" and u != node_fokus and v != node_fokus:
            warna, tebal = "rgba(200,200,200,0.1)", 0.5
        else:
            warna = "rgba(150,150,150,0.4)" if node_fokus == "Semua" else "#009E73"
            tebal = max(0.5, (d['weight'] / max_weight) * 5) if node_fokus == "Semua" else max(2, (d['weight'] / max_weight) * 8)

        fig.add_trace(go.Scattergeo(
            lat=[lat_pel, lat_neg], lon=[lon_pel, lon_neg],
            mode='lines', line=dict(width=tebal, color=warna),
            hoverinfo='none', showlegend=False
        ))

    for node, attr in G.nodes(data=True):
        cent_score = degree_cent[node]
        ukuran = 6 + (cent_score * 40)
        mitra = list(G.neighbors(node))
        teks_hover = f"<b>{node}</b><br>Mitra dagang: {G.nodes[node].get('jml_mitra', len(mitra))}<br>Sentralitas: {cent_score:.3f}"

        if attr['tipe'] == 'pelabuhan':
            lat, lon = _ambil_koordinat_pelabuhan(node)
            warna = "#009E73"
        else:
            lat, lon = _ambil_koordinat(node)
            warna = "#E69F00"
        if (lat, lon) == (0, 0): continue

        opacity = 1.0 if node_fokus == "Semua" or node == node_fokus or node in mitra else 0.2

        fig.add_trace(go.Scattergeo(
            lat=[lat], lon=[lon],
            mode='markers+text' if (attr['tipe'] == 'pelabuhan' or ukuran > 15) else 'markers',
            text=[node] if attr['tipe'] == 'pelabuhan' else [""],
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
    pivot = df.pivot_table(index='pelabuhan', columns='negara', values='nilai_usd', aggfunc='sum').fillna(0)
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns, y=list(pivot.index),
        colorscale="Greens",
        hovertemplate="Pelabuhan/Bandara: %{y}<br>Negara: %{x}<br>Nilai Ekspor: %{customdata}<extra></extra>",
        customdata=pivot.values.astype(float)
    ))
    return fig

def _css_kontrol():
    st.markdown("""<style>
    .st-key-kontrol_filter, .st-key-kontrol_sorot{
        background:#FFFFFF; border:1px solid #D5E3DF; border-radius:12px;
        padding:1.1rem 1.2rem !important; gap:.8rem !important;
        box-shadow:0 1px 4px rgba(0,0,0,.05); overflow:visible !important;
    }
        .st-key-kontrol_filter, .st-key-kontrol_sorot{
        padding-bottom:1.4rem !important;
    }
    .st-key-kontrol_filter > div, .st-key-kontrol_sorot > div{
        overflow:visible !important;
    }
    .st-key-kontrol_filter [data-testid="stElementContainer"],
    .st-key-kontrol_sorot [data-testid="stElementContainer"]{
        overflow:visible !important;
    }
    .st-key-kontrol_filter p strong, .st-key-kontrol_sorot p strong{
        font-size:.8rem; text-transform:uppercase; letter-spacing:.6px; color:#007656;
    }

    .st-key-kontrol_sorot [data-testid="stRadio"] div[role="radiogroup"]{
        display:flex !important; flex-direction:row !important; flex-wrap:nowrap !important;
        justify-content:stretch !important; gap:4px !important; width:100% !important;
        background:#F1F5F4; border:1px solid #D5E3DF; border-radius:10px;
        padding:4px; margin:0 !important;
    }
    .st-key-kontrol_sorot [data-testid="stRadio"] div[role="radiogroup"] > label{
        flex:1 1 0 !important; min-width:0; display:flex !important;
        justify-content:center !important; margin:0 !important;
        padding:7px 2px !important; border-radius:7px; cursor:pointer;
        transition:background .2s;
    }
    .st-key-kontrol_sorot [data-testid="stRadio"] label > div:first-child{display:none !important;}
    .st-key-kontrol_sorot [data-testid="stRadio"] label p{
        margin:0 !important; font-size:.82rem; font-weight:600; color:#202124;
        white-space:nowrap; text-align:center;
    }
    .st-key-kontrol_sorot [data-testid="stRadio"] label:hover{background:#E1EFEA;}
    .st-key-kontrol_sorot [data-testid="stRadio"] label:has(input:checked){
        background:#009E73; box-shadow:0 1px 3px rgba(0,0,0,.15);
    }
    .st-key-kontrol_sorot [data-testid="stRadio"] label:has(input:checked) p{color:#FFFFFF;}

    .st-key-kontrol_sorot hr{margin:.2rem 0 !important;}
    
    .st-key-kontrol_sorot [data-testid="stRadio"] div[role="radiogroup"]{
        gap:2px !important; padding:3px !important; border-radius:999px;
    }
    .st-key-kontrol_sorot [data-testid="stRadio"] div[role="radiogroup"] > label{
        flex:1 1 auto !important; justify-content:center !important;
        align-items:center !important; gap:0 !important;
        padding:6px 14px !important; border-radius:999px;
        min-height:0 !important;
    }
    .st-key-kontrol_sorot [data-testid="stRadio"] label > div:first-child{
        display:none !important; width:0 !important; margin:0 !important; padding:0 !important;
    }
    .st-key-kontrol_sorot [data-testid="stRadio"] label > div:last-child{
        margin:0 !important; padding:0 !important; width:auto !important;
    }
    .st-key-kontrol_sorot [data-testid="stRadio"] label p{
        font-size:.85rem !important; line-height:1.2 !important;
        text-align:center !important; margin:0 !important;
    }
    .st-key-kontrol_sorot [data-testid="stRadio"] label:has(input:checked){
        box-shadow:0 1px 3px rgba(0,0,0,.18);
    }
    </style>""", unsafe_allow_html=True)
    
# RENDER UTAMA JARINGAN
def render_jaringan(tahun: int):
    st.subheader(f"Struktur Jaringan Perdagangan Global {tahun}")
    st.caption("Menganalisis keterhubungan (Bipartite) antara pelabuhan/bandara ekspor dengan negara mitra.")

    col_kontrol, col_plot = st.columns([1, 2.5], gap="large")

    with col_kontrol:
        _css_kontrol() 
        # --- FILTER ---
        with st.container(key="kontrol_filter"):
            st.markdown("**Pengaturan Filter**")

            ambang_juta = st.slider(
                "Ambang Nilai (Juta USD)",
                min_value=5, max_value=500, value=20, step=5, format="%d",
            )
            ambang_usd = ambang_juta * 1_000_000

            G, df_filtered = _siap(tahun, ambang_usd)

            kotak = ("flex:1;background:#E8F5F1;border:1px solid #C6E7DE;"
                     "border-radius:10px;padding:10px 14px;")
            angka = "font-size:1.5rem;font-weight:800;color:#007656;line-height:1.1;"
            label = ("font-size:.7rem;font-weight:700;text-transform:uppercase;"
                     "letter-spacing:.6px;color:#202124;margin-top:2px;")
            st.markdown(
                f'<div style="display:flex;gap:10px;margin:.4rem 0 .6rem;">'
                f'<div style="{kotak}"><div style="{angka}">{G.number_of_nodes()}</div>'
                f'<div style="{label}">Node</div></div>'
                f'<div style="{kotak}"><div style="{angka}">{G.number_of_edges()}</div>'
                f'<div style="{label}">Rute</div></div>'
                f'</div>', unsafe_allow_html=True)

        with st.expander("Fungsi Filter", expanded=False):
            st.write("Menetapkan batas minimum nilai ekspor. Rute bernilai di bawah batas akan disembunyikan agar terhindar dari kepadatan (clutter).")

        # --- INTERAKSI ---
        with st.container(key="kontrol_sorot"):
            st.markdown("**Interaksi Visual**")

            st.caption("Sorot hubungan")
            jenis_sorot = st.radio(
                "Sorot Hubungan:",
                ["Semua", "Pelabuhan", "Negara"],
                horizontal=True,
                label_visibility="collapsed",
            )

            node_fokus = "Semua"
            if jenis_sorot != "Semua":
                tipe = jenis_sorot.lower()
                pilihan = sorted(n for n, a in G.nodes(data=True) if a["tipe"] == tipe)
                if pilihan:
                    node_fokus = st.selectbox(f"Pilih {tipe}:", pilihan)
                else:
                    st.info("Tidak ada node pada ambang ini.")

            st.divider()
            fokus_saja = st.toggle(
                "Hanya yang disorot",
                value=True,
                disabled=(node_fokus == "Semua"),
                help="Aktif: graf hanya berisi node terpilih dan mitranya. Nonaktif: semua node tetap tampil, hanya jalurnya yang menyala.",
            )
            pakai_peta = st.toggle("Gunakan Peta Geospasial", value=False)
            jenis_layout = "Peta Geospasial" if pakai_peta else "Force-Directed"
            
        with st.expander("Cara Pakai Interaksi", expanded=False):
            st.write("Pilih pelabuhan/bandara atau negara spesifik untuk melihat jalurnya. Aktifkan toggle untuk mengubah proyeksi ke lokasi asli. Aktifkan toggle 'Hanya yang disorot' untuk menyederhanakan graf.")

    with col_plot:
        nx.set_node_attributes(G, nx.degree_centrality(G), "cent")
        nx.set_node_attributes(G, dict(G.degree()), "jml_mitra")

        if node_fokus != "Semua" and fokus_saja:
            G_tampil = G.subgraph([node_fokus, *G.neighbors(node_fokus)]).copy()
            st.caption(f"**{node_fokus}** terhubung ke {G.degree(node_fokus)} mitra.")
        else:
            G_tampil = G

        if jenis_layout == "Force-Directed":
            st.plotly_chart(_fig_network_force(G_tampil, node_fokus), use_container_width=True)
        else:
            st.plotly_chart(_fig_network_geo(G_tampil, node_fokus), use_container_width=True)
        style.chart_footer("USD")

    # --- Panduan Membaca Graf Keterkaitan ---
    with st.expander("Panduan Membaca Graf Keterkaitan", expanded=False):
        st.markdown("""
        - **Hijau:** Pelabuhan/Bandara Ekspor | **Oranye:** Negara Tujuan
        - **Ukuran Titik:** Sentralitas (*Degree Centrality*). Semakin besar titiknya, semakin banyak mitranya. Arahkan kursor ke titik untuk melihat jumlah mitra dan nilai sentralitasnya.
        - **Garis Penghubung:** Menggambarkan aliran keterkaitan antara Pelabuhan/Bandara dengan negara mitra Ekspor
        - **Hubungan:** Menjelaskan keterkaitan antara Pelabuhan/Bandara dan negara mitra.
        """)

    st.markdown("---")

    st.markdown("**Tampilan Adjacency Matrix**")
    st.caption("Matriks hubungan Pelabuhan/Bandara dan negara. Semakin gelap/hijau warna sel, semakin tinggi nilai transaksinya.")
    
    if not df_filtered.empty:
        st.plotly_chart(_fig_matrix(df_filtered), use_container_width=True)
        style.chart_footer("USD")
    else:
        st.info("Tidak ada data yang memenuhi ambang batas filter saat ini.")
        
    # --- Panduan Membaca Matriks ---
    with st.expander("Panduan Membaca Matriks", expanded=False):
        st.markdown("""
        - **Baris:** Pelabuhan/Bandara ekspor.
        - **Kolom:** Negara mitra dagang.
        - Titik potong antar baris dan kolom menunjukkan adanya ekspor dari Pelabuhan/Bandara ke Negara mitra.
        """)