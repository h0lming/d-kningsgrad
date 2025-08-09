
import streamlit as st

st.set_page_config(page_title="Dækningsgrad beregner", page_icon="💸", layout="centered")

# --- Simple styling ---
st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 920px;}
.hero-wrap {display: grid; grid-template-columns: 1fr; gap: 14px; margin: 10px 0 16px;}
.hero {border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 18px 20px; background: rgba(255,255,255,0.04); text-align: center;}
.hero .label {font-size: 0.95rem; opacity: 0.85; margin-bottom: 6px;}
.hero .value {font-size: 2rem; font-weight: 700; line-height: 1.1;}
.kpi-wrap {display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 8px 0 0;}
.kpi {border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 16px; text-align: center; background: rgba(255,255,255,0.02);}
.kpi .label {font-size: 0.9rem; opacity: 0.85;}
.kpi .value {font-size: 1.6rem; font-weight: 700; margin-top: 6px;}
div.streamlit-expanderHeader {font-weight: 600;}
@media (max-width: 800px){ .kpi-wrap{grid-template-columns: 1fr;} }
</style>
""", unsafe_allow_html=True)

st.title("Dækningsgrad beregner 💸")

# --- Inputs ---
timepris_kost = st.number_input("Timepris (KOST)", min_value=0.0, value=356.9, step=1.0)
timepris_salg = st.number_input("Timepris (SALG)", min_value=0.0, value=628.0, step=1.0)
timer = st.number_input("Montørtimer (antal)", min_value=0.0, value=5.0, step=1.0)
materiale_kost = st.number_input("Kostpris for materialer", min_value=0.0, value=6000.0, step=100.0)
onsket_dg_pct = st.number_input("Ønsket dækningsgrad (%)", min_value=0.0, max_value=99.9, value=35.0, step=1.0, help="DG = (Omsætning - Omkostning) / Omsætning")

# --- Calculations ---
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
salg_med_moms = samlet_salg_uden_moms * 1.25  # 25% moms

# --- HERO totals ---
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

# --- Details + KPIs ---
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
    # KPI block moved here
    st.markdown('<div class="kpi-wrap">', unsafe_allow_html=True)
    st.markdown(f"""
      <div class="kpi">
        <div class="label">Dækningsbidrag (DB)</div>
        <div class="value">{db:,.2f} kr.</div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
      <div class="kpi">
        <div class="label">DB pr. time</div>
        <div class="value">{db_pr_time:,.2f} kr./time</div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
      <div class="kpi">
        <div class="label">Dækningsgrad</div>
        <div class="value">{onsket_dg_pct:.1f}%</div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("Formler: S = C / (1 − DG).  DG = (S − C) / S.  DB = S − C.  DB/time = DB ÷ timer.  Moms = 25%.")
