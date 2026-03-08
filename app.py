import streamlit as st
import pandas as pd
from datetime import date
import PyPDF2
from docx import Document

# =====================
# CONFIG DASHBOARD
# =====================
st.set_page_config(
    page_title="Dashboard Analisis Sentimen DISDIKBUD Karanganyar",
    layout="wide"
)

# =====================
# CSS GRADASI BIRU & ABU-ABU
# =====================
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
}
.card {
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
h1, h2, h3 {
    color: #0d47a1;
}
.stButton>button {
    background-color: #1976d2;
    color: white;
    border-radius: 10px;
    height: 3em;
}
</style>
""", unsafe_allow_html=True)

# =====================
# HEADER
# =====================
st.markdown("""
<div class="card" style="text-align:center;">
    <h1 style="
        background: linear-gradient(to right, #6c757d, #0d47a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    ">
        🗨️ Dashboard Analisis Sentimen
    </h1>
    <h3 style="
        background: linear-gradient(to right, #6c757d, #1976d2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    ">
        Dinas Pendidikan dan Kebudayaan Kabupaten Karanganyar
    </h3>
</div>
""", unsafe_allow_html=True)

# =====================
# FORM IDENTITAS
# =====================
with st.form("form_identitas"):
    st.subheader("📋 Form Identitas Pengisi")
    nama_pengisi = st.text_input("Nama Pengisi")
    bidang = st.text_input("Bidang Pelayanan")
    tanggal = st.date_input("Tanggal/Hari", value=date.today())
    submit_form = st.form_submit_button("Konfirmasi Identitas")

if submit_form:
    st.success(f"Identitas terdaftar: {nama_pengisi}, Bidang: {bidang}, Tanggal: {tanggal}")

# =====================
# INPUT KOMENTAR
# =====================
st.subheader("💬 Analisis Sentimen Komentar")

uploaded_file = st.file_uploader(
    "Upload PDF / Word / Excel / CSV / TXT",
    type=["pdf", "docx", "xlsx", "csv", "txt"]
)

komentar_list = []

# ===== BACA FILE =====
if uploaded_file:
    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        komentar_list.extend(df.iloc[:, 0].dropna().astype(str).tolist())

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        komentar_list.extend(df.iloc[:, 0].dropna().astype(str).tolist())

    elif filename.endswith(".txt"):
        komentar_list.extend(
            uploaded_file.read().decode("utf-8").splitlines()
        )

    elif filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
        komentar_list.extend(
            [line for line in text.split("\n") if line.strip() != ""]
        )

    elif filename.endswith(".docx"):
        doc = Document(uploaded_file)
        komentar_list.extend(
            [p.text for p in doc.paragraphs if p.text.strip() != ""]
        )

# ===== INPUT MANUAL =====
manual_komentar = st.text_area(
    "Atau tulis komentar manual (satu komentar per baris)"
)

if manual_komentar:
    komentar_list.extend(
        [k for k in manual_komentar.split("\n") if k.strip() != ""]
    )

# =====================
# KAMUS SENTIMEN
# =====================
kata_positif = [
    "bagus", "baik", "sangat baik", "memuaskan", "sangat memuaskan",
    "ramah", "sopan", "cepat", "responsif", "sigap",
    "mantap", "luar biasa", "hebat", "terbaik", "profesional",
    "pelayanan baik", "pelayanan bagus", "pelayanan memuaskan",
    "berkualitas", "bermutu", "efektif", "efisien",
    "jelas", "transparan", "tertib", "rapi",
    "mudah", "praktis", "lancar", "tanpa kendala",
    "membantu", "sangat membantu", "bermanfaat",
    "puas", "sangat puas", "senang", "menyenangkan",
    "apresiasi", "terima kasih", "respon cepat",
    "tepat waktu", "tepat sasaran", "sesuai harapan",
    "komunikatif", "informatif", "edukatif"
]


kata_negatif = [
    "jelek", "buruk", "sangat buruk", "tidak baik",
    "lama", "terlambat", "bertele-tele", "ribet",
    "mengecewakan", "sangat mengecewakan",
    "parah", "payah", "kacau", "amburadul",
    "tidak ramah", "kasar", "jutek", "cuek",
    "pelayanan jelek", "pelayanan buruk",
    "tidak memuaskan", "sangat tidak memuaskan",
    "lemot", "lambat", "tidak responsif",
    "dipersulit", "dipersulit prosesnya",
    "tidak jelas", "membingungkan",
    "tidak transparan", "bermasalah",
    "keluhan", "komplain", "kecewa", "sangat kecewa",
    "marah", "kesal", "frustrasi",
    "tidak profesional", "asal-asalan",
    "salah", "banyak kesalahan",
    "tidak sesuai", "tidak sesuai harapan",
    "tidak membantu", "kurang membantu"
]

def analisis_sentimen(teks):
    teks = str(teks).lower()

    for kata in kata_negatif:
        if kata in teks:
            return "Negatif", "Komentar negatif. Perlu evaluasi dan perbaikan layanan."

    for kata in kata_positif:
        if kata in teks:
            return "Positif", "Komentar positif. Pertahankan kualitas layanan yang sudah baik."

    # Jika tidak ada kata negatif maupun positif → dianggap Positif
    return "Positif", "Komentar positif. Pertahankan kualitas layanan yang sudah baik."


# =====================
# PROSES ANALISIS
# =====================
if st.button("🔍 Deteksi Sentimen"):
    if not komentar_list:
        st.error("Belum ada komentar untuk dianalisis!")
    else:
        results = []
        for k in komentar_list:
            sentimen, saran = analisis_sentimen(k)
            results.append({
                "Komentar": k,
                "Sentimen": sentimen,
                "Saran": saran
            })
        df_results = pd.DataFrame(results)

        df_results.index = range(1, len(df_results) + 1)
        df_results.index.name = "No"

        st.success("Analisis Sentimen Selesai ✅")
        st.dataframe(df_results)


