import base64
import json
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
import streamlit.components.v1 as components

KARTU, BORDER = "#FFFFFF", "#E0E0E0"
AKSEN = "#009E73"
TEKS, TEKS2 = "#202124", "#181B19"

OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9",
             "#D55E00", "#F0E442", "#999999"]
DIVERGEN = [[0, "#D55E00"], [0.5, "#F1F5F9"], [1, "#009E73"]]

SUMBER = "Sumber: BPS"

SECTIONS = [("hero", "Awal"), ("hierarki", "Struktur"), ("aliran", "Aliran"),
            ("jaringan", "Jaringan"), ("akhir", "Penutup dan data")]
LATAR = {"hero": "#FFFFFF", "hierarki": "#E8F5F1", "aliran": "#FFFFFF",
         "jaringan": "#E8F5F1", "akhir": "#FFFFFF"}


def format_usd(x: float) -> str:
    for batas, kata in [(1e12, "triliun"), (1e9, "miliar"), (1e6, "juta"), (1e3, "ribu")]:
        if abs(x) >= batas:
            return f"{x / batas:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".") + f" {kata} USD"
    return f"{x:,.0f} USD"


def daftar_template():
    pio.templates["visdat"] = go.layout.Template(layout=dict(
        font=dict(family="Inter, Arial, sans-serif", size=13, color=TEKS),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
        yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
        legend=dict(orientation="h", y=-0.15),
        hoverlabel=dict(font_size=13),
        margin=dict(l=10, r=10, t=50, b=10),
    ))
    pio.templates.default = "visdat"


def chart_footer(satuan: str = "USD"):
    st.markdown(f'<div class="footer-grafik">{SUMBER} | Satuan: {satuan}</div>',
                unsafe_allow_html=True)


def anchor(k):
    st.markdown(f'<div id="{k}"></div>', unsafe_allow_html=True)


def kontrol_negara(kunci: str):
    c1, c2 = st.columns(2)
    ambang = c1.slider("Ambang kontribusi komoditas (%)", 0.0, 5.0, 0.5, 0.1, key=f"ambang_{kunci}")
    topn = c2.slider("Jumlah negara teratas", 10, 40, 30, 5, key=f"topn_{kunci}")
    return ambang, topn


def kartu(label: str, nilai: str, catatan: str = "", warna: str = None):
    w = f"color:{warna};" if warna else f"color:{TEKS};"
    return (f'<div class="kartu"><div class="kartu-label">{label}</div>'
            f'<div class="kartu-nilai" style="{w}">{nilai}</div>'
            f'<div class="kartu-catatan" title="{catatan}">{catatan}</div></div>')


def inject_css():
    st.markdown(f"""<style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
      html, body, .stApp, button, input, select, textarea {{ font-family:'Inter',sans-serif; }}
      h1, h2, h3 {{ color:{TEKS}; font-weight:700; letter-spacing:-0.3px; margin-bottom:1rem; }}
      [data-testid="stCaptionContainer"] {{ color:{TEKS2} !important; font-size:1.05rem !important; font-weight:500; }}
      a {{ color:#007656; text-decoration:none; font-weight:500; }}

      div[role="radiogroup"] {{ flex-direction:row !important; justify-content:center !important; gap:2rem !important; }}

      [data-testid="stExpander"] {{ border:1px solid {BORDER}; border-radius:8px; background:#FFFFFF; }}
      [data-testid="stVerticalBlockBorderWrapper"] {{ border-radius:8px; }}
      hr {{ margin:2rem 0; }}

      [data-testid="stMetric"] {{ background:{KARTU}; border:1px solid {BORDER};
          border-left:4px solid {AKSEN}; border-radius:8px; padding:16px; min-height:125px; }}
      [data-testid="stMetricLabel"] {{ color:{TEKS2}; font-weight:600; font-size:12px; text-transform:uppercase; }}
      [data-testid="stMetricValue"] > div {{ font-weight:700; color:{TEKS}; font-size:20px;
          white-space:normal; overflow:visible; line-height:1.2; }}
      [data-testid="stMetricDelta"] {{ font-size:13px; }}
      [data-testid="stMetricValue"] {{
            white-space: normal !important;
      }}
        [data-testid="stMetricValue"] > div {{
            white-space: normal !important;
            word-break: break-word !important;
            line-height: 1.2 !important;
            font-size: 1.4rem !important; /* Sedikit dikecilkan agar muat rapi */
        }}

      .kartu {{ background:{KARTU}; border:1px solid {BORDER}; border-top:3px solid {AKSEN};
          border-radius:8px; padding:16px 18px; min-height:132px;
          display:flex; flex-direction:column; gap:4px; margin-bottom: 24px; }}
      .kartu-label {{ color:{TEKS2}; font-size:.75rem; font-weight:700; text-transform:uppercase;
          letter-spacing:.5px; margin-bottom:4px; }}
      .kartu-nilai {{ font-weight:800; font-size:clamp(1.15rem,1.8vw,1.6rem); line-height:1.15;
          overflow-wrap:anywhere; }}
      .kartu-catatan {{ color:{TEKS2}; font-size:.9rem; font-weight:600; line-height:1.3;
          margin-top:auto; padding-top:8px;
          display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }}
      .footer-grafik {{ color:{TEKS2}; font-size:.8rem; margin-top:-.5rem; }}
    </style>""", unsafe_allow_html=True)


