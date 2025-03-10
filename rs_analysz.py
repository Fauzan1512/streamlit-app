import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Analisis",  # Judul yang muncul di tab browser
    page_icon="📊",  # Ikon di tab browser
    layout="wide"  # Mode tampilan (wide untuk layar lebar)
)


st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📊 Dashboard Analisis Pasien Rujukan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px; color:gray;'>Visualisasi Data Pasien dengan Grafik </p>", unsafe_allow_html=True)

# Judul aplikasi
st.title("Frekuensi Faskes per Kecamatan")

# Membaca file Excel
data = pd.read_excel("Data feb_maret.xlsx", engine="openpyxl")
data2 = pd.read_excel("rujukan2025.xlsx", engine="openpyxl")

data2['Tgl. SEP'] = pd.to_datetime(data2['Tgl. SEP'], errors='coerce')
data2['Tgl. Lahir'] = pd.to_datetime(data2['Tgl. Lahir'], errors='coerce')

data2['Umur'] = (data2['Tgl. SEP'] - data2['Tgl. Lahir']).dt.days // 365

# Fungsi untuk menentukan kategori umur
def kategori_umur(umur):
    if pd.isna(umur) or umur < 0:
        return 'Tidak Valid'
    elif umur <= 5:
        return 'Bayi'
    elif umur <= 12:
        return 'Anak-anak'
    elif umur <= 18:
        return 'Remaja'
    elif umur <= 59:
        return 'Dewasa'
    else:
        return 'Lansia'

# Tambahkan kolom 'Kategori Umur'
data2['Kategori Umur'] = data2['Umur'].apply(kategori_umur)


# Konversi kolom "Jarak (km) faskes" ke numerik
data["Jarak (km) faskes"] = pd.to_numeric(data["Jarak (km) faskes"], errors="coerce")

# Buat kolom baru menggabungkan nama faskes dan jaraknya
data['Faskes dan Jarak'] = data['NAMA FASKES'].astype(str) + ' (' + data['Jarak (km) faskes'].astype(str) + ' km)'
# Konversi kolom pasien ke numerik
data["FAKO JANUARI"] = pd.to_numeric(data["FAKO JANUARI"], errors="coerce")
data["FAKO FEBRUARI"] = pd.to_numeric(data["FAKO FEBRUARI"], errors="coerce")
data["RJ JANUARI"] = pd.to_numeric(data["RJ JANUARI"], errors="coerce")
data["RJ FEBRUARI"] = pd.to_numeric(data["RJ FEBRUARI"], errors="coerce")

# Buat kolom baru "Pasien Fako" dan "Pasien RJ"
data["Pasien Fako"] = data["FAKO JANUARI"] + data["FAKO FEBRUARI"]
data["Pasien RJ"] = data["RJ JANUARI"] + data["RJ FEBRUARI"]

# Hitung jumlah faskes per kecamatan
kecamatan_counts = data['Kecamatan faskes'].value_counts().reset_index()
kecamatan_counts.columns = ['Kecamatan', 'Frekuensi']

# Buat diagram batang interaktif dengan Plotly
fig1 = px.bar(
    kecamatan_counts, 
    x='Kecamatan', 
    y='Frekuensi', 
    text_auto=False,  # Hilangkan angka di atas batang
    color='Frekuensi', 
    color_continuous_scale='viridis',
    labels={'Frekuensi': 'Jumlah Faskes', 'Kecamatan': 'Kecamatan'},
    hover_data={'Frekuensi': True, 'Kecamatan': True}  # Info saat hover
)

# Atur tampilan sumbu & rotasi label
fig1.update_layout(
    title='Frekuensi Faskes per Kecamatan',
    xaxis_title='Kecamatan',
    yaxis_title='Frekuensi',
    xaxis_tickangle=-45,  # Rotasi agar tidak bertumpuk
    template='plotly_white'
)

# Tampilkan grafik di Streamlit
st.plotly_chart(fig1)

# Judul aplikasi
st.title("10 Faskes Terdekat dan Total Pasiennya")

