import streamlit as st
import google.generativeai as genai


def generate_summary(final_percent: int, att_range: str, inatt_range: str, frame_no: int) -> str:
    """
    Panggil Gemini API dan kembalikan teks evaluasi.
    Mengembalikan string biasa, atau string dengan prefix
    '__ERROR__:' / '__NO_KEY__' jika gagal.

    Prioritas pengambilan API key:
    1. st.secrets (Streamlit Cloud deployment)
    2. os.getenv / .env file (localhost)
    """
    import os
    from dotenv import load_dotenv
    load_dotenv()

    # Coba ambil dari Streamlit Secrets (untuk deployment di Streamlit Cloud)
    api_key = st.secrets.get("GEMINI_API_KEY", None)

    # Fallback ke environment variable / .env (untuk localhost)
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "__NO_KEY__"

    genai.configure(api_key=api_key)
    try:
        gemini_model = genai.GenerativeModel("gemini-3-flash-preview")
        prompt = f"""
Buatkan evaluasi pembelajaran berdasarkan data berikut:

- Persentase siswa memperhatikan: {final_percent}%
- Rentang waktu siswa memperhatikan: {att_range}
- Rentang waktu siswa tidak memperhatikan: {inatt_range}
- Total frame dianalisis: {frame_no}

Jelaskan dalam Bahasa Indonesia:
1. Insight kondisi kelas berdasarkan persentase perhatian
2. Apa yang perlu diperbaiki
3. Saran konkret untuk guru agar pembelajaran lebih efektif
"""
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"__ERROR__:{str(e)}"


def render(anim, close_anim, anchor, trigger_scroll_fn):
    """Render section Summary AI dari session_state."""
    anchor("section-summary")
    st.markdown("---")

    anim("reveal-scale-anim", "0ms")
    st.markdown(f"## {st.session_state.opening_text}")
    close_anim()

    anim("reveal-anim", "100ms")
    st.markdown(f"**Persentase Memperhatikan Secara Keseluruhan:** {st.session_state.final_percent}%")
    st.markdown(f"- 🟢 Rentang waktu memperhatikan: `{st.session_state.att_range}`")
    st.markdown(f"- 🔴 Rentang waktu tidak memperhatikan: `{st.session_state.inatt_range}`")
    close_anim()

    anim("reveal-anim", "200ms")
    st.markdown("### 🤖 Hasil Summary AI")
    close_anim()

    anim("reveal-anim", "300ms")
    summary = st.session_state.summary_text
    if summary.startswith("__ERROR__:"):
        st.error(f"❌ Gagal mengambil respons dari Gemini: {summary.replace('__ERROR__:', '')}")
        st.info("Pastikan:\n- API Key valid\n- Model `gemini-3-flash-preview` tersedia\n- Koneksi internet aktif")
    elif summary == "__NO_KEY__":
        st.error("API Key Gemini tidak tersedia. Tambahkan GEMINI_API_KEY ke file .env")
    else:
        st.success("Evaluasi AI berhasil dibuat!")
        st.markdown(summary)
    close_anim()

    # Re-trigger observer untuk elemen baru
    st.components.v1.html("""
    <script>
    setTimeout(function() {
        var parentDoc = window.parent.document;
        var sel = '.reveal-anim:not(.visible),.reveal-left-anim:not(.visible),.reveal-right-anim:not(.visible),.reveal-scale-anim:not(.visible)';
        var obs = new IntersectionObserver(function(entries) {
            entries.forEach(function(e) {
                if (e.isIntersecting) {
                    e.target.style.transitionDelay = e.target.getAttribute('data-delay') || '0ms';
                    e.target.classList.add('visible');
                }
            });
        }, { threshold: 0.10, rootMargin: '0px 0px -40px 0px' });
        parentDoc.querySelectorAll(sel).forEach(function(el) { obs.observe(el); });
    }, 500);
    </script>
    """, height=0)