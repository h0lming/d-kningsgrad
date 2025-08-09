# Dækningsgrad beregner (Streamlit)

En simpel Streamlit-app til at beregne samlet salgspris ud fra timepriser, materialer og ønsket dækningsgrad.

## Filer
- `daekningsgrad_app_v3.py` – selve appen
- `requirements.txt` – Python afhængigheder

## Kør lokalt
```bash
# (valgfrit) opret og aktiver virtuel environment
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run daekningsgrad_app_v3.py
```

## Del som hjemmeside (Streamlit Community Cloud)
1. Opret et GitHub repository og upload `daekningsgrad_app_v3.py` + `requirements.txt`.
2. Log ind på https://streamlit.io → **Deploy an app**.
3. Vælg dit repo og fil: `daekningsgrad_app_v3.py`. Tryk **Deploy**.
4. Du får et offentlig link (kan åbnes på mobil/andre PC'er).