# Urutkan data berdasarkan jarak
data_sorted = data.sort_values(by='Jarak (km) faskes')

# Buat diagram batang interaktif
fig3 = px.bar(
    data_sorted.head(10), 
    x='Faskes dan Jarak', 
    y='TOTAL', 
    text_auto=False,  # Hilangkan angka di atas batang
    color='TOTAL', 
    color_continuous_scale='viridis',
    labels={'TOTAL': 'Total Pasien', 'Faskes dan Jarak': 'Faskes'},
    hover_data={'TOTAL': True, 'Jarak (km) faskes': True}  # Info saat hover
)

# Atur tampilan sumbu & rotasi label
fig3.update_layout(
    title='10 Faskes Terdekat dan Total Pasiennya',
    xaxis_title='Faskes dan Jarak',
    yaxis_title='Total Pasien',
    xaxis_tickangle=-45,
    template='plotly_white'
)

# Tampilkan grafik di Streamlit
st.plotly_chart(fig3)

# Judul aplikasi
# Buat figure untuk 10 Faskes dengan Total Pasien Terbanyak
st.title("10 Faskes dengan Total Pasien Terbanyak")
top_10_faskes = data_sorted.sort_values(by='TOTAL', ascending=False).head(10)
fig4, ax4 = plt.subplots(figsize=(10, 6))
bars = ax4.bar(top_10_faskes['Faskes dan Jarak'], top_10_faskes['TOTAL'])

# Buat diagram batang interaktif
fig4 = px.bar(
    top_10_faskes, 
    x='Faskes dan Jarak', 
    y='TOTAL', 
    text_auto=False,  # Hilangkan angka di atas batang
    color='TOTAL', 
    color_continuous_scale='viridis',
    labels={'TOTAL': 'Total Pasien', 'Faskes dan Jarak': 'Faskes'},
    hover_data={'TOTAL': True, 'Faskes dan Jarak': True}  # Info saat hover
)

# Atur tampilan sumbu & rotasi label
fig4.update_layout(
    title='10 Faskes dengan Total Pasien Terbanyak',
    xaxis_title='Faskes dan Jarak',
    yaxis_title='Total Pasien',
    xaxis_tickangle=-45,  # Rotasi agar tidak bertumpuk
    template='plotly_white'
)

# Pengaturan label dan judul
ax4.set_xlabel('Faskes dan Jarak')
ax4.set_ylabel('Total Pasien')
ax4.set_title('10 Faskes dengan Total Pasien Terbanyak')
ax4.set_xticklabels(top_10_faskes['Faskes dan Jarak'], rotation=90)
plt.tight_layout()

# Tampilkan grafik di Streamlit
st.plotly_chart(fig4)

# Buat figure untuk 10 Faskes dengan Pasien Fako Terbanyak
st.title("10 Faskes dengan Pasien Fako Terbanyak")
fako_per_faskes = data.groupby("Faskes dan Jarak")["Pasien Fako"].sum().reset_index()
top_10_fako = fako_per_faskes.nlargest(10, "Pasien Fako")

# Buat diagram batang interaktif
fig5 = px.bar(
    top_10_fako, 
    x='Faskes dan Jarak', 
    y='Pasien Fako', 
    text_auto=False,  # Hilangkan angka di atas batang
    color='Pasien Fako', 
    color_continuous_scale='viridis',
    labels={'Pasien Fako': 'Jumlah Pasien Fako', 'Faskes dan Jarak': 'Faskes'},
    hover_data={'Pasien Fako': True, 'Faskes dan Jarak': True}  # Info saat hover
)

# Atur tampilan sumbu & rotasi label
fig5.update_layout(
    title='Top 10 Jumlah Pasien Fako per Faskes',
    xaxis_title='Faskes dan Jarak',
    yaxis_title='Jumlah Pasien Fako',
    xaxis_tickangle=-45,  # Rotasi agar tidak bertumpuk
    template='plotly_white'
)

