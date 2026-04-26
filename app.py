import streamlit as st
import pandas as pd
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="STRAPOLHAM Analytics", layout="wide", page_icon="🌱")

st.title("🌱 STRAPOLHAM Digital System")
st.markdown("### Decision Support System untuk Harmonisasi Kebijakan")

# --- SIDEBAR INPUT & SIMULASI ---
st.sidebar.header("Konfigurasi & Simulasi")
uploaded_file = st.sidebar.file_uploader("Upload Data Aktor (Excel/CSV)", type=['xlsx', 'csv'])

# 1. Load Data
if uploaded_file is None:
    st.sidebar.warning("Gunakan data simulasi...")
    data = {
        'Nama': ['BEMU', 'BEMF', 'HMI', 'KAMMI', 'MTB', 'REKTORAT'],
        'Power': [3, 2, 4, 4, 4, 4],
        'Posisi_Isu': [1, -1, -2, 1, 1, 2],
        'Visi': ['Merdeka', 'Program', 'Islam', 'Islam', 'Kemanusiaan', 'Unggul'],
        'History_Friction': [1, 0, 1, 1, 1, 1]
    }
    df = pd.DataFrame(data)
else:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)

# 2. Fitur Simulasi Slider
st.sidebar.divider()
st.sidebar.subheader("🕹️ Simulation Tool")
actor_to_sim = st.sidebar.selectbox("Pilih Aktor untuk Lobi:", df['Nama'].tolist())
current_pos = int(df[df['Nama'] == actor_to_sim]['Posisi_Isu'].values[0])
new_pos = st.sidebar.slider(f"Geser Posisi {actor_to_sim}", -2, 2, current_pos)

# Create Simulated Data
df_sim = df.copy()
df_sim.loc[df_sim['Nama'] == actor_to_sim, 'Posisi_Isu'] = new_pos

# --- CALCULATION ENGINE ---
def get_metrics(data_df):
    phi = (data_df['Power'] * data_df['Posisi_Isu']).sum() / (data_df['Power'].sum() * 2)
    return phi

phi_ori = get_metrics(df)
phi_sim = get_metrics(df_sim)
status_keb = "KRITIS/RENTAN" if phi_sim < 0.3 else "STABIL/KONDUSIF"

# --- DISPLAY UTAMA ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Strategic Mapping (Simulasi)")
    fig = px.scatter(df_sim, x="Posisi_Isu", y="Power", size="Power", color="Nama",
                     hover_name="Visi", text="Nama", range_x=[-2.5, 2.5], range_y=[0, 6])
    fig.add_vline(x=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔬 Metrics & Diagnosa")
    st.metric("Potential Harmony Index (PHI)", f"{phi_sim:.2f}", delta=f"{phi_sim - phi_ori:.2f}")
    
    if phi_sim < 0.3:
        st.error(f"Status: {status_keb}")
    else:
        st.success(f"Status: {status_keb}")

# --- INTERPRETASI RAPI ---
st.divider()
st.subheader("📝 Interpretasi Strategis")
int_col1, int_col2 = st.columns(2)

with int_col1:
    st.markdown("**1. Status Harmonisasi**")
    st.write(f"Kebijakan ini berada pada level **{status_keb}**. Energi konvergensi kepentingan memerlukan orkestrasi tambahan.")
    
    st.markdown("**2. Variabel Kunci**")
    st.info(f"Aktor **{actor_to_sim}** diidentifikasi sebagai variabel kunci. Pergeseran posisinya berdampak signifikan pada stabilitas harmoni.")

with int_col2:
    st.markdown("**3. Residu Konflik (Bab 4)**")
    total_friction = df_sim['History_Friction'].sum()
    if total_friction > 0:
        st.warning(f"Terdeteksi residu konflik pada {total_friction} aktor. Gunakan 'Bridging Actor'!")
    else:
        st.success("Hambatan historis minimal.")

    st.markdown("**4. Rekomendasi Eksekusi**")
    st.write("👉 Fokus pada 'Interest Reframing' dan lobi informal sebelum implementasi teknis dilakukan.")

# --- FITUR NARASI LAPORAN ---
st.divider()
if st.button("📄 Buat Narasi Laporan Strategis"):
    narasi_final = f"""BERDASARKAN ANALISIS STRATEGI POLITIK HARMONIS (STRAPOLHAM):

Kondisi harmonisasi kebijakan saat ini berada pada tingkat yang {status_keb} dengan skor PHI sebesar {phi_sim:.2f}. Angka ini menunjukkan bahwa ruang konvergensi kepentingan masih memerlukan orkestrasi yang lebih mendalam.

Strategi prioritas adalah melakukan pendekatan intensif kepada {actor_to_sim} guna menggeser posisinya ke arah yang lebih kooperatif. Simulasi menunjukkan kenaikan harmoni sebesar {phi_sim - phi_ori:+.2f}.

Disarankan melibatkan mediator independen untuk mengatasi 'History Friction' yang terdeteksi, guna memastikan keberlanjutan kebijakan di masa depan."""

    st.subheader("📝 Draft Laporan (Copy-Paste)")
    st.text_area("Hasil Narasi:", narasi_final, height=300)
