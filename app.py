import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="CryptoPredictor Lite",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Dark mode CSS
st.markdown(
    """
    <style>
    body {background-color: #0E1117; color: #ECEDEF;}
    .stApp {background-color: #0E1117;}
    .css-1avcm0n, .css-1inwz65 {background-color: #1A1C23;}
    table, th, td {color: #ECEDEF !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("CryptoPredictor Lite (Dark Mode)")

@st.cache_data(ttl=60)
def fetch_top_coins(vs_currency="idr", per_page=50):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h"
    }
    r = requests.get(url, params=params)
    data = r.json()
    return pd.DataFrame(data)

# Ambil data Top 50 koin
df = fetch_top_coins()

# Tampilkan tabel utama
st.subheader("Daftar Koin Teratas (Top 50)")
st.dataframe(
    df[["symbol", "current_price", "price_change_percentage_24h"]]
      .rename(columns={
          "symbol": "Koin",
          "current_price": "Harga (IDR)",
          "price_change_percentage_24h": "24h (%)"
      }),
    use_container_width=True
)
