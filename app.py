import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import scipy.stats as st_stats

# 1. Konfigurasi Halaman
st.set_page_config(page_title="HIGO Analytics 2026", layout="wide")

# Palet Warna Luxury
color_palette = ['#00e5ff', '#7e57c2', '#ff7043', '#f5f5f5', '#444']

# Custom CSS untuk Luxury Dark Mode
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #f5f5f5; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #ffffff; font-weight: 800; letter-spacing: -1px; }
    h2, h3 { color: #00e5ff; font-weight: 600; margin-top: 20px; }
    div[data-testid="stMetricValue"] { color: #00e5ff; font-weight: bold; font-size: 40px; }
    div[data-testid="stMetricLabel"] { color: #c0c0c0; text-transform: uppercase; letter-spacing: 1px; font-size: 12px; }
    .stPlotlyChart { border: 1px solid #222; border-radius: 16px; background-color: #1a1a1a; padding: 15px; }
    .fixed-header {
        position: fixed; top: 0; left: 0; width: 100%;
        background-color: #121212; padding: 10px 50px;
        z-index: 999; border-bottom: 1px solid #333;
    }
    .main .block-container { padding-top: 100px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Load Data
@st.cache_data
def load_data():
    
    df = pd.read_csv('data_dummy_higo_final.csv')
    return df

df_raw = load_data()

# --- 3. FIXED HEADER WITH GLOBAL FILTERS ---
with st.container():
    st.markdown('<div class="fixed-header">', unsafe_allow_html=True)
    header_col1, header_col2, header_col3 = st.columns([2, 1, 1])
    with header_col1:
        st.title("Behavioral & Digital Interest Analytics 2026")
    with header_col2:
        lokasi_options = ["All Locations"] + list(df_raw['Tipe Lokasi'].unique())
        selected_location = st.selectbox("Select Location Type:", lokasi_options)
    with header_col3:
        generasi_options = ["All Generations"] + list(df_raw['Generasi'].unique())
        selected_generation = st.selectbox("Select Generation:", generasi_options)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. LOGIKA FILTERING ---
df = df_raw.copy()
if selected_location != "All Locations":
    df = df[df['Tipe Lokasi'] == selected_location]
if selected_generation != "All Generations":
    df = df[df['Generasi'] == selected_generation]

# 5. Fungsi Confidence Interval (CI)
def get_ci_text(data_series):
    if len(data_series) < 2: return "CI N/A"
    n = len(data_series)
    mean = np.mean(data_series)
    sem = st_stats.sem(data_series)
    h = sem * st_stats.t.ppf((1 + 0.95) / 2, n - 1)
    return f"95% CI: [{mean-h:.2f} - {mean+h:.2f}]"

st.markdown("---")

# --- 6. KPI HEADER ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Login", f"{len(df):,}")
    st.caption(f"Showing {selected_location}")
with col2:
    if len(df) > 0:
        st.metric("Avg. Interest Score", f"{df['Skor Minat Digital'].mean():.2f}")
        st.caption(get_ci_text(df['Skor Minat Digital']))
with col3:
    if len(df) > 0:
        st.markdown("<style>div[data-testid='stBlock']:nth-of-type(3) div[data-testid='stMetricValue'] { color: #ff7043; }</style>", unsafe_allow_html=True)
        st.metric("Average User Age", f"{df['Usia'].mean():.2f}")
        st.caption(get_ci_text(df['Usia']))
with col4:
    if len(df) > 0:
        top_interest = df['Kategori Minat Digital'].mode()[0]
        st.markdown("<style>div[data-testid='stBlock']:nth-of-type(4) div[data-testid='stMetricValue'] { color: #7e57c2; }</style>", unsafe_allow_html=True)
        st.metric("Peak Interest Category", top_interest)
        st.caption("Dominant Interest")

st.markdown("---")

# --- 7. VISUALISASI UTAMA ---

# Baris 1: Demografi & Minat
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    st.subheader("Demographics by Generation")
    fig_gen = px.pie(df, names='Generasi', hole=0.6, color_discrete_sequence=color_palette)
    fig_gen.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white",
                          legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
    st.plotly_chart(fig_gen, use_container_width=True)

with row1_col2:
    st.subheader("Digital Interest Categories")
    df_minat = df.groupby('Kategori Minat Digital')['Nama'].count().reset_index()
    color_map = {'Finance/Investment': '#7e57c2', 'News/Portal': '#f3f4f6', 'Gaming': '#ff7043', 'E-Commerce': '#00e5ff', 'Social Media': '#e91e63'}
    fig_donut = px.pie(df_minat, names='Kategori Minat Digital', values='Nama', hole=0.6, color='Kategori Minat Digital', color_discrete_map=color_map)
    fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white",
                            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
    st.plotly_chart(fig_donut, use_container_width=True)

# Baris 2: Skor & Waktu
row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.subheader("Avg. Interest Score by Location Type")
    df_loc = df.groupby('Tipe Lokasi')['Skor Minat Digital'].mean().reset_index().sort_values('Skor Minat Digital', ascending=True)
    fig_skor = px.bar(df_loc, x='Skor Minat Digital', y='Tipe Lokasi', orientation='h', color='Skor Minat Digital', color_continuous_scale=['#0D47A1', '#00E5FF'])
    fig_skor.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", xaxis=dict(visible=False), yaxis=dict(title=None), coloraxis_showscale=False)
    fig_skor.update_traces(texttemplate='%{x:.2f}', textposition='outside')
    st.plotly_chart(fig_skor, use_container_width=True)

with row2_col2:
    st.subheader("Daily Activity Peak Sessions")
    fig_session = px.histogram(df, y='Sesi Login', orientation='h', category_orders={"Sesi Login": ["Malam", "Sore", "Siang", "Pagi"]},
                               color='Sesi Login', color_discrete_map={'Pagi': '#ff7043', 'Siang': '#deff9a', 'Sore': '#7e57c2', 'Malam': '#00e5ff'})
    fig_session.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False, yaxis=dict(title=None))
    st.plotly_chart(fig_session, use_container_width=True)

# Baris 3: Perangkat Mobile (Baris Baru)
row3_col1, row3_col2 = st.columns([2, 1])
with row3_col1:
    st.subheader("Top Mobile Device Brands")
    if len(df) > 0:
        df_device = df['Merk HP'].value_counts().reset_index().sort_values('count', ascending=True)
        
        # menggunakan gradasi warna (Orange Gelap ke Orange/Coral)
        fig_device = px.bar(
            df_device, 
            x='count', 
            y='Merk HP', 
            orientation='h', 
            color='count', # Menggunakan kolom 'count' sebagai basis gradasi
            color_continuous_scale=['#BF360C', '#FFAB40'] # Gradasi dari Merah Gelap ke Orange
        )
        
        fig_device.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color="white", 
            xaxis=dict(visible=False), 
            yaxis=dict(title=None),
            coloraxis_showscale=False 
        )
        fig_device.update_traces(texttemplate='%{x}', textposition='outside')
        st.plotly_chart(fig_device, use_container_width=True)
    else:
        st.info("No data available.")

with row3_col2:
    st.write("")
    st.info("💡 **Insight:** Fokus pada brand dominan untuk optimasi UI/UX halaman login.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #A6A6A6; font-size: small;'>Data Analyst | Fityan Hanif Assalmi</p>", unsafe_allow_html=True)
