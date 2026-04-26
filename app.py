# --- BAGIAN INTERPRETASI STRATEGIS (VERSI RAPI) ---
st.divider()
st.subheader("📝 Interpretasi Strategis")

# Membuat kolom agar poin-poin tidak terlalu memanjang ke bawah
int_col1, int_col2 = st.columns(2)

with int_col1:
    st.markdown(f"**1. Status Harmonisasi Kebijakan**")
    if phi_sim < 0.3:
        st.error(f"Skor PHI: {phi_sim:.2f} (KRITIS). Kebijakan ini masih sangat rentan terhadap penolakan masif.")
    else:
        st.success(f"Skor PHI: {phi_sim:.2f} (STABIL). Kebijakan memiliki basis dukungan yang cukup untuk eksekusi.")

    st.markdown(f"**2. Analisis Aktor Terkuat**")
    st.info(f"Menggeser posisi **{actor_to_sim}** ke angka {new_pos} memberikan dampak perubahan harmoni sebesar {phi_sim - phi_ori:+.2f}. Ini menunjukkan {actor_to_sim} adalah variabel kunci.")

with int_col2:
    st.markdown(f"**3. Residu Konflik (History Friction)**")
    total_friction = df_sim['History_Friction'].sum()
    if total_friction > 0:
        st.warning(f"Terdeteksi {total_friction} aktor memiliki residu konflik masa lalu. Penanganan teknis saja tidak cukup; dibutuhkan pendekatan personal/informal.")
    else:
        st.success("Tidak terdeteksi hambatan historis yang signifikan antar aktor kunci.")

    st.markdown(f"**4. Rekomendasi Eksekusi STRAPOLHAM**")
    if phi_sim < 0.3:
        st.write("👉 Lakukan *Interest Reframing*. Narasi kebijakan harus diubah agar menyentuh kepentingan ekonomi/ego aktor yang menolak.")
    else:
        st.write("👉 Lakukan *Policy Implementation*. Fokus pada penjagaan koalisi agar tidak terjadi 'backsliding' dari aktor pendukung.")
# --- FITUR GENERATOR NARASI LAPORAN (TAMBAHKAN DI PALING BAWAH) ---
st.divider()
if st.button("📄 Buat Narasi Laporan Strategis"):
    # Menentukan status berdasarkan PHI
    status_keb = "KRITIS/RENTAN" if phi_sim < 0.3 else "STABIL/KONDUSIF"
    
    # Merangkai narasi gaya deduktif
    narasi_final = f"""BERDASARKAN ANALISIS STRATEGI POLITIK HARMONIS (STRAPOLHAM):

Kondisi harmonisasi kebijakan saat ini berada pada tingkat yang {status_keb} dengan skor PHI sebesar {phi_sim:.2f}. Angka ini menunjukkan bahwa ruang konvergensi kepentingan masih memerlukan orkestrasi yang lebih mendalam, terutama dalam memitigasi resistensi dari aktor-aktor strategis.

Strategi prioritas yang direkomendasikan adalah melakukan pendekatan intensif kepada {actor_to_sim} guna menggeser posisinya ke arah yang lebih kooperatif. Melalui simulasi lobi, perubahan posisi aktor ini terbukti mampu meningkatkan stabilitas harmoni secara signifikan sebesar {phi_sim - phi_ori:+.2f}.

Selain faktor posisi, temuan lapangan menunjukkan adanya residu konflik historis (History Friction) yang cukup kental di antara para aktor kunci. Oleh karena itu, disarankan untuk tidak hanya mengandalkan pendekatan teknis-formal, melainkan juga melibatkan 'Bridging Actor' atau mediator independen guna mencairkan kebuntuan komunikasi dan memastikan keberlanjutan kebijakan di masa depan."""

    # Menampilkan hasil narasi dalam kotak teks yang bisa di-copy
    st.subheader("📝 Draft Laporan (Copy-Paste ke Word/WA)")
    st.text_area("Hasil Narasi:", narasi_final, height=350)
    st.info("💡 Tips: Narasi di atas sudah menggunakan gaya deduktif sesuai standar laporan STRAPOLHAM.")
