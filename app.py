import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="STRAPOLHAM Analytics", layout="wide", page_icon="🌱")

# --- JUDUL & HEADER ---
st.title("🌱 STRAPOLHAM Digital System")
st.markdown("### Decision Support System untuk Harmonisasi Kebijakan")
st.info("Berdasarkan Teori Strategi Politik Harmonis oleh Yuhka Sundaya")

# --- SIDEBAR INPUT ---
st.sidebar.header("Konfigurasi Analisis")
uploaded_file = st.sidebar.file_uploader("Upload Data Aktor (Excel/CSV)", type=['xlsx', 'csv'])

# Data Dummy untuk Demonstrasi jika belum ada file
if uploaded_file is None:
    st.sidebar.warning("Silakan upload file. Menggunakan data simulasi...")
    data = {
        'Nama': ['Dinas Lingkungan', 'Investor Swasta', 'LSM Lokal', 'Komunitas Warga', 'Sektor Informal'],
        'Power': [5, 4, 3, 2, 1],
        'Posisi_Isu': [2, 2, -1, -2, -1],
        'Visi': ['Regulasi', 'Profit', 'Advokasi', 'Sosial', 'Ekonomi'],
        'History_Friction': [0, 0, 1, 0, 0]
    }
    df = pd.DataFrame(data)
else:
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

# --- FUNGSI ENGINE DIAGNOSA ---
def jalankan_diagnosa(df):
    laporan = []
    
    # Bab 4: Dendam Organisasi
    if df['History_Friction'].sum() > 0:
        laporan.append({"model": "Bab 4", "judul": "Dendam Organisasi", "aksi": "Tunjuk 'Bridging Actor' untuk mediasi informal."})
    
    # Bab 7: Asimetri Kekuasaan
    if df['Power'].max() - df['Power'].min() >= 4:
        laporan.append({"model": "Bab 7", "judul": "Asimetri Kekuasaan", "aksi": "Lakukan 'Empowerment' pada aktor lemah agar tidak terjadi dominasi sepihak."})

    # Bab 9: Hidden Agenda (Power rendah tapi vokal ekstrim)
    hidden = df[(df['Power'] <= 2) & (abs(df['Posisi_Isu']) == 2)]
    if not hidden.empty:
        laporan.append({"model": "Bab 9", "judul": "Potensi Hidden Agenda", "aksi": f"Lakukan pendekatan personal pada: {', '.join(hidden['Nama'].tolist())}."})

    return laporan

# --- LAYOUT UTAMA ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Strategic Mapping")
    fig = px.scatter(df, x="Posisi_Isu", y="Power", 
                     size="Power", color="Nama",
                     hover_name="Visi", text="Nama",
                     range_x=[-2.5, 2.5], range_y=[0, 6])
    fig.add_vline(x=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔬 Hasil Diagnosa")
    hasil = jalankan_diagnosa(df)
    
    # Kalkulasi PHI
    phi = (df['Power'] * df['Posisi_Isu']).sum() / (df['Power'].sum() * 2)
    st.metric("Potential Harmony Index (PHI)", f"{phi:.2f}")

    for h in hasil:
        with st.expander(f"🚩 {h['judul']} ({h['model']})"):
            st.write(f"**Eksekusi Praktik:** {h['aksi']}")
# --- TAMBAHKAN KODE INI DI BAGIAN BAWAH app.py ---

st.subheader("📝 Interpretasi Strategis (Gaya Deduktif)")

# Logika kalkulasi untuk interpretasi
if phi < 0.3:
    status_kebijakan = "KRITIS/RENTAN"
    saran_utama = "Segera lakukan 'Interest Reframing' dan mediasi informal."
else:
    status_kebijakan = "STABIL/KONDUSIF"
    saran_utama = "Lanjutkan ke fase implementasi teknis."

# Menampilkan poin penting
st.markdown(f"""
1. **Status Harmonisasi Kebijakan:** Kondisi saat ini berada pada level **{status_kebijakan}** dengan skor PHI **{phi:.2f}**. Hal ini menunjukkan bahwa energi pertentangan masih cukup kuat untuk menghambat stabilitas kebijakan.
2. **Kekuatan Oposisi Dominan:** Keberadaan aktor dengan *Power* tinggi di zona negatif (seperti HMI) menjadi faktor penentu rendahnya PHI. Tanpa akomodasi kepentingan terhadap aktor ini, kebijakan berisiko mengalami *deadlock*.
3. **Residu Konflik Historis:** Tingginya angka *History Friction* pada hampir seluruh aktor kunci menandakan bahwa komunikasi rasional terhambat oleh memori organisasi masa lalu.
4. **Rekomendasi Eksekusi:** {saran_utama} Gunakan *Bridging Actor* untuk memutus kebuntuan antara Rektorat dan faksi mahasiswa yang menolak.
""")
st.divider()
st.caption("STRAPOLHAM v1.0 - Digital Transformation of Academic Research")
