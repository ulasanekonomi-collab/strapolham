import streamlit as st
import pandas as pd
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="STRAPOLHAM Analytics", layout="wide", page_icon="🌱")

# --- JUDUL & IDENTITAS PENGEMBANG ---
st.title("🌱 STRAPOLHAM")
st.markdown("##### **Dikembangkan oleh Yuhka Sundaya - Ekonomi Pembangunan Unisba**")
st.markdown("---") 
st.markdown("### Analisis Kedalaman Konflik & Visi")

# --- SIDEBAR INPUT & LOGIKA LOAD DATA ---
st.sidebar.header("Konfigurasi & Simulasi")
uploaded_file = st.sidebar.file_uploader("Upload Data Excel (Sheet 1: info, Sheet 2: data)", type=['xlsx'])

if uploaded_file is None:
    # Data dummy agar sistem tidak error saat pertama kali dibuka
    df = pd.DataFrame({
        'Nama': ['Aktor A', 'Aktor B'],
        'Power': [3, 4],
        'Posisi_Isu': [1, -1],
        'Visi': ['Visi A', 'Visi B'],
        'Tipe_Visi': [1, 3],
        'History_Friction': [0, 1]
    })
    st.info("💡 Selamat Datang! Silakan upload file Excel Akang untuk memulai analisis.")
else:
    try:
        # Membaca Sheet ke-2 (index 1) untuk data
        df = pd.read_excel(uploaded_file, sheet_name=1)
    except:
        # Jika sheet 2 tidak ada, balik ke sheet 1
        df = pd.read_excel(uploaded_file, sheet_name=0)

# Pastikan kolom Tipe_Visi ada
if 'Tipe_Visi' not in df.columns:
    df['Tipe_Visi'] = 1

# --- FITUR SIMULASI ---
st.sidebar.divider()
st.sidebar.subheader("🕹️ Simulation Tool")
actor_to_sim = st.sidebar.selectbox("Pilih Aktor untuk Lobi:", df['Nama'].tolist())
current_pos = int(df[df['Nama'] == actor_to_sim]['Posisi_Isu'].values[0])
new_pos = st.sidebar.slider(f"Geser Posisi {actor_to_sim}", -2, 2, current_pos)

# Mapping Bobot Visi
vision_weights = {1: 1.0, 2: 1.2, 3: 1.8}

# Update Data Simulasi
df_sim = df.copy()
df_sim.loc[df_sim['Nama'] == actor_to_sim, 'Posisi_Isu'] = new_pos

# --- CALCULATION ENGINE ---
def get_metrics(data_df):
    weighted_sum = sum(data_df['Power'] * data_df['Posisi_Isu'] * data_df['Tipe_Visi'].map(vision_weights))
    max_possible = sum(data_df['Power'] * 2 * 1.8)
    return weighted_sum / max_possible

phi_ori = get_metrics(df)
phi_sim = get_metrics(df_sim)
status_keb = "KRITIS/RENTAN" if phi_sim < 0.25 else "STABIL/KONDUSIF"

# --- TAMPILAN DASHBOARD ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Strategic Mapping (Simulasi)")
    fig = px.scatter(df_sim, x="Posisi_Isu", y="Power", size="Power", color="Tipe_Visi",
                     hover_name="Visi", text="Nama", range_x=[-2.5, 2.5], range_y=[0, 6],
                     color_continuous_scale="RdYlGn_r")
    fig.add_vline(x=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔬 Metrics & Diagnosa")
    st.metric("Potential Harmony Index (PHI)", f"{phi_sim:.2f}", delta=f"{phi_sim - phi_ori:.2f}")
    conflict_depth = df_sim[df_sim['Tipe_Visi'] == 3]['Power'].sum()
    st.write(f"**Indeks Kedalaman Konflik:** {conflict_depth}")
    st.progress(min(conflict_depth / 15, 1.0))

# --- INTERPRETASI & LAPORAN ---
st.divider()
int_col1, int_col2 = st.columns(2)
with int_col1:
    st.markdown("**1. Status Harmonisasi**")
    st.write(f"Kebijakan berstatus **{status_keb}**.")
with int_col2:
    st.markdown("**2. Residu Konflik**")
    total_friction = df_sim['History_Friction'].sum()
    st.write(f"Terdeteksi {total_friction} friksi historis.")

if st.button("📄 Buat Narasi Laporan Strategis"):
    narasi = f"""HASIL ANALISIS STRAPOLHAM:
Status kebijakan: {status_keb} (PHI: {phi_sim:.2f}). 
Terdapat kedalaman konflik sebesar {conflict_depth}. 
Strategi utama: Pendekatan intensif pada {actor_to_sim}."""
    st.text_area("Draft Laporan:", narasi, height=200)
