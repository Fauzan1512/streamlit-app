import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Data
@st.cache_data
def load_data(file):
    data = pd.read_excel(file)
    return data

file = st.file_uploader("Upload File Excel", type=["xlsx", "xls"])

if file is not None:
    df = load_data(file)
    st.write("### Preview Data")
    st.dataframe(df.head())

    # Preprocessing Data
    st.write("### Preprocessing Data")
    df['Tgl. SEP'] = pd.to_datetime(df['Tgl. SEP'], errors='coerce')
    df['Tgl. Lahir'] = pd.to_datetime(df['Tgl. Lahir'], errors='coerce')
    df['Umur'] = (df['Tgl. SEP'] - df['Tgl. Lahir']).dt.days // 365

    # Kategori Umur
    def kategori_umur(umur):
        if umur <= 5:
            return 'Bayi'
        elif umur <= 12:
            return 'Anak-anak'
        elif umur <= 18:
            return 'Remaja'
        elif umur <= 59:
            return 'Dewasa'
        else:
            return 'Lansia'

    df['Kategori Umur'] = df['Umur'].apply(kategori_umur)
    st.write("Data setelah preprocessing:")
    st.dataframe(df[['Tgl. SEP', 'Kelamin', 'Umur', 'Kategori Umur', 'Diagnosa Awal', 'Faskes Perujuk']].head())

    # Analisis Distribusi Kelamin
    st.write("### Distribusi Kelamin")
    gender_count = df['Kelamin'].value_counts()
    st.bar_chart(gender_count)

    # Tren Kunjungan Bulanan
    st.write("### Tren Kunjungan Bulanan")
    df['Bulan'] = df['Tgl. SEP'].dt.to_period('M').astype(str)
    monthly_visits = df.groupby('Bulan').size().reset_index(name='Jumlah')
    monthly_visits = monthly_visits.sort_values('Bulan')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='Bulan', y='Jumlah', data=monthly_visits, marker='o', ax=ax)
    ax.set_title("Tren Kunjungan Bulanan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pasien")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Diagnosa Terbanyak
    st.write("### Top 10 Diagnosa Awal")
    top_diagnosa = df['Diagnosa Awal'].value_counts().head(10)
    st.bar_chart(top_diagnosa)

    faskes_diagnosa = df.groupby(['Faskes Perujuk', 'Diagnosa Awal']).size().reset_index(name='Jumlah')
    st.write("Jumlah Pasien berdasarkan Faskes dan Diagnosa awal")
    st.dataframe(faskes_diagnosa)

    # Hubungan Umur dan Diagnosa
    st.write("### Hubungan Umur dan Diagnosa awak")
    umur_diagnosa = df.groupby(['Kategori Umur', 'Diagnosa Awal']).size().reset_index(name='Jumlah')
    st.write("Jumlah Pasien berdasarkan Umur dan Diagnosa awal")
    st.dataframe(umur_diagnosa)

    # Insight
    st.write("### Insight")
    st.write(f"Total Pasien: {df.shape[0]}")
    st.write(f"Rata-rata Usia Pasien: {df['Umur'].mean():.2f} Tahun")
    st.write(f"Diagnosa Awal Terbanyak: {top_diagnosa.idxmax()}")