def inject_sections():
    css = f"""
    [class*="st-key-sec_"] {{ padding:4rem max(1.5rem, calc((100% - 1100px)/2)); }}
    [class*="st-key-sec_"] h2 {{ font-size:1.9rem; margin-bottom:.25rem; }}
    [class*="st-key-sec_"] h3 {{ font-size:1.35rem; }}

    .hero-badge {{ display:inline-block; padding:6px 16px; border-radius:4px; background:#E8F5F1;
        color:#007656; font-size:.85rem; font-weight:600; text-transform:uppercase; margin-bottom:1.5rem; }}
    .hero-judul {{ text-align:center; font-size:3rem; font-weight:800; color:{TEKS};
        line-height:1.1; margin:0 0 1rem; }}
    .hero-garis {{ display:none; }}
    .hero-sub {{ text-align:center; font-size:1.1rem; color:{TEKS2}; max-width:700px;
        margin:0 auto 2rem; line-height:1.6; }}

    @media (max-width: 768px) {{
        [class*="st-key-sec_"] {{ padding: 3rem 1.25rem !important; }}
        
        .hero-judul {{ font-size: 2.2rem !important; line-height: 1.2 !important; }}
        .hero-sub {{ font-size: 1rem !important; padding: 0 10px; }}
        
        div[role="radiogroup"] {{ flex-wrap: wrap !important; gap: 1rem !important; }}
        
        [data-testid="stVerticalBlock"] > [data-testid="column"] {{ 
            margin-bottom: 1rem; 
        }}
        
        [data-testid="stMetric"] {{ padding: 16px !important; min-height: auto !important; }}
        .kartu {{ min-height: 110px; padding: 14px 16px; margin-bottom: 16px !important; }}
        
        [data-testid="stMetricValue"] > div, .kartu-nilai {{ font-size: 1.5rem !important; }}
    }}
    """
    for k, bg in LATAR.items():
        css += f".st-key-sec_{k} {{ background:{bg}; }}\n"
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


@st.cache_data
def _hero_css(path: str) -> str:
    p = Path(__file__).resolve().parents[1] / path
    if not p.exists():
        return ""
    b64 = base64.b64encode(p.read_bytes()).decode()
    return (
        ".st-key-sec_hero{background:linear-gradient(rgba(6,40,30,.35),rgba(6,40,30,.60)),"
        f"url(data:image/jpeg;base64,{b64}) center/cover no-repeat !important;}}"
        ".st-key-sec_hero .hero-judul{color:#FFFFFF !important;}"
        ".st-key-sec_hero .hero-sub{color:#EAF4F0 !important;}"
        ".st-key-sec_hero .hero-badge{background:rgba(255,255,255,.92) !important;color:#007656 !important;}"
        '.st-key-sec_hero div[role="radiogroup"]{background:rgba(255,255,255,.94);'
        "border-radius:999px;padding:.4rem 1.4rem;width:fit-content;margin:0 auto;}"
    )


def inject_extra(hero_path: str = "assets/hero.jpg"):
    css = f"""
    header[data-testid="stHeader"] {{ background:transparent !important; }}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {{ visibility:hidden; }}
    footer, .stApp > footer, [data-testid="stFooter"],
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {{ display:none !important; }}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main {{
        background:#202124 !important; }}
    
    [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"],
    [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {{
        gap: 0 !important; 
    }}

    div[class*="st-key-sec_"] > div[data-testid="stVerticalBlock"] {{
        gap: 1rem !important;
    }}

    [data-testid="stElementContainer"]:has(iframe), .element-container:has(iframe) {{
        position:absolute !important; width:0 !important; height:0 !important;
        margin:0 !important; padding:0 !important; overflow:hidden !important; }}

    #js-plotly-tester {{ width:0 !important; height:0 !important;
        overflow:hidden !important; pointer-events:none !important; }}
    html, body {{ overflow-x:hidden; }}

    * {{ scrollbar-width:none !important; }}
    *::-webkit-scrollbar {{ display:none !important; width:0 !important; height:0 !important; }}

    .st-key-sec_hero {{ min-height:100vh; display:flex; flex-direction:column; justify-content:center; }}

    .st-key-sec_footer {{ background:#202124 !important; padding-top:2.5rem !important;
        padding-bottom:2rem !important; margin-bottom:0 !important; }}
    .st-key-sec_footer, .st-key-sec_footer * {{ color:#E8EAED !important; }}
    .st-key-sec_footer a {{ color:#7FD8BE !important; text-decoration:underline; }}
    .foot-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:1.5rem; }}
    .foot-grid b {{ display:block; margin-bottom:.35rem; font-size:.8rem; letter-spacing:.5px;
        text-transform:uppercase; opacity:.7; }}
    .foot-copy {{ margin-top:1.5rem; padding-top:1rem; border-top:1px solid #3C4043;
        font-size:.8rem; opacity:.75; }}
    
    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stMain"] {{ padding-top:0 !important; margin-top:0 !important; }}

    [data-testid="stMainBlockContainer"] {{ padding-top:0 !important; }}

    .st-key-sec_hero {{ margin-top:0 !important; }}
    
    .stApp [data-testid="stMainBlockContainer"] {{
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-top: 0 !important;
        max-width: 100vw !important;
        width: 100% !important;
        overflow-x: hidden;
    }}
    """ + _hero_css(hero_path)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


_JS = """<script>
(function(){
  const P = window.parent, D = P.document;
  const ids = __IDS__, warna = __WARNA__, label = __LABEL__;
  const hero = D.querySelector('.st-key-sec_hero');

  function rapikan(){
    const t = D.getElementById('js-plotly-tester');
    if (t){ t.style.setProperty('width','0','important'); t.style.setProperty('height','0','important'); }
  }
  rapikan(); setInterval(rapikan, 1500);

  ['nv-style','nv-dots','btn-atas'].forEach(function(i){ const e=D.getElementById(i); if(e) e.remove(); });

  const st = D.createElement('style'); st.id = 'nv-style';
  st.textContent = `
    #nv-dots{position:fixed;right:18px;top:50%;transform:translateY(-50%);z-index:99999;
      display:flex;flex-direction:column;gap:16px;}
    #nv-dots a{display:block;width:12px;height:12px;border-radius:50%;background:#B9C0C7;
      border:2px solid #FFFFFF;box-shadow:0 0 0 1px #9AA3AB;transition:all .25s;}
    #nv-dots a:hover{transform:scale(1.3);}
    #nv-dots a.aktif{transform:scale(1.6);border-color:#009E73;box-shadow:0 0 0 1px #009E73;}
    #btn-atas{position:fixed;right:18px;bottom:22px;z-index:99999;width:44px;height:44px;
      border-radius:50%;border:1px solid #009E73;background:#FFFFFF;color:#009E73;font-size:20px;
      cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.15);opacity:0;pointer-events:none;
      transform:translateY(10px);transition:all .25s;}
    #btn-atas.tampil{opacity:1;pointer-events:auto;transform:none;}
    #btn-atas:hover{background:#009E73;color:#FFFFFF;}
    @media (max-width:480px){#nv-dots{display:none;}}`;
  D.head.appendChild(st);

  const nav = D.createElement('div'); nav.id = 'nv-dots';
  ids.forEach(function(k){
    const a = D.createElement('a');
    a.href = '#' + k; a.title = label[k] || k; a.setAttribute('aria-label', label[k] || k);
    nav.appendChild(a);
  });
  D.body.appendChild(nav);

  const btn = D.createElement('button');
  btn.id = 'btn-atas'; btn.type = 'button'; btn.title = 'Kembali ke atas';
  btn.setAttribute('aria-label', 'Kembali ke atas'); btn.textContent = '\\u2191';
  btn.onclick = function(){ if (hero) hero.scrollIntoView({behavior:'smooth', block:'start'}); };
  D.body.appendChild(btn);

  function update(){
    let aktif = ids[0];
    ids.forEach(function(k){
      const el = D.querySelector('.st-key-sec_' + k);
      if (el && el.getBoundingClientRect().top <= P.innerHeight * 0.4) aktif = k;
    });
    nav.querySelectorAll('a').forEach(function(a){
      const k = a.getAttribute('href').slice(1), on = (k === aktif);
      a.classList.toggle('aktif', on);
      a.style.background = on ? (warna[k] || '#FFFFFF') : '#B9C0C7';
    });
    if (hero) btn.classList.toggle('tampil', hero.getBoundingClientRect().bottom < P.innerHeight * 0.3);
  }
  nav.addEventListener('click', function(e){
    const a = e.target.closest('a'); if (!a) return;
    e.preventDefault();
    const el = D.querySelector('.st-key-sec_' + a.getAttribute('href').slice(1));
    if (el) el.scrollIntoView({behavior:'smooth', block:'start'});
  });
  if (P.__navScroll) D.removeEventListener('scroll', P.__navScroll, true);
  P.__navScroll = update;
  D.addEventListener('scroll', update, true);
  setTimeout(update, 300);
})();
</script>"""


def nav_aktif():
    warna = {k: (v if v.startswith("#") else "#FFFFFF") for k, v in LATAR.items()}
    html = (_JS.replace("__IDS__", json.dumps([k for k, _ in SECTIONS]))
               .replace("__WARNA__", json.dumps(warna))
               .replace("__LABEL__", json.dumps(dict(SECTIONS))))
    components.html(html, height=0)

def inject_aksesibilitas():
    _JS_A11Y = """<script>
    (function(){
        const P = window.parent, D = P.document;
        if (D.getElementById('a11y-widget')) return;

        const st = D.createElement('style');
        st.innerHTML = `
            #a11y-widget {
                position: fixed; top: 50%; left: 0; transform: translateY(-50%);
                z-index: 999999; display: flex; flex-direction: column;
                background: #FFFFFF; border: 1px solid #E0E0E0; border-left: none;
                border-radius: 0 12px 12px 0; box-shadow: 4px 4px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
            }
            .a11y-header {
                background: #F8F9FA; padding: 12px; font-size: 11px; font-weight: 700;
                color: #5F6368; text-transform: uppercase; letter-spacing: 0.5px;
                border-bottom: 1px solid #E0E0E0; text-align: center;
                border-radius: 0 12px 0 0;
            }
            .a11y-btn {
                background: transparent; border: none; padding: 16px; cursor: pointer;
                display: flex; align-items: center; justify-content: center;
                border-bottom: 1px solid #F0F0F0; color: #5F6368; transition: all 0.2s;
                position: relative;
            }
            .a11y-btn:last-child { border-bottom: none; border-radius: 0 0 12px 0; }
            .a11y-btn svg { width: 24px; height: 24px; flex-shrink: 0; }
            
            .a11y-label { display: none; }

            .a11y-btn::after {
                content: attr(data-tooltip); position: absolute; left: 100%; top: 50%;
                transform: translateY(-50%); background: #202124; color: #fff;
                padding: 8px 14px; border-radius: 6px; font-size: 13px; font-weight: 500;
                white-space: nowrap; opacity: 0; pointer-events: none;
                transition: 0.2s; margin-left: 12px; font-family: 'Inter', sans-serif;
            }
            @media (hover: hover) {
                .a11y-btn:hover { background: #E8F5F1; color: #009E73; }
                .a11y-btn:hover::after { opacity: 1; margin-left: 16px; }
            }

            #a11y-toggle { display: none; }
            
            @media (max-width: 1024px) {
                #a11y-widget { 
                    top: auto; bottom: 40px; 
                    transform: translateX(-100%); 
                    overflow: visible; 
                }
                #a11y-widget.buka { transform: translateX(0); }
                .a11y-header { display: none; }
                
                .a11y-btn {
                    justify-content: flex-start;
                    padding: 16px 24px 16px 16px;
                    gap: 14px;
                }
                
                .a11y-label {
                    display: block; font-family: 'Inter', sans-serif;
                    font-size: 14px; font-weight: 600; white-space: nowrap;
                }
                
                #a11y-toggle {
                    display: flex; position: absolute; left: 100%; 
                    bottom: 0; top: auto; transform: none; 
                    background: #009E73; color: #fff;
                    border: none; padding: 18px 10px; border-radius: 0 8px 8px 0;
                    cursor: pointer; box-shadow: 3px 0 8px rgba(0,0,0,0.15);
                }
                #a11y-toggle svg { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 2.5;}
                .a11y-btn::after { display: none !important; }
            }

            body.a11y-teks * { font-size: 106% !important; }
            body.a11y-kontras .stApp { filter: contrast(135%) saturate(115%); }
            body.a11y-parsial .stApp { filter: contrast(120%) saturate(160%) hue-rotate(-10deg); }
            body.a11y-total .stApp { filter: grayscale(100%) contrast(110%); }
        `;
        D.head.appendChild(st);

        const widget = D.createElement('div');
        widget.id = 'a11y-widget';
        
        const header = D.createElement('div');
        header.className = 'a11y-header';
        header.innerText = 'Akses';
        widget.appendChild(header);

        const btnToggle = D.createElement('button');
        btnToggle.id = 'a11y-toggle';
        btnToggle.innerHTML = '<svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"></polyline></svg>';
        btnToggle.onclick = function() {
            widget.classList.toggle('buka');
            const isOpen = widget.classList.contains('buka');
            btnToggle.innerHTML = isOpen 
                ? '<svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"></polyline></svg>'
                : '<svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"></polyline></svg>';
        };
        widget.appendChild(btnToggle);

        const iconTeks = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>';
        const iconKontras = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 0 0 20z" fill="currentColor"/></svg>';
        const iconParsial = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="2" x2="12" y2="22"/><path d="M12 12h8.5"/></svg>';
        const iconTotal = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>';

        const fitur = [
            { id: 'btn-teks', ikon: iconTeks, tooltip: 'Perbesar Teks', kelas: 'a11y-teks', grup: 'ukuran' },
            { id: 'btn-kontras', ikon: iconKontras, tooltip: 'Kontras Tinggi', kelas: 'a11y-kontras', grup: 'warna' },
            { id: 'btn-parsial', ikon: iconParsial, tooltip: 'Buta Warna Parsial', kelas: 'a11y-parsial', grup: 'warna' },
            { id: 'btn-total', ikon: iconTotal, tooltip: 'Monokrom (Total)', kelas: 'a11y-total', grup: 'warna' }
        ];

        fitur.forEach(f => {
            const b = D.createElement('button');
            b.className = 'a11y-btn';
            b.id = f.id;
            b.innerHTML = f.ikon + '<span class="a11y-label">' + f.tooltip + '</span>';
            b.setAttribute('data-tooltip', f.tooltip);
            
            b.onclick = function() {
                const isActive = D.body.classList.contains(f.kelas);
                
                if (f.grup === 'warna') {
                    fitur.filter(item => item.grup === 'warna').forEach(item => {
                        D.body.classList.remove(item.kelas);
                        const btnReset = D.getElementById(item.id);
                        if(btnReset) { btnReset.style.background = ''; btnReset.style.color = '#5F6368'; }
                    });
                }

                if (!isActive) {
                    D.body.classList.add(f.kelas);
                    b.style.background = '#C6E7DE';
                    b.style.color = '#007656';
                } else {
                    D.body.classList.remove(f.kelas);
                    b.style.background = '';
                    b.style.color = '#5F6368';
                }
            };
            widget.appendChild(b);
        });

        D.body.appendChild(widget);
    })();
    </script>"""
    import streamlit.components.v1 as components
    components.html(_JS_A11Y, height=0)
       
