import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
import os

# Konfigurasi Halaman
st.set_page_config(
    page_title="Beijing Air Quality Analytics",
    layout="wide"
)

# Definisi Ikon SVG Vektor Bersih
ICONS = {
    "wind": '<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#4285f4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/></svg>',
    "filter": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>',
    "trend": '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4285f4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>',
    "temp": '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ea4335" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/></svg>',
    "bar": '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#34a853" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-4"/></svg>',
    "map": '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fbbc05" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "smog": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9aa0a6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 6px;"><path d="M5 8h14"/><path d="M4 12h16"/><path d="M7 16h10"/></svg>',
    "db": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9aa0a6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 6px;"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/></svg>',
    "alert": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ea4335" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 6px;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
}

# Styling CSS Card
st.markdown("""
<style>
    .section-title {
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
    }
    .kpi-card {
        background-color: #1e212b;
        border: 1px solid #2d313e;
        border-radius: 8px;
        padding: 14px 18px;
    }
    .kpi-title {
        color: #9aa0a6;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f1f3f4;
    }
</style>
""", unsafe_allow_html=True)

# Load Data Menggunakan Absolute Path Dinamis
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'main_data.csv')
    
    # Fallback jika file berada di root repo
    if not os.path.exists(file_path):
        file_path = 'main_data.csv'
        
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

df = load_data()

# ================= SIDEBAR =================
st.sidebar.markdown(f'<div class="section-title">{ICONS["filter"]} Filter Dashboard</div>', unsafe_allow_html=True)

stations = df['station'].unique().tolist()
selected_station = st.sidebar.selectbox("Pilih Stasiun Pemantauan:", ["Semua Stasiun"] + stations)

min_date = df['datetime'].min().date()
max_date = df['datetime'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter Data
filtered_df = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
if selected_station != "Semua Stasiun":
    filtered_df = filtered_df[filtered_df['station'] == selected_station]

# ================= MAIN CONTENT =================
st.markdown(f'# {ICONS["wind"]} Beijing Air Quality Analytics Dashboard', unsafe_allow_html=True)
st.caption("Dashboard analisis tren polutan PM2.5, faktor meteorologi, dan sebaran spasial kualitas udara (2013–2017).")
st.markdown("<br>", unsafe_allow_html=True)

# ================= BARIS 1: TREN TEMPORAL (KIRI) & KORELASI CUACA (KANAN) =================
row1_left, row1_right = st.columns([1, 1], gap="medium")
with row1_left:
    st.markdown(f'<div class="section-title">{ICONS["trend"]} Tren Konsentrasi Rata-rata PM2.5 Bulanan</div>', unsafe_allow_html=True)
    monthly_trend = filtered_df.set_index('datetime').resample('ME')['PM2.5'].mean().reset_index()
    fig1, ax1 = plt.subplots(figsize=(6, 3.9))
    ax1.plot(monthly_trend['datetime'], monthly_trend['PM2.5'], color='#1f77b4', linewidth=2, marker='o', markersize=3)
    ax1.axhline(y=15, color='#2ecc71', linestyle='--', linewidth=1.5, label='Baku Mutu WHO (15 µg/m³)')
    ax1.set_ylabel("PM2.5 (µg/m³)", fontsize=9)
    ax1.set_xlabel("Periode Pengamatan", fontsize=9)
    ax1.legend(loc="upper right", frameon=True, fontsize=8)
    ax1.grid(True, linestyle=':', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig1)
with row1_right:
    st.markdown(f'<div class="section-title">{ICONS["temp"]} Korelasi Parameter Meteorologi terhadap PM2.5</div>', unsafe_allow_html=True)
    weather_vars = ['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    corr = filtered_df[weather_vars].corr()['PM2.5'].drop('PM2.5').sort_values()
    fig2, ax2 = plt.subplots(figsize=(6, 3.9))
    bar_colors = ['#d93025' if x < 0 else '#1a73e8' for x in corr.values]
    corr.plot(kind='barh', ax=ax2, color=bar_colors, edgecolor='black', alpha=0.85)
    ax2.axvline(0, color='grey', linewidth=0.8)
    ax2.set_xlabel("Koefisien Korelasi Pearson (r)", fontsize=9)
    ax2.set_ylabel("Parameter Cuaca", fontsize=9)
    ax2.grid(True, linestyle=':', alpha=0.5)
    for i, v in enumerate(corr):
        ax2.text(v + (0.01 if v >= 0 else -0.04), i, f"{v:.2f}", va='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig2)
st.markdown("<br>", unsafe_allow_html=True)


# 4. DISTRIBUSI AQI & PETA FOLIUM (PERTANYAAN 3 & ANALISIS LANJUTAN)
col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown(f'<div class="section-title">{ICONS["bar"]} Distribusi Kategori Kualitas Udara (AQI)</div>', unsafe_allow_html=True)
    category_order = ['Good', 'Moderate', 'Unhealthy for Sensitive', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
    aqi_counts = filtered_df['AQI_Category'].value_counts().reindex(category_order, fill_value=0)
    
    fig3, ax3 = plt.subplots(figsize=(6, 4.2))
    aqi_colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c', '#c0392b', '#7f0000']
    aqi_counts.plot(kind='bar', ax=ax3, color=aqi_colors, edgecolor='black', alpha=0.85)
    ax3.set_ylabel("Frekuensi (Jam)", fontsize=10)
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=35, ha='right', fontsize=9)
    ax3.grid(True, axis='y', linestyle=':', alpha=0.5)
    st.pyplot(fig3)

with col_b:
    st.markdown(f'<div class="section-title">{ICONS["map"]} Peta Spasial Sebaran Stasiun Beijing</div>', unsafe_allow_html=True)
    station_locations = {
        'station': ['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 
                    'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'],
        'lat': [39.982, 40.217, 40.292, 39.929, 39.929, 39.914, 40.328, 39.933, 40.127, 39.886, 39.987, 39.878],
        'lon': [116.397, 116.230, 116.220, 116.417, 116.339, 116.184, 116.628, 116.460, 116.655, 116.407, 116.287, 116.352]
    }
    geo_df = pd.DataFrame(station_locations)
    station_stats = filtered_df.groupby('station')['PM2.5'].mean().reset_index()
    geo_data = pd.merge(geo_df, station_stats, on='station')

    beijing_map = folium.Map(
        location=[40.05, 116.4], 
        zoom_start=9, 
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', 
        attr='Esri'
    )

    for _, row in geo_data.iterrows():
        color = 'red' if row['PM2.5'] > 80 else 'orange' if row['PM2.5'] > 70 else 'green'
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['PM2.5']/4.5,
            popup=f"<b>{row['station']}</b><br>PM2.5: {row['PM2.5']:.2f} µg/m³",
            tooltip=f"{row['station']}: {row['PM2.5']:.2f} µg/m³",
            color=color, fill=True, fill_color=color, fill_opacity=0.7, weight=2
        ).add_to(beijing_map)

    st_folium(beijing_map, height=415, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Copyright © 2026 - Beijing Air Quality Analytics Project | Dicoding Submission", text_alignment='center')