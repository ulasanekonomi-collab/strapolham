import streamlit as st
import pandas as pd
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="STRAPOLHAM Analytics", layout="wide", page_icon="🌱")

# --- JUDUL & IDENTITAS PENGEMBANG ---
st.title("🌱 STRAPOLHAM Digital System (v1.1)")
st.markdown("##### **Dikembangkan oleh Yuhka Sundaya - Ekonomi Pembangunan Unisba**")
st.markdown("---") 
st.markdown("### Decision Support System: Analisis Kedalaman Konflik & Visi")

# --- SIDEBAR INPUT & SIMULASI ---
st.sidebar.header("Konfigurasi & Simulasi")
uploaded_file = st.sidebar.file_uploader("Upload Data Aktor (Excel/CSV)", type=['xlsx', 'csv'])

# --- UPDATE BAGIAN LOAD DATA (DUA SHEET) ---
if uploaded_file is not None:
    if uploaded_file.name.endswith('.xlsx'):
        try:
            # Sistem mencoba membaca Sheet ke-2 (index 1) yang bernama 'data'
            df = pd.read_excel(uploaded_file, sheet_name=1) 
        except:
            # Jika Sheet 2 tidak ada atau error, baca sheet pertama (index 0)
            df = pd.read_excel(uploaded_file, sheet_name=0)
    else:
        # Jika file yang diupload adalah CSV
        df = pd.read_csv(uploaded_file)
    
    # Pastikan kolom Tipe_Visi ada, kalau tidak ada kita kasih default 1
    if 'Tipe_Visi' not in df.columns:
        df['Tipe_Visi'] = 1
else:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    if 'Tipe_Visi' not in df.columns:
        df['Tipe_Visi'] = 1 # Default jika kolom belum ada di Excel

# 2. Fitur Simulasi Slider
st.sidebar.divider()
st.sidebar.subheader("🕹️ Simulation Tool")
actor_to_sim = st.sidebar.selectbox("Pilih Aktor untuk Lobi:", df['Nama'].tolist())
current_pos = int(df[df['Nama'] == actor_to_sim]['Posisi_Isu'].values[0])
new_pos = st.sidebar.slider(f"Geser Posisi {actor_to_sim}", -2, 2, current_pos)

# Mapping Bobot Visi: Tipe 3 (Kontra) memperberat dampak posisi
vision_weights = {1: 1.0, 2: 1.2, 3: 1.8}

# Create Simulated Data
df_sim = df.copy()
df_sim.loc[df_sim['Nama'] == actor_to_sim, 'Posisi_Isu'] = new_pos

# --- CALCULATION ENGINE (WITH VISION WEIGHT) ---
def get_metrics(data_df):
    # Rumus PHI Terbobot Visi
    weighted_sum = sum(data_df['Power'] * data_df['Posisi_Isu'] * data_df['Tipe_Visi'].map(vision_weights))
    max_possible = sum(data_df['Power'] * 2 * 1.8) # Normalisasi dengan bobot tertinggi
    phi = weighted_sum / max_possible
    return phi

phi_ori = get_metrics(df)
phi_sim = get_metrics(df_sim)
status_keb = "KRITIS/RENTAN" if phi_sim < 0.25 else "STABIL/KONDUSIF"

# --- DISPLAY UTAMA ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Strategic Mapping (Simulasi)")
    # Tambahkan kategori Tipe Visi di warna atau simbol
    fig = px.scatter(df_sim, x="Posisi_Isu", y="Power", size="Power", color="Tipe_Visi",
                     hover_name="Visi", text="Nama", range_x=[-2.5, 2.5], range_y=[0, 6],
                     color_continuous_scale="RdYlGn_r", title="Peta Kekuatan & Kedalaman Visi")
    fig.add_vline(x=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔬 Metrics & Diagnosa")
    st.metric("Potential Harmony Index (PHI)", f"{phi_sim:.2f}", delta=f"{phi_sim - phi_ori:.2f}")
    
    # Indikator Kedalaman Konflik
    conflict_depth = df_sim[df_sim['Tipe_Visi'] == 3]['Power'].sum()
    st.write(f"**Indeks Kedalaman Konflik:** {conflict_depth}")
    st.progress(min(conflict_depth / 15, 1.0))
    st.caption("Semakin tinggi bar, semakin berat benturan ideologi (Visi Kontra).")

# --- INTERPRETASI RAPI ---
st.divider()
st.subheader("📝 Interpretasi Strategis (Weighted Analysis)")
int_col1, int_col2 = st.columns(2)

with int_col1:
    st.markdown("**1. Status Harmonisasi (Weighted)**")
    st.write(f"Kebijakan ini berada pada level **{status_keb}**. Bobot visi menunjukkan adanya {'resistensi prinsipil' if conflict_depth > 3 else 'ruang negosiasi'} yang kuat.")
    
    st.markdown("**2. Analisis Lobi**")
    st.info(f"Lobi terhadap **{actor_to_sim}** memberikan dampak {'signifikan' if abs(phi_sim - phi_ori) > 0.05 else 'moderat'}. Strategi harus menyesuaikan dengan Tipe Visi aktor tersebut.")

with int_col2:
    st.markdown("**3. Residu Konflik & Visi (Bab 4 & 5)**")
    if (df_sim['Tipe_Visi'] == 3).any():
        st.warning("⚠️ Terdeteksi benturan Visi Ideologis (Tipe 3). Pendekatan transaksional mungkin akan gagal; gunakan pendekatan nilai.")
    else:
        st.success("✅ Visi antar aktor relatif konvergen.")

# --- FITUR NARASI LAPORAN ---
st.divider()
if st.button("📄 Buat Narasi Laporan Strategis"):
    narasi_final = f"""BERDASARKAN ANALISIS STRATEGI POLITIK HARMONIS (STRAPOLHAM) VERSI 1.1:

Kondisi harmonisasi saat ini menunjukkan skor PHI sebesar {phi_sim:.2f} ({status_keb}). Berbeda dengan analisis standar, perhitungan ini telah memasukkan 'Bobot Visi' yang mendeteksi kedalaman benturan prinsip antar aktor.

Ditemukan bahwa hambatan utama bukan sekadar posisi menolak, melainkan adanya ketidaksesuaian visi ideologis (Conflict Depth: {conflict_depth}). Hal ini terlihat pada aktor ber-Tipe Visi 3 yang memerlukan penanganan khusus di luar lobi teknis.

Rekomendasi: Lakukan pendekatan 'Value Alignment' kepada {actor_to_sim}. Jika aktor ini memiliki visi yang berseberangan secara prinsip, maka narasi kebijakan harus di-reframing agar masuk ke dalam koridor visi mereka tanpa mengorbankan tujuan utama kebijakan."""

    st.subheader("📝 Draft Laporan")
    st.text_area("Hasil Narasi:", narasi_final, height=300)
