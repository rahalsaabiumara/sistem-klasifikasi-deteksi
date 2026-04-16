import streamlit as st
from ultralytics import YOLO
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Import semua section
from sections import hero, tentang, fitur, upload, hasil, summary

# ================= CONFIG =================
st.set_page_config(page_title="EduDetect", layout="wide")

# ================= INJECT CSS ANIMASI KE PARENT FRAME =================
st.components.v1.html("""
<script>
(function() {
    var parentDoc = window.parent.document;
    if (parentDoc.getElementById('reveal-style')) return;

    var style = parentDoc.createElement('style');
    style.id  = 'reveal-style';
    style.textContent = `
        .reveal-anim {
            opacity: 0;
            transform: translateY(48px);
            transition: opacity 0.75s cubic-bezier(.4,0,.2,1),
                        transform 0.75s cubic-bezier(.4,0,.2,1);
        }
        .reveal-anim.visible {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
        .reveal-left-anim {
            opacity: 0;
            transform: translateX(-60px);
            transition: opacity 0.75s cubic-bezier(.4,0,.2,1),
                        transform 0.75s cubic-bezier(.4,0,.2,1);
        }
        .reveal-left-anim.visible {
            opacity: 1 !important;
            transform: translateX(0) !important;
        }
        .reveal-right-anim {
            opacity: 0;
            transform: translateX(60px);
            transition: opacity 0.75s cubic-bezier(.4,0,.2,1),
                        transform 0.75s cubic-bezier(.4,0,.2,1);
        }
        .reveal-right-anim.visible {
            opacity: 1 !important;
            transform: translateX(0) !important;
        }
        .reveal-scale-anim {
            opacity: 0;
            transform: scale(0.82);
            transition: opacity 0.65s cubic-bezier(.4,0,.2,1),
                        transform 0.65s cubic-bezier(.4,0,.2,1);
        }
        .reveal-scale-anim.visible {
            opacity: 1 !important;
            transform: scale(1) !important;
        }
    `;
    parentDoc.head.appendChild(style);

    function initObserver() {
        var sel     = '.reveal-anim,.reveal-left-anim,.reveal-right-anim,.reveal-scale-anim';
        var targets = parentDoc.querySelectorAll(sel);
        if (targets.length === 0) { setTimeout(initObserver, 400); return; }

        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var d = entry.target.getAttribute('data-delay') || '0ms';
                    entry.target.style.transitionDelay = d;
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.10, rootMargin: '0px 0px -40px 0px' });

        targets.forEach(function(el) { observer.observe(el); });

        setInterval(function() {
            var newEls = parentDoc.querySelectorAll(sel + ':not([data-observed])');
            newEls.forEach(function(el) {
                el.setAttribute('data-observed', '1');
                observer.observe(el);
            });
        }, 1200);
    }

    setTimeout(initObserver, 900);
})();
</script>
""", height=0)

