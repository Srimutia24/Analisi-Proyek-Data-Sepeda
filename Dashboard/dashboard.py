import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Dashboard Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Adding custom CSS for the dashboard style
st.markdown("""
<style>
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #1E88E5;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #43A047;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #1E88E5;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Function to load and prepare the data with caching
@st.cache_data
def load_data(start_date, end_date):
    try:
        hours_df = pd.read_csv("hour_df.csv")
        days_df = pd.read_csv("day_df.csv")
        
        # Convert date columns to datetime format
        days_df['dteday'] = pd.to_datetime(days_df['dteday'], errors='coerce')  # Convert invalid dates to NaT
        
        # Remove rows where 'dteday' is NaT (invalid date)
        days_df = days_df.dropna(subset=['dteday'])
        
        # Filter data based on the selected date range
        days_df = days_df[(days_df['dteday'] >= pd.to_datetime(start_date)) & 
                           (days_df['dteday'] <= pd.to_datetime(end_date))]
        
        return hours_df, days_df
    except FileNotFoundError:
        st.error("File data tidak ditemukan. Pastikan file 'hour_df.csv' dan 'day_df.csv' ada di direktori aplikasi.")
        return None, None

# Sidebar for filter options using date input
st.sidebar.title("Navigasi")

# Date range selection using calendar
start_date = st.sidebar.date_input("Pilih Tanggal Mulai", datetime(2011, 1, 1))
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", datetime(2012, 12, 31))

# Display selected date range in sidebar
st.sidebar.write(f"Rentang Waktu: {start_date} - {end_date}")

# Load filtered data based on the date range
hours_df, days_df = load_data(start_date, end_date)

# Check if data was successfully loaded
if hours_df is None or days_df is None:
    st.stop()

# Memastikan nilai min dan max tanggal bukan NaT sebelum memformat
min_date = days_df['dteday'].min()
max_date = days_df['dteday'].max()

# Cek apakah min_date dan max_date adalah NaT
if pd.isna(min_date) or pd.isna(max_date):
    st.error("Data tanggal tidak lengkap, pastikan ada data yang valid.")
else:
    min_date = min_date.strftime('%d %B %Y')
    max_date = max_date.strftime('%d %B %Y')

# Menampilkan rentang waktu yang dipilih
st.markdown(f"Periode Data: {min_date} - {max_date}")

# Data Overview Page
st.header(f"Data Overview untuk {start_date} hingga {end_date}")
st.subheader("Dataset Penyewaan Sepeda Harian")
st.dataframe(days_df.head())

# Main Header
st.markdown('<div class="main-header">🚲 Dashboard Penyewaan Sepeda</div>', unsafe_allow_html=True)

# Key Metrics
st.markdown('<div class="sub-header">📊 Metrik Utama</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    total_rentals = days_df['cnt'].sum()  # Total rentals based on 'cnt'
    st.metric("Total Penyewaan", f"{total_rentals:,}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    daily_avg = days_df['cnt'].mean()
    st.metric("Rata-rata per Hari", f"{daily_avg:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    if not days_df.empty:
        max_day = days_df.loc[days_df['cnt'].idxmax()]
        st.metric("Penyewaan Tertinggi", f"{int(max_day['cnt']):,}", 
                  f"{max_day['dteday'].strftime('%d %b %Y')}")
    else:
        st.metric("Penyewaan Tertinggi", "Tidak ada data")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    if not days_df.empty:
        min_day = days_df.loc[days_df['cnt'].idxmin()]
        st.metric("Penyewaan Terendah", f"{int(min_day['cnt']):,}", 
                  f"{min_day['dteday'].strftime('%d %b %Y')}")
    else:
        st.metric("Penyewaan Terendah", "Tidak ada data")
    st.markdown('</div>', unsafe_allow_html=True)

# Pertanyaan 1: Bagaimana penggunaan sepeda berubah seiring dengan variasi musim dan kondisi cuaca?
st.markdown("### Pertanyaan 1: Bagaimana penggunaan sepeda berubah seiring dengan variasi musim dan kondisi cuaca?")
st.markdown("""
    *Jawaban:*
    - Pergantian musim dan kondisi cuaca sangat mempengaruhi jumlah peminjaman sepeda.
    - Musim gugur menunjukkan tingkat penyewaan tertinggi, sementara musim semi mencatatkan angka terendah.
    - Cuaca cerah mendorong penggunaan sepeda yang lebih tinggi dibandingkan dengan kondisi cuaca lainnya.
""")
st.markdown('<div class="sub-header">📈 Penggunaan Sepeda Berdasarkan Musim dan Cuaca</div>', unsafe_allow_html=True)
plt.figure(figsize=(12,6))
sns.barplot(x='season', y='cnt', data=days_df, palette='Spectral', estimator='mean')
plt.xlabel('Musim', fontsize=12)
plt.ylabel('Rata-rata Peminjaman Sepeda', fontsize=12)
plt.title('📈 Rata-rata Peminjaman Sepeda Berdasarkan Musim', fontsize=14, weight='bold')
plt.xticks([0, 1, 2, 3], ['Spring', 'Summer', 'Fall', 'Winter'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

# Pertanyaan 2: Bagaimana perbedaan perilaku penyewaan sepeda antara hari kerja, hari libur dan akhir pekan?
st.markdown("### Pertanyaan 2: Bagaimana perbedaan perilaku penyewaan sepeda antara hari kerja, hari libur dan akhir pekan?")
st.markdown("""
    *Jawaban:*
    - Hari kerja menunjukkan dua puncak peminjaman utama, pada pagi dan sore hari, sementara akhir pekan memiliki pola lebih merata.
    - Pengguna casual lebih banyak di akhir pekan, sementara pengguna registered dominan di hari kerja.
""")
st.markdown('<div class="sub-header">📅 Pola Penyewaan Berdasarkan Tipe Hari</div>', unsafe_allow_html=True)
avg_by_type = days_df.groupby('day_type')['cnt'].mean().reindex(['Hari Kerja', 'Akhir Pekan', 'Hari Libur Nasional'])
plt.figure(figsize=(10,6))
sns.barplot(x=avg_by_type.index, y=avg_by_type.values, palette='coolwarm')
plt.xlabel('Tipe Hari')
plt.ylabel('Rata-rata Jumlah Peminjaman Sepeda')
plt.title('Perbandingan Rata-rata Peminjaman Sepeda berdasarkan Tipe Hari')
plt.grid(True, linestyle='--', alpha=0.7, axis='y')
st.pyplot(plt)

# Pertanyaan 3: Faktor-faktor apa saja yang mempengaruhi intensitas penyewaan sepeda?
st.markdown("### Pertanyaan 3: Faktor-faktor apa saja yang mempengaruhi intensitas penyewaan sepeda?")
st.markdown("""
    *Jawaban:*
    - Faktor cuaca, suhu, dan kelembapan berhubungan langsung dengan jumlah peminjaman.
    - Pengguna registered berkontribusi lebih banyak pada penyewaan sepeda dibandingkan pengguna casual.
""")
st.markdown('<div class="sub-header">🔍 Faktor yang Mempengaruhi Intensitas Peminjaman</div>', unsafe_allow_html=True)
plt.figure(figsize=(12, 8))
numeric_cols = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
correlation = days_df[numeric_cols].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, cbar_kws={'label': 'Korelasi'})
plt.title('🔍 Korelasi antara Variabel Numerik dan Jumlah Peminjaman', fontsize=14, weight='bold')
st.pyplot(plt)

# Conclusion and Strategy Recommendations
st.markdown('<div class="sub-header">🎯 Kesimpulan dan Rekomendasi</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="highlight">
        <h4>Kesimpulan:</h4>
        <ol>
            <li>Pola penyewaan sepeda menunjukkan tren yang jelas berdasarkan waktu (jam), musim, dan kondisi cuaca.</li>
            <li>Faktor cuaca dan suhu memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda.</li>
            <li>Terdapat perbedaan pola penyewaan antara hari kerja dan akhir pekan, yang menunjukkan perbedaan perilaku pengguna.</li>
        </ol>
    </div>
    <div class="highlight">
        <h4>Rekomendasi:</h4>
        <ol>
            <li><strong>Manajemen Armada:</strong> Sesuaikan jumlah sepeda yang tersedia berdasarkan jam sibuk dan hari dalam seminggu.</li>
            <li><strong>Promosi:</strong> Lakukan promosi khusus pada musim atau kondisi cuaca yang biasanya memiliki jumlah penyewaan rendah.</li>
            <li><strong>Perawatan:</strong> Jadwalkan pemeliharaan armada sepeda pada waktu-waktu dengan aktivitas penyewaan yang rendah.</li>
            <li><strong>Prediksi Permintaan:</strong> Gunakan data historis dan prakiraan cuaca untuk memprediksi permintaan di masa mendatang.</li>
        </ol>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>📊 <strong>Dashboard Penyewaan Sepeda</strong> &copy; 2025</p>
    <p>Created with ❤ using Streamlit</p>
</div>
""", unsafe_allow_html=True)