def inject_loader():
    _JS_LOADER = """<script>
    (function(){
        const P = window.parent, D = P.document;
        
        if (D.getElementById('layar-pramuat')) return;

        const st = D.createElement('style');
        st.innerHTML = `
            #layar-pramuat {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                
                background-color: rgba(32, 33, 36, 0.75); 
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px); 
                
                z-index: 9999999;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                transition: opacity 0.6s ease, visibility 0.6s ease;
            }
            .roda-putar {
                width: 60px; height: 60px;
                border: 6px solid rgba(0, 158, 115, 0.15);
                border-top: 6px solid #009E73;
                border-radius: 50%;
                animation: putar 1s linear infinite;
                margin-bottom: 24px;
            }
            @keyframes putar { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .teks-loading {
                color: #FFFFFF; font-family: 'Inter', sans-serif; font-size: 1.1rem; 
                font-weight: 500; letter-spacing: 1px;
            }
        `;
        D.head.appendChild(st);

        const loader = D.createElement('div');
        loader.id = 'layar-pramuat';
        loader.innerHTML = '<div class="roda-putar"></div><div class="teks-loading">Memuat Dasbor Ekspor...</div>';
        D.body.appendChild(loader);

        setTimeout(function() {
            loader.style.opacity = '0';
            setTimeout(() => loader.remove(), 600);
        }, 1500);
    })();
    </script>"""
    import streamlit.components.v1 as components
    components.html(_JS_LOADER, height=0)

def inject_scroll_anim():
    _JS_ANIM = """<script>
    (function(){
        const P = window.parent, D = P.document;

        if (D.getElementById('scroll-anim-style')) return;

        const st = D.createElement('style');
        st.id = 'scroll-anim-style';
        st.innerHTML = `
            .anim-geser {
                opacity: 0;
                transform: translateY(40px); 
                transition: opacity 0.7s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.7s cubic-bezier(0.2, 0.8, 0.2, 1);
                will-change: opacity, transform;
            }
            .anim-geser.tampil {
                opacity: 1;
                transform: translateY(0);
            }
        `;
        D.head.appendChild(st);

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('tampil');
                } else {
                    entry.target.classList.remove('tampil');
                }
            });
        }, { 
            threshold: 0.1
        });

        setInterval(() => {
            const elemen = D.querySelectorAll(`
                [class*="st-key-sec_"]:not(.st-key-sec_hero):not(.st-key-sec_footer) h2,
                [class*="st-key-sec_"]:not(.st-key-sec_hero):not(.st-key-sec_footer) h3,
                [class*="st-key-sec_"]:not(.st-key-sec_hero):not(.st-key-sec_footer) .kartu,
                [class*="st-key-sec_"]:not(.st-key-sec_hero):not(.st-key-sec_footer) [data-testid="stMetric"],
                [class*="st-key-sec_"]:not(.st-key-sec_hero):not(.st-key-sec_footer) [data-testid="stPlotlyChart"],
                [class*="st-key-sec_"]:not(.st-key-sec_hero):not(.st-key-sec_footer) [data-testid="stMarkdownContainer"],
                [class*="st-key-sec_"]:not(.st-key-sec_hero):not(.st-key-sec_footer) [data-testid="stExpander"]
            `);
            
            elemen.forEach(el => {
                if (!el.classList.contains('anim-geser')) {
                    el.classList.add('anim-geser');
                    observer.observe(el);
                }
            });
        }, 1000);
    })();
    </script>"""
    import streamlit.components.v1 as components
    components.html(_JS_ANIM, height=0)