# ================= SESSION STATE =================
defaults = {
    "scroll_target":       None,
    "show_warning":        None,
    "video_done":          False,
    "auto_scrolled":       False,
    "last_video_name":     None,
    "replay_requested":    False,
    "attentive_history":   [],
    "inattentive_history": [],
    "timeline":            [],
    "final_percent":       0,
    "att_range":           "",
    "inatt_range":         "",
    "opening_text":        "",
    "summary_text":        "",
    "frame_no":            0,
    "last_frame_rgb":      None,
    "last_percent":        0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ================= HELPER FUNCTIONS =================
def anchor(anchor_id: str):
    st.markdown(
        f'<div id="{anchor_id}" style="position:relative;top:-80px;"></div>',
        unsafe_allow_html=True
    )

def anim(cls: str = "reveal-anim", delay: str = "0ms"):
    st.markdown(
        f'<div class="{cls}" data-delay="{delay}">',
        unsafe_allow_html=True
    )

def close_anim():
    st.markdown('</div>', unsafe_allow_html=True)

def trigger_scroll(target_id: str):
    st.components.v1.html(f"""
        <script>
        (function() {{
            var attempts = 0;
            function tryScroll() {{
                var doc = window.parent.document;
                var el  = doc.getElementById("{target_id}");
                if (el) {{
                    el.scrollIntoView({{behavior: "smooth", block: "start"}});
                }} else if (attempts < 10) {{
                    attempts++;
                    setTimeout(tryScroll, 200);
                }}
            }}
            tryScroll();
        }})();
        </script>
    """, height=0)

# ================= SIDEBAR NAVBAR =================
with st.sidebar:
    st.markdown("---")

    if st.button("Tentang", use_container_width=True):
        st.session_state.scroll_target = "section-tentang"
        st.session_state.show_warning  = None

    if st.button("Fitur", use_container_width=True):
        st.session_state.scroll_target = "section-fitur"
        st.session_state.show_warning  = None

    if st.button("Unggah Video", use_container_width=True):
        st.session_state.scroll_target = "section-upload"
        st.session_state.show_warning  = None

    if st.button("Hasil Analisis", use_container_width=True):
        if st.session_state.video_done:
            st.session_state.scroll_target = "section-hasil"
            st.session_state.show_warning  = None
        else:
            st.session_state.show_warning  = "hasil"
            st.session_state.scroll_target = None

    if st.button("Summary AI", use_container_width=True):
        if st.session_state.video_done:
            st.session_state.scroll_target = "section-summary"
            st.session_state.show_warning  = None
        else:
            st.session_state.show_warning  = "summary"
            st.session_state.scroll_target = None

    st.markdown("---")
    st.markdown(
        "<small style='color:gray;'>© 2026 Rahalsa Abi Umara</small>",
        unsafe_allow_html=True
    )

# ================= POPUP PERINGATAN =================
if st.session_state.show_warning == "hasil":
    @st.dialog("⚠️ Video Belum Diunggah")
    def warning_hasil():
        st.warning(
            "Anda belum mengunggah video rekaman CCTV.\n\n"
            "Silahkan unggah video terlebih dahulu agar **Hasil Analisis** dapat ditampilkan."
        )
        if st.button("Oke, Mengerti", type="primary", use_container_width=True):
            st.session_state.show_warning  = None
            st.session_state.scroll_target = "section-upload"
            st.rerun()
    warning_hasil()

elif st.session_state.show_warning == "summary":
    @st.dialog("⚠️ Video Belum Diunggah")
    def warning_summary():
        st.warning(
            "Anda belum mengunggah video rekaman CCTV.\n\n"
            "Silahkan unggah video terlebih dahulu agar **Summary AI** dapat ditampilkan."
        )
        if st.button("Oke, Mengerti", type="primary", use_container_width=True):
            st.session_state.show_warning  = None
            st.session_state.scroll_target = "section-upload"
            st.rerun()
    warning_summary()

# ================= TRIGGER SCROLL =================
if st.session_state.scroll_target:
    trigger_scroll(st.session_state.scroll_target)
    st.session_state.scroll_target = None

# ================= LOAD MODEL =================
model = YOLO("my_model/my_model.pt")

# ===================================================================
# RENDER SEMUA SECTION
# ===================================================================

# 1. Hero
hero.render()

# 2. Tentang
tentang.render(anim, close_anim, anchor)

# 3. Fitur
fitur.render(anim, close_anim, anchor)

# 4. Upload
anchor("section-hasil")  # anchor hasil dipasang sebelum upload agar urut
video_file = upload.render(anim, close_anim, anchor)

# ================= CEK VIDEO BARU =================
if video_file is not None:
    current_video_name = video_file.name
    if current_video_name != st.session_state.last_video_name:
        # Reset semua state jika video berbeda
        for key in ["video_done", "auto_scrolled", "replay_requested"]:
            st.session_state[key] = False
        for key in ["attentive_history", "inattentive_history", "timeline"]:
            st.session_state[key] = []
        for key in ["final_percent", "frame_no", "last_percent"]:
            st.session_state[key] = 0
        for key in ["att_range", "inatt_range", "opening_text", "summary_text"]:
            st.session_state[key] = ""
        st.session_state.last_frame_rgb  = None
        st.session_state.last_video_name = current_video_name

# ================= PROSES VIDEO PERTAMA KALI =================
if video_file is not None and not st.session_state.video_done:

    anim("reveal-anim", "0ms")
    st.subheader("📹 Hasil Analisis Rekaman CCTV")
    close_anim()

    video_bytes = video_file.read()
    result      = hasil.run_analysis(model, video_bytes)

    # Simpan ke session_state
    for key in ["attentive_history", "inattentive_history", "timeline",
                "frame_no", "last_frame_rgb", "last_percent",
                "final_percent", "att_range", "inatt_range", "opening_text"]:
        st.session_state[key] = result[key]

    # Panggil Gemini (hanya sekali)
    with st.spinner("Memproses Summary AI..."):
        st.session_state.summary_text = summary.generate_summary(
            result["final_percent"],
            result["att_range"],
            result["inatt_range"],
            result["frame_no"]
        )

    st.session_state.video_done       = True
    st.session_state.replay_requested = False

    if not st.session_state.auto_scrolled:
        trigger_scroll("section-summary")
        st.session_state.auto_scrolled = True

    # Update state KECUALI summary_text (hasil Gemini tetap sama)
    for key in ["attentive_history", "inattentive_history", "timeline",
                "frame_no", "last_frame_rgb", "last_percent",
                "final_percent", "att_range", "inatt_range", "opening_text"]:
        st.session_state[key] = result[key]

    st.session_state.replay_requested = False

# ================= TAMPILKAN FRAME TERAKHIR + TOMBOL REPLAY =================
elif video_file is not None and st.session_state.video_done:
    hasil.render_static(anim, close_anim, trigger_scroll)

# ================= SUMMARY =================
if st.session_state.video_done:
    summary.render(anim, close_anim, anchor, trigger_scroll)