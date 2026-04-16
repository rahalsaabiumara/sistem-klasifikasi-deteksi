import streamlit as st
import google.generativeai as genai


def generate_summary(final_percent: int, att_range: str, inatt_range: str, frame_no: int) -> str:
    """
    Panggil Gemini API dan kembalikan teks evaluasi.
    Prioritas: Streamlit Secrets → .env / environment variable.
    """
    import os
    from dotenv import load_dotenv
    load_dotenv()

    api_key = st.secrets.get("GEMINI_API_KEY", None)
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


def _stat_cards(final_percent: int, att_range: str, inatt_range: str):
    """Tiga kartu statistik ringkasan di atas summary."""
    pct_color = "#10b981" if final_percent >= 50 else "#ef4444"
    pct_label = "Baik ✓" if final_percent >= 50 else "Perlu Perhatian ⚠"

    st.components.v1.html(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
  * {{ box-sizing:border-box; margin:0; padding:0; }}

  :root {{
    --sc-bg:     #ffffff;
    --sc-border: rgba(229,231,235,0.9);
    --sc-title:  #6b7280;
    --sc-val:    #1f2937;
    --sc-sub:    #9ca3af;
  }}
  .sc-dark {{
    --sc-bg:     #1e2330;
    --sc-border: rgba(255,255,255,0.08);
    --sc-title:  #64748b;
    --sc-val:    #f1f5f9;
    --sc-sub:    #475569;
  }}

  .stat-row {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px;
    margin-bottom: 24px;
    font-family: 'Plus Jakarta Sans', sans-serif;
  }}

  .stat-card {{
    background: var(--sc-bg);
    border: 1px solid var(--sc-border);
    border-radius: 16px;
    padding: 20px 18px;
    position: relative;
    overflow: hidden;
    opacity: 0;
    animation: fadeUp 0.6s ease forwards;
  }}

  .stat-card:nth-child(1) {{ animation-delay: 0.10s; }}
  .stat-card:nth-child(2) {{ animation-delay: 0.22s; }}
  .stat-card:nth-child(3) {{ animation-delay: 0.34s; }}

  .stat-card::before {{
    content:'';
    position:absolute; top:0; left:0; right:0; height:3px;
    border-radius:16px 16px 0 0;
  }}

  .stat-card.c-green::before  {{ background: linear-gradient(90deg,#10b981,#3b82f6); }}
  .stat-card.c-blue::before   {{ background: linear-gradient(90deg,#3b82f6,#6366f1); }}
  .stat-card.c-red::before    {{ background: linear-gradient(90deg,#ef4444,#f59e0b); }}
  .stat-card.c-orange::before {{ background: linear-gradient(90deg,#f59e0b,#ef4444); }}

  .stat-icon  {{ font-size:24px; margin-bottom:10px; }}
  .stat-label {{ font-size:11px; font-weight:700; text-transform:uppercase;
                 letter-spacing:1px; color:var(--sc-title); margin-bottom:6px; }}
  .stat-value {{ font-size:22px; font-weight:800; color:var(--sc-val); line-height:1.2; }}
  .stat-sub   {{ font-size:11px; color:var(--sc-sub); margin-top:4px; font-weight:500; }}

  @keyframes fadeUp {{
    from {{ opacity:0; transform:translateY(18px); }}
    to   {{ opacity:1; transform:translateY(0); }}
  }}
</style>

<div class="stat-row" id="stat-root">
  <div class="stat-card {'c-green' if final_percent >= 50 else 'c-red'}">
    <div class="stat-icon">{'📈' if final_percent >= 50 else '📉'}</div>
    <div class="stat-label">Persentase Perhatian</div>
    <div class="stat-value" style="color:{pct_color};">{final_percent}%</div>
    <div class="stat-sub">{pct_label}</div>
  </div>
  <div class="stat-card c-green">
    <div class="stat-icon">🟢</div>
    <div class="stat-label">Waktu Memperhatikan</div>
    <div class="stat-value" style="font-size:15px;margin-top:4px;">{att_range}</div>
    <div class="stat-sub">Rentang waktu aktif</div>
  </div>
  <div class="stat-card c-orange">
    <div class="stat-icon">🔴</div>
    <div class="stat-label">Waktu Tidak Memperhatikan</div>
    <div class="stat-value" style="font-size:15px;margin-top:4px;">{inatt_range}</div>
    <div class="stat-sub">Rentang waktu tidak aktif</div>
  </div>
</div>

<script>
(function() {{
  var root = document.getElementById('stat-root');
  function applyTheme() {{
    var html = window.parent.document.documentElement;
    var body = window.parent.document.body;
    var dark = html.getAttribute('data-theme') === 'dark' ||
               body.classList.contains('dark') ||
               window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.classList.toggle('sc-dark', dark);
  }}
  applyTheme();
  new MutationObserver(applyTheme).observe(window.parent.document.documentElement,
    {{ attributes:true, attributeFilter:['data-theme','class'] }});
  new MutationObserver(applyTheme).observe(window.parent.document.body,
    {{ attributes:true, attributeFilter:['class','data-theme'] }});
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
}})();
</script>
""", height=145)


def _summary_header(opening_text: str):
    """Header section summary dengan styling profesional."""
    is_good   = "cukup baik" in opening_text
    grad      = "linear-gradient(135deg,rgba(16,185,129,0.08),rgba(59,130,246,0.07))" if is_good \
                else "linear-gradient(135deg,rgba(245,158,11,0.08),rgba(239,68,68,0.07))"
    brd       = "rgba(16,185,129,0.22)" if is_good else "rgba(245,158,11,0.28)"
    icon_grad = "linear-gradient(135deg,#10b981,#3b82f6)" if is_good \
                else "linear-gradient(135deg,#f59e0b,#ef4444)"
    icon_em   = "🎯" if is_good else "⚠️"

    st.components.v1.html(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
  * {{ box-sizing:border-box; margin:0; padding:0; }}

  :root {{
    --sh-text: #1f2937;
    --sh-sub:  #6b7280;
  }}
  .sh-dark {{ --sh-text:#f1f5f9; --sh-sub:#94a3b8; }}

  .sum-header {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 22px 26px;
    background: {grad};
    border: 1px solid {brd};
    border-radius: 18px;
    margin-bottom: 20px;
    animation: fadeUp 0.6s ease forwards;
    opacity: 0;
  }}

  .sh-icon {{
    width: 54px; height: 54px;
    background: {icon_grad};
    border-radius: 16px;
    display: flex; align-items:center; justify-content:center;
    font-size: 26px;
    flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  }}

  .sh-title {{
    font-size: 16px;
    font-weight: 800;
    color: var(--sh-text);
    line-height: 1.4;
  }}

  .sh-sub {{
    font-size: 12.5px;
    color: var(--sh-sub);
    margin-top: 4px;
    font-weight: 500;
  }}

  @keyframes fadeUp {{
    from {{ opacity:0; transform:translateY(16px); }}
    to   {{ opacity:1; transform:translateY(0); }}
  }}
</style>

<div class="sum-header" id="sh-root">
  <div class="sh-icon">{icon_em}</div>
  <div>
    <div class="sh-title">{opening_text}</div>
    <div class="sh-sub">Ringkasan evaluasi berdasarkan analisis seluruh frame video</div>
  </div>
</div>

<script>
(function() {{
  var root = document.getElementById('sh-root');
  function applyTheme() {{
    var html = window.parent.document.documentElement;
    var body = window.parent.document.body;
    var dark = html.getAttribute('data-theme') === 'dark' ||
               body.classList.contains('dark') ||
               window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.classList.toggle('sh-dark', dark);
  }}
  applyTheme();
  new MutationObserver(applyTheme).observe(window.parent.document.documentElement,
    {{ attributes:true, attributeFilter:['data-theme','class'] }});
  new MutationObserver(applyTheme).observe(window.parent.document.body,
    {{ attributes:true, attributeFilter:['class','data-theme'] }});
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
}})();
</script>
""", height=110)


def _ai_result_card(summary_text: str):
    """Card header khusus sebelum konten AI."""
    st.components.v1.html("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
  * { box-sizing:border-box; margin:0; padding:0; }

  :root {
    --ai-bg:  linear-gradient(135deg,rgba(139,92,246,0.07),rgba(59,130,246,0.06));
    --ai-brd: rgba(139,92,246,0.22);
    --ai-txt: #1f2937;
    --ai-sub: #6b7280;
  }
  .ai-dark {
    --ai-bg:  linear-gradient(135deg,rgba(139,92,246,0.14),rgba(59,130,246,0.10));
    --ai-brd: rgba(139,92,246,0.35);
    --ai-txt: #f1f5f9;
    --ai-sub: #94a3b8;
  }

  .ai-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 18px 22px;
    background: var(--ai-bg);
    border: 1px solid var(--ai-brd);
    border-radius: 16px;
    margin-bottom: 12px;
    animation: fadeUp 0.6s ease 0.15s forwards;
    opacity: 0;
  }

  .ai-icon-wrap {
    width: 48px; height: 48px;
    background: linear-gradient(135deg,#8b5cf6,#3b82f6);
    border-radius: 14px;
    display:flex; align-items:center; justify-content:center;
    font-size:22px; flex-shrink:0;
    box-shadow: 0 4px 14px rgba(139,92,246,0.28);
  }

  .ai-title { font-size:16px; font-weight:800; color:var(--ai-txt); margin-bottom:3px; }
  .ai-sub   { font-size:12px; color:var(--ai-sub); font-weight:500; }

  /* Animated badge */
  .ai-live {
    margin-left:auto;
    display:flex; align-items:center; gap:6px;
    font-size:11px; font-weight:700;
    background:rgba(139,92,246,0.12);
    border:1px solid rgba(139,92,246,0.25);
    color:#7c3aed;
    padding:5px 14px; border-radius:999px;
  }

  .ai-dot {
    width:7px; height:7px;
    background:#8b5cf6; border-radius:50%;
    animation: pulse 1.8s ease infinite;
  }

  @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(1.5)} }
  @keyframes fadeUp { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:translateY(0)} }
</style>

<div class="ai-header" id="ai-root">
  <div class="ai-icon-wrap">🤖</div>
  <div>
    <div class="ai-title">Hasil Evaluasi & Rekomendasi AI</div>
    <div class="ai-sub">Dihasilkan oleh Gemini AI berdasarkan data analisis video</div>
  </div>
  <div class="ai-live"><div class="ai-dot"></div>Gemini AI</div>
</div>

<script>
(function() {
  var root = document.getElementById('ai-root');
  function applyTheme() {
    var html = window.parent.document.documentElement;
    var body = window.parent.document.body;
    var dark = html.getAttribute('data-theme') === 'dark' ||
               body.classList.contains('dark') ||
               window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.classList.toggle('ai-dark', dark);
  }
  applyTheme();
  new MutationObserver(applyTheme).observe(window.parent.document.documentElement,
    { attributes:true, attributeFilter:['data-theme','class'] });
  new MutationObserver(applyTheme).observe(window.parent.document.body,
    { attributes:true, attributeFilter:['class','data-theme'] });
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
})();
</script>
""", height=88)


def render(anim, close_anim, anchor, trigger_scroll_fn):
    """Render section Summary AI dari session_state."""
    anchor("section-summary")

    # ── Divider ──
    st.markdown("---")

    # ── Header hasil evaluasi ──
    anim("reveal-scale-anim", "0ms")
    _summary_header(st.session_state.opening_text)
    close_anim()

    # ── Tiga stat cards ──
    anim("reveal-anim", "80ms")
    _stat_cards(
        st.session_state.final_percent,
        st.session_state.att_range,
        st.session_state.inatt_range
    )
    close_anim()

    # ── AI result card header ──
    anim("reveal-anim", "160ms")
    _ai_result_card(st.session_state.summary_text)
    close_anim()

    # ── Konten summary ──
    anim("reveal-anim", "240ms")
    summary = st.session_state.summary_text
    if summary.startswith("__ERROR__:"):
        st.error(f"❌ Gagal mengambil respons dari Gemini: {summary.replace('__ERROR__:', '')}")
        st.info("Pastikan:\n- API Key valid\n- Model `gemini-3-flash-preview` tersedia\n- Koneksi internet aktif")
    elif summary == "__NO_KEY__":
        st.error("API Key Gemini tidak tersedia. Tambahkan GEMINI_API_KEY ke file .env")
    else:
        st.success("✅ Evaluasi AI berhasil dibuat!")
        st.markdown(summary)
    close_anim()

    # ── Re-trigger scroll observer ──
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
