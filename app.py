"""Peta Ekspor Pertanian dan Pangan Indonesia. Sumber: BPS."""
import streamlit as st
from src import data, style
from src.views.hierarki import render_hierarki
from src.views.aliran import render_aliran
from src.views.jaringan import render_jaringan

st.set_page_config(page_title="Peta Ekspor Pertanian dan Pangan Indonesia",
                   layout="wide")
style.daftar_template()
style.inject_css()
style.inject_loader()
style.inject_sections()
style.inject_extra("assets/hero.jpg")
style.inject_aksesibilitas()
style.inject_scroll_anim()
style.inject_geometri()

ch = data.chapter_tahun()

# ---- 0. Hero ----
with st.container(key="sec_hero"):
    style.anchor("hero")
    st.markdown(
        '<div style="text-align:center"><span class="hero-badge">'
        'Ekspor HS Chapter 01–24 · Pertanian &amp; Pangan</span></div>'
        '<div class="hero-judul">Peta Ekspor Pertanian<br>dan Pangan Indonesia</div>'
        '<div class="hero-garis"></div>'
        '<div class="hero-sub">Struktur komoditas, aliran perdagangan, '
        'dan jaringan negara tujuan · Sumber: Badan Pusat Statistik</div>',
        unsafe_allow_html=True)

    c_spasi1, c_filter, c_spasi2 = st.columns([1, 4, 1])
    with c_filter:
        tahun = st.radio("Tahun data", sorted(ch["tahun"].unique(), reverse=True),
                         horizontal=True, label_visibility="collapsed")

    d = ch[ch["tahun"] == tahun]
    total = d["nilai_usd"].sum()
    prev = ch[ch["tahun"] == tahun - 1]["nilai_usd"].sum()
    top = d.nlargest(1, "nilai_usd").iloc[0]
    n_negara = data.chapter_negara_tahun().query("tahun == @tahun")["negara"].nunique()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"Total ekspor {tahun}", style.format_usd(total))
    c2.metric(
        label=f"Komoditas Terbesar", 
        value=top["nama_chapter"]
    )
    c3.metric("Negara tujuan", f"{n_negara}")
    
    tahun_awal = 2023   
    if prev > 0:
        pertumbuhan = (total - prev) / prev
        c4.metric(
            "Pertumbuhan y-o-y",
            f"{pertumbuhan:+.1%}",
            delta=f"dibanding {tahun - 1}",
            delta_color="off",
        )
    else:
        c4.metric(
            "Pertumbuhan y-o-y",
            f"Tidak ada pembanding",
            delta_color="off",
        )
    st.markdown("<br><br>", unsafe_allow_html=True)

# ---- 1. Hierarki ----
with st.container(key="sec_hierarki"):
    style.anchor("hierarki")
    st.header("1. Komoditas apa yang menopang ekspor?")
    with st.spinner("Menyiapkan struktur komoditas..."):
        render_hierarki(tahun)

# ---- 2. Aliran ----
with st.container(key="sec_aliran"):
    style.anchor("aliran")
    st.header("2. Ke negara mana komoditas mengalir?")
    with st.spinner("Memetakan aliran perdagangan..."):
        render_aliran(tahun)

# ---- 3. Jaringan ----
with st.container(key="sec_jaringan"):
    style.anchor("jaringan")
    st.header("3. Pelabuhan/Bandara mana yang melayani negara mana?")
    with st.spinner("Membangun jaringan negara tujuan..."):
        render_jaringan(tahun)

# ---- 4. Penutup + Tentang ----
neg_t = (data.chapter_negara_tahun().query("tahun == @tahun")
         .groupby("negara")["nilai_usd"].sum().sort_values(ascending=False))
top3 = neg_t.head(3)
if prev > 0:
    g = (total - prev) / prev
    teks_g = f"{'naik' if g >= 0 else 'turun'} {abs(g):.1%}".replace(".", ",")
    kartu_g = (f"{g:+.1%}".replace(".", ","), f"Ekspor {tahun} {teks_g} dari {tahun - 1}")
else:
    kartu_g = ("n/a", "Tahun terawal, tidak ada pembanding")

with st.container(key="sec_akhir"):
    style.anchor("akhir")
    st.header("Penutup")
    st.subheader("Ekspor pangan Indonesia bertumpu pada sedikit komoditas dan sedikit negara")
    p1, p2, p3 = st.columns(3)
    p1.markdown(style.kartu("Satu komoditas dominan", f"{top['nilai_usd'] / total:.0%}",
                            top["nama_chapter"]), unsafe_allow_html=True)
    p2.markdown(style.kartu("Tiga negara teratas", f"{top3.sum() / total:.0%}",
                            ", ".join(top3.index)), unsafe_allow_html=True)
    p3.markdown(style.kartu("Arah tahun ini", kartu_g[0], kartu_g[1]), unsafe_allow_html=True)
    st.markdown(
        "<br>Struktur menunjukkan satu komoditas menguasai sebagian besar nilai ekspor. "
        "Aliran dan jaringan memperlihatkan nilainya terkonsentrasi pada segelintir negara tujuan. "
        "Pola ini berarti ekspor pangan peka terhadap perubahan permintaan satu komoditas dan "
        "beberapa pasar utama.", unsafe_allow_html=True)

    st.divider()
    st.header("Tentang")
    a, b = st.columns(2)
    with a:
        st.subheader("Sumber data")
        st.markdown("""
- **Tabel:** Ekspor HS 2 Digit Tahun 2023, 2024, 2025 (Badan Pusat Statistik)
- **Cakupan:** HS chapter 01-24, menurut negara tujuan, pelabuhan, dan bulan
- **Satuan:** USD
- **URL:** https://www.bps.go.id/id/exim  |  **Tanggal akses:** 03/10/2026
""")
        st.subheader("Keterbatasan")
        st.markdown("""
- Analisis di level chapter, bukan komoditas rinci.
- Nama kelompok komoditas adalah ringkasan penulis, bukan nama resmi BTKI.
- Ambang nilai dan jumlah negara teratas memengaruhi tampilan Aliran dan Jaringan.
- Kolom pelabuhan pada data BPS mencampur pelabuhan laut dan bandara (bertanda "(U)"), dan keduanya diperlakukan sama.
""")
    with b:
        st.subheader("Penggunaan alat AI")
        st.markdown("Asisten AI dipakai untuk membantu menulis, men-debug kode serta keperluan teknis dalam pengkodingan. Seluruh data, angka, rancangan visual dan hasil dibuat, diperiksa, dan dipahami sendiri oleh penulis.")

# ---- Footer ----
with st.container(key="sec_footer"):
    st.markdown("""
<div class="foot-grid">
  <div><b>Proyek</b>Peta Ekspor Pertanian dan Pangan Indonesia<br>
  UAS Visualisasi Data dan Informasi, Politeknik Statistika STIS, 2026</div>
  <div><b>Sumber data</b>Badan Pusat Statistik (BPS)<br>Ekspor HS 2 Digit, 2023-2025</div>
  <div><b>Contact Us</b><div>222313373@stis.ac.id</div></div>
</div>
<div class="foot-copy">Dibuat oleh Sean Gusti Setyawan. </div>
""", unsafe_allow_html=True)

style.nav_aktif()

