import streamlit as st
import pandas as pd
import requests

# Konfigurasi halaman
st.set_page_config(page_title="CryptoPredictor Lite", page_icon=":crystal_ball:", layout="wide", initial_sidebar_state="expanded")

# Judul
st.title("CryptoPredictor Lite (Dark Mode)")

# Fungsi ambil data
@st.cache_data(ttl=600)
def fetch_top_coins(per_page=50):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "idr",
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h"
    }
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Ambil data
df = fetch_top_coins()

# Kalau datanya tidak kosong
if not df.empty:
    # Tambahkan kolom Status: Bullish jika 24h% > 0, Bearish jika <= 0
    if "price_change_percentage_24h" in df.columns:
        df["Status"] = df["price_change_percentage_24h"].apply(lambda x: "Bullish" if x > 0 else "Bearish")
    
        # Tampilkan tabel
        st.subheader("Daftar Koin Teratas (Top 50)")
        st.dataframe(
            df[["symbol", "current_price", "price_change_percentage_24h", "Status"]]
            .rename(columns={
                "symbol": "Koin",
                "current_price": "Harga (IDR)",
                "price_change_percentage_24h": "24h (%)"
            }),
            use_container_width=True
        )
    else:
        st.error("Kolom perubahan harga 24 jam tidak tersedia.")
else:
    st.warning("Data tidak tersedia.")
