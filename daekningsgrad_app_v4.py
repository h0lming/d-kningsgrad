
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components

# Page + icon
try:
    page_icon = Image.open("app_icon_512.png")
except Exception:
    page_icon = None
st.set_page_config(page_title="Dækningsgrad beregner", page_icon=page_icon, layout="centered")

# Head icon links (browser + iPhone homescreen)
components.html("""
<script>
(function() {
  const links = [
    { rel: 'apple-touch-icon', sizes: '120x120', href: 'app_icon_180.png?v=2' },
    { rel: 'apple-touch-icon', sizes: '152x152', href: 'app_icon_180.png?v=2' },
    { rel: 'apple-touch-icon', sizes: '167x167', href: 'app_icon_180.png?v=2' },
    { rel: 'apple-touch-icon', sizes: '180x180', href: 'app_icon_180.png?v=2' },
    { rel: 'icon', type: 'image/png', sizes: '32x32', href: 'favicon_32.png?v=2' },
    { rel: 'icon', type: 'image/png', sizes: '64x64', href: 'favicon_64.png?v=2' }
  ];
  links.forEach(def => { const el = document.createElement('link'); Object.entries(def).forEach(([k,v]) => el.setAttribute(k,v)); document.head.appendChild(el); });
  const metaTitle = document.createElement('meta'); metaTitle.name='apple-mobile-web-app-title'; metaTitle.content='Dækningsgrad'; document.head.appendChild(metaTitle);
})();
</script>
""", height=0)

# Auth with session state so field disappears after login
if "auth_ok" not in st.session_state:
    st.session_state.auth_ok = False
if not st.session_state.auth_ok:
    col_a, col_b = st.columns([1,3])
    with col_b:
        pw = st.text_input("Adgangskode", type="password", placeholder="Indtast kode")
        if st.button("Log ind"):
            if pw == "0000":
                st.session_state.auth_ok = True
                st.rerun()
            else:
                st.error("Forkert kode")
    st.stop()

# Light styling
st.markdown("""
<style>
:root { --card-border: rgba(0,0,0,0.12); }
.block-container {padding-top: 2rem; max-width: 980px;}
.hero-wrap {display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 10px 0 16px;}
.hero {border: 1px solid var(--card-border); border-radius: 14px; padding: 18px 20px; background: #ffffff; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.04);}
.hero .label {font-size: 0.95rem; opacity: 0.65; margin-bottom: 6px;}
.hero .value {font-size: 2rem; font-weight: 700; line-height: 1.1;}
div.streamlit-expanderHeader {font-weight: 600;}
@media (max-width: 800px){ .hero-wrap{grid-template-columns: 1fr;} }
</style>
""", unsafe_allow_html=True)

st.title("Dækningsgrad beregner 💸")

# Inputs
with st.expander("Forudsætninger", expanded=False):
    timepris_kost = st.number_input("Timepris (KOST)", min_value=0.0, value=356.9, step=1.0)
    timepris_salg = st.number_input("Timepris (SALG)", min_value=0.0, value=628.0, step=1.0)

timer = st.number_input("Montørtimer (antal)", min_value=0.0, value=5.0, step=1.0)
materiale_kost = st.number_input("Kostpris for materialer", min_value=0.0, value=6000.0, step=100.0)
onsket_dg_pct = st.number_input("Ønsket dækningsgrad (%)", min_value=0.0, max_value=99.9, value=35.0, step=1.0, help="DG = (Omsætning - Omkostning) / Omsætning")

# Calculations
arbejde_kost = timepris_kost * timer
arbejde_salg = timepris_salg * timer
samlet_kost = arbejde_kost + materiale_kost

dg = onsket_dg_pct / 100.0
if dg >= 1.0:
    st.error("Dækningsgrad kan ikke være 100% eller mere.")
    st.stop()

samlet_salg_uden_moms = samlet_kost / (1.0 - dg) if (1.0 - dg) != 0 else 0.0
materiale_salg = max(samlet_salg_uden_moms - arbejde_salg, 0.0)
materiale_avance_faktor = (materiale_salg / materiale_kost) if materiale_kost > 0 else 0.0
materiale_avance_pct = (materiale_avance_faktor - 1.0) * 100.0 if materiale_avance_faktor > 0 else 0.0

db = samlet_salg_uden_moms - samlet_kost
db_pr_time = (db / timer) if timer > 0 else 0.0
salg_med_moms = samlet_salg_uden_moms * 1.25

# Totals (side-by-side)
st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
st.markdown(f"""
  <div class="hero">
    <div class="label">Samlet salgspris (uden moms)</div>
    <div class="value">{samlet_salg_uden_moms:,.2f} kr.</div>
  </div>
""", unsafe_allow_html=True)
st.markdown(f"""
  <div class="hero">
    <div class="label">Samlet salgspris (inkl. 25% moms)</div>
    <div class="value">{salg_med_moms:,.2f} kr.</div>
  </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Details
with st.expander("Detaljer", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Montørtimer**")
        st.write(f"Kostpris: {arbejde_kost:,.2f} kr.")
        st.write(f"Salgspris: {arbejde_salg:,.2f} kr.")
    with col2:
        st.markdown("**Materialer**")
        st.write(f"Kostpris: {materiale_kost:,.2f} kr.")
        st.write(f"Salgspris (for at nå DG): {materiale_salg:,.2f} kr.")
        st.caption(f"(≈ materialeavance {materiale_avance_pct:,.1f}% → faktor {materiale_avance_faktor:,.2f}×)")

st.caption("Formler: S = C / (1 − DG).  DG = (S − C) / S.  DB = S − C.  DB/time = DB ÷ timer.  Moms = 25%.")
