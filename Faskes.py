import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Analisis Data Faskes")

# Upload file
uploaded_file = st.file_uploader("📂 Upload file Excel (.xlsx)", type=["xlsx"])

@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_excel(file)  # Baca file Excel
        df.columns = df.columns.str.strip()  # Hapus spasi di nama kolom
        
        # Konversi data ke numerik
        df['Jarak (km)'] = pd.to_numeric(df['Jarak (km)'], errors='coerce')
        df['TOTAL'] = pd.to_numeric(df['TOTAL'], errors='coerce')
        
        return df
    return None

df = None

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.success("✅ Data berhasil dimuat!")
    st.dataframe(df)

    if df is not None and {'Jarak (km)', 'TOTAL', 'NAMA FASKES'}.issubset(df.columns):
        st.subheader("📌 Scatter Plot: Jarak vs TOTAL")

        # Hapus NaN sebelum plotting
        df = df.dropna(subset=['Jarak (km)', 'TOTAL'])

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(x=df['Jarak (km)'], 
                        y=df['TOTAL'], 
                        hue=df['NAMA FASKES'], 
                        s=100, ax=ax)
        plt.xlabel("Jarak (km)")
        plt.ylabel("TOTAL")
        plt.title("Hubungan Jarak Faskes dengan TOTAL")
        plt.legend(title="Nama Faskes", bbox_to_anchor=(1, 1))
        st.pyplot(fig)
    else:
        st.warning("⚠ Data tidak memiliki kolom yang diperlukan! Pastikan file Excel memiliki kolom: 'Jarak (km)', 'TOTAL', dan 'NAMA FASKES'.")

else:
    st.warning("⚠ Silakan upload file Excel (.xlsx) terlebih dahulu.")