# Tampilkan grafik di Streamlit
st.plotly_chart(fig5)

# Buat figure untuk 10 Faskes dengan Pasien RJ Terbanyak
st.title("10 Faskes dengan Pasien RJ Terbanyak")
rj_per_faskes = data.groupby("Faskes dan Jarak")["Pasien RJ"].sum().reset_index()
# Ambil 10 Faskes dengan pasien RJ terbanyak
top_10_rj = rj_per_faskes.nlargest(10, "Pasien RJ")

# Pengaturan label
fig6 = px.bar(
    top_10_rj, 
    x='Faskes dan Jarak', 
    y='Pasien RJ', 
    text_auto=False,  # Hilangkan angka di atas batang
    color='Pasien RJ', 
    color_continuous_scale='viridis',
    labels={'Pasien RJ': 'Jumlah Pasien RJ', 'Faskes dan Jarak': 'Faskes'},
    hover_data={'Pasien RJ': True, 'Faskes dan Jarak': True}  # Info saat hover
)

# Atur tampilan sumbu & rotasi label
fig6.update_layout(
    title='Top 10 Jumlah Pasien RJ per Faskes',
    xaxis_title='Faskes dan Jarak',
    yaxis_title='Jumlah Pasien RJ',
    xaxis_tickangle=-45,  # Rotasi agar tidak bertumpuk
    template='plotly_white'
)

# Tampilkan grafik di Streamlit
st.plotly_chart(fig6)

# Buat figure untuk Pie Chart Pasien FAKO dan Pasien RJ
st.title("📊 Proporsi Pasien FAKO dan Pasien RJ")

# Hitung total pasien
total_fako = data["Pasien Fako"].sum()
total_rj = data["Pasien RJ"].sum()

# Buat DataFrame untuk Plotly
df_pie = pd.DataFrame({
    "Kategori": ["Pasien FAKO", "Pasien RJ"],
    "Jumlah": [total_fako, total_rj]
})

# Buat Pie Chart dengan Plotly
fig7 = px.pie(
    df_pie,
    values="Jumlah",
    names="Kategori",
    color="Kategori",
    color_discrete_map={"Pasien FAKO": "royalblue", "Pasien RJ": "crimson"},
    hole=0.4,  # Membuat tampilan Donut Chart
    title="🔹 Proporsi Pasien Berdasarkan Kategori 🔹"
)

# Tambahkan hover effect dan angka di tengah
fig7.update_traces(
    textinfo="percent+label",
    pull=[0.1, 0],  # Meledakkan bagian terbesar
    marker=dict(line=dict(color='#000', width=2))  # Tambahkan garis tepi
)

# Ubah background & tata letak
fig7.update_layout(
    showlegend=True,
    legend_title_text="Kategori Pasien",
    template="plotly_white",
    annotations=[dict(
        text=f"Total: {total_fako + total_rj}", 
        x=0.5, y=0.5, font_size=18, showarrow=False
    )]
)

# Tampilkan di Streamlit
st.plotly_chart(fig7)


st.title("🚻 Proporsi Pasien Berdasarkan Jenis Kelamin")

# Hitung jumlah pasien berdasarkan jenis kelamin
gender_counts = data2['Kelamin'].value_counts().reset_index()
gender_counts.columns = ['Jenis Kelamin', 'Jumlah']

# Tentukan warna khusus untuk tampilan lebih menarik
color_map = {
    "Laki-Laki": "royalblue",
    "Perempuan": "deeppink"
}

# Buat Pie Chart dengan Plotly
fig8 = px.pie(
    gender_counts,
    values="Jumlah",
    names="Jenis Kelamin",
    color="Jenis Kelamin",
    color_discrete_map=color_map,
    hole=0.4,  # Membuat tampilan Donut Chart
    title="🟢 Proporsi Pasien Berdasarkan Jenis Kelamin"
)

# Tambahkan efek hover & highlight
fig8.update_traces(
    textinfo="percent+label",
    pull=[0.1 if i == gender_counts['Jumlah'].idxmax() else 0 for i in range(len(gender_counts))],
    marker=dict(line=dict(color='#000', width=2))  # Tambahkan garis tepi agar lebih jelas
)

# Atur tata letak & background
fig8.update_layout(
    showlegend=True,
    legend_title_text="Jenis Kelamin",
    template="plotly_white",
    annotations=[dict(
        text=f"Total: {gender_counts['Jumlah'].sum()}",
        x=0.5, y=0.5, font_size=18, showarrow=False
    )]
)

# Tampilkan di Streamlit
st.plotly_chart(fig8)

st.title("Grafik Tren Kunjungan Mingguan")

# Salin data
df = data2.copy()

# Konversi tanggal dan filter dari 2 Januari 2025
df['Tgl. SEP'] = pd.to_datetime(df['Tgl. SEP'], errors='coerce')
start_date = pd.Timestamp("2025-01-02")
df = df[df['Tgl. SEP'] >= start_date].copy()

# Hitung minggu ke berapa sejak 2 Januari 2025
df['Minggu'] = ((df['Tgl. SEP'] - start_date).dt.days // 7) + 1

# Hitung jumlah pasien per minggu
weekly_visits = df.groupby('Minggu', as_index=False)['Tgl. SEP'].count()
weekly_visits.rename(columns={'Tgl. SEP': 'Jumlah Pasien'}, inplace=True)

# Buat grafik interaktif dengan Plotly
fig9 = px.line(
    weekly_visits, 
    x='Minggu', 
    y='Jumlah Pasien', 
    markers=True,
    line_shape="spline",  # Garis lebih halus
    title="Tren Kunjungan Mingguan (Mulai Kamis, 2 Januari 2025)",
    labels={'Minggu': 'Minggu Ke-', 'Jumlah Pasien': 'Jumlah Pasien'},
    template='plotly_white'
)

# Sesuaikan tampilan tooltip
fig9.update_traces(
    hoverinfo="x+y",  # Menampilkan info saat hover
    line=dict(width=3, color="royalblue"),  # Warna garis
    marker=dict(size=8, color="red", line=dict(width=2, color="black"))  # Marker merah dengan border hitam
)

# Tambahkan grid dan atur tampilan
fig9.update_layout(
    xaxis=dict(
        tickmode='linear', 
        tick0=1, 
        dtick=1,  # Pastikan sumbu X berisi angka minggu dengan jarak 1
        tickangle=-45  # Putar label sumbu X agar lebih rapi
    ),
    yaxis=dict(
        showgrid=True, gridwidth=0.5, gridcolor="lightgray"
    )
)
# Tampilkan grafik di Streamlit
st.plotly_chart(fig9)

st.title("Proporsi Pasien Berdasarkan Kategori Umur")

# Hitung jumlah masing-masing kategori umur
age_category_counts = data2['Kategori Umur'].value_counts().reset_index()
age_category_counts.columns = ['Kategori Umur', 'Jumlah']

# Buat Pie Chart interaktif
fig10 = px.pie(
    age_category_counts, 
    names="Kategori Umur", 
    values="Jumlah", 
    title="Proporsi Pasien Berdasarkan Kategori Umur",
    color_discrete_sequence=px.colors.qualitative.Set3,  # Warna yang lebih variatif
    hole=0.3  # Membuat efek semi-donut
)

# Tambahkan efek highlight pada kategori terbesar
fig10.update_traces(
    pull=[0.1 if i == age_category_counts['Jumlah'].idxmax() else 0 for i in range(len(age_category_counts))],  # "Meledakkan" bagian terbesar
    textinfo="percent+label",
    hoverinfo="label+value+percent"
)

# Tampilkan grafik di Streamlit
st.plotly_chart(fig10)
                
# Judul
st.title("Hubungan Diagnosa Awal dengan Faskes Perujuk")

# Grup data berdasarkan Diagnosa Awal & Faskes Perujuk
diagnosis_faskes = data2.groupby(['Diagnosa Awal', 'Faskes Perujuk']).size().reset_index(name='Jumlah Pasien')

# Ambil 10 Diagnosa Awal dengan jumlah pasien terbanyak
top_10_diagnoses = diagnosis_faskes.groupby('Diagnosa Awal')['Jumlah Pasien'].sum().nlargest(10).index
filtered_data = diagnosis_faskes[diagnosis_faskes['Diagnosa Awal'].isin(top_10_diagnoses)]

# Buat Stacked Bar Chart interaktif
fig11 = px.bar(
    filtered_data, 
    x="Diagnosa Awal", 
    y="Jumlah Pasien", 
    color="Faskes Perujuk",
    title="Hubungan antara Diagnosa Awal dan Faskes Perujuk",
    barmode="stack",  # Stacked bar
    text_auto=False,  # Menampilkan angka secara otomatis
    color_discrete_sequence=px.colors.qualitative.Set3
)

# Update tampilan chart
fig11.update_layout(
    xaxis_title="Diagnosa Awal",
    yaxis_title="Jumlah Pasien",
    legend_title="Faskes Perujuk",
    xaxis_tickangle=-45,
    plot_bgcolor="rgba(0,0,0,0)",  # Background transparan
    margin=dict(l=40, r=40, t=40, b=100)
)

# Tampilkan chart di Streamlit
st.plotly_chart(fig11)

# Judul
st.title("Hubungan Kategori Umur dengan Diagnosa Awal")

# Grup data berdasarkan Kategori Umur & Diagnosa Awal
age_diagnosis_counts = data2.groupby(['Kategori Umur', 'Diagnosa Awal']).size().reset_index(name='Jumlah Pasien')

# Ambil 10 Diagnosa Awal dengan jumlah pasien terbanyak
top_10_diagnoses = age_diagnosis_counts.groupby('Diagnosa Awal')['Jumlah Pasien'].sum().nlargest(10).index
filtered_data = age_diagnosis_counts[age_diagnosis_counts['Diagnosa Awal'].isin(top_10_diagnoses)]

# Buat Stacked Bar Chart interaktif
fig12 = px.bar(
    filtered_data, 
    x="Diagnosa Awal", 
    y="Jumlah Pasien", 
    color="Kategori Umur",
    title="Hubungan antara Kategori Umur dan Diagnosa Awal",
    barmode="stack",  # Stacked bar
    text_auto=False,  # Menampilkan angka secara otomatis
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Update tampilan chart
fig12.update_layout(
    xaxis_title="Diagnosa Awal",
    yaxis_title="Jumlah Pasien",
    legend_title="Kategori Umur",
    xaxis_tickangle=-45,
    plot_bgcolor="rgba(0,0,0,0)",  # Background transparan
    margin=dict(l=40, r=40, t=40, b=100)
)

# Tampilkan chart di Streamlit
st.plotly_chart(fig12)

st.title("Jumlah Pasien Per Dokter")

# Hitung jumlah pasien per dokter
doctor_counts = data2['Dokter'].value_counts().reset_index()
doctor_counts.columns = ['Dokter', 'Jumlah Pasien']

# Ambil 15 dokter dengan pasien terbanyak
top_15_doctors = doctor_counts.head(15)

# Buat bar chart interaktif
fig13 = px.bar(
    top_15_doctors, 
    x="Dokter", 
    y="Jumlah Pasien", 
    text="Jumlah Pasien",
    title="Top 15 Dokter dengan Jumlah Pasien Terbanyak",
    color="Jumlah Pasien",
    color_continuous_scale="blues",  # Warna gradasi biru
)

# Update tampilan chart
fig13.update_layout(
    xaxis_title="Dokter",
    yaxis_title="Jumlah Pasien",
    xaxis_tickangle=-45,
    plot_bgcolor="rgba(0,0,0,0)",  # Background transparan
    margin=dict(l=40, r=40, t=40, b=100)
)

# Tampilkan chart di Streamlit
st.plotly_chart(fig13)