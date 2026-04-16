import streamlit as st


def render(anim, close_anim, anchor):
    """
    Render section upload video — tampilan interaktif dengan animasi.
    Mengembalikan objek file yang diupload (atau None jika belum ada).
    """
    anchor("section-upload")

    # ── Inject custom upload area styling ──
    st.components.v1.html("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  /* ── Variables light ── */
  :root {
    --up-bg:          #ffffff;
    --up-border:      rgba(99,102,241,0.35);
    --up-border-hov:  rgba(99,102,241,0.70);
    --up-bg-hov:      rgba(99,102,241,0.04);
    --up-title:       #1f2937;
    --up-sub:         #6b7280;
    --up-badge-bg:    rgba(99,102,241,0.08);
    --up-badge-txt:   #4f46e5;
    --up-badge-brd:   rgba(99,102,241,0.20);
    --up-tip-bg:      rgba(59,130,246,0.05);
    --up-tip-brd:     rgba(59,130,246,0.15);
    --up-tip-txt:     #374151;
    --up-step-txt:    #4b5563;
    --up-step-num-bg: linear-gradient(135deg,#6366f1,#8b5cf6);
  }

  /* ── Variables dark ── */
  .dark-mode {
    --up-bg:          #1e2330;
    --up-border:      rgba(139,92,246,0.40);
    --up-border-hov:  rgba(139,92,246,0.75);
    --up-bg-hov:      rgba(139,92,246,0.08);
    --up-title:       #f1f5f9;
    --up-sub:         #94a3b8;
    --up-badge-bg:    rgba(139,92,246,0.15);
    --up-badge-txt:   #a78bfa;
    --up-badge-brd:   rgba(139,92,246,0.30);
    --up-tip-bg:      rgba(59,130,246,0.10);
    --up-tip-brd:     rgba(59,130,246,0.25);
    --up-tip-txt:     #cbd5e1;
    --up-step-txt:    #94a3b8;
    --up-step-num-bg: linear-gradient(135deg,#6366f1,#8b5cf6);
  }

  /* ── Wrapper ── */
  .upload-wrapper {
    font-family: 'Plus Jakarta Sans', sans-serif;
    padding: 8px 4px 20px;
  }

  /* ── Section header ── */
  .section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 24px;
    opacity: 0;
    animation: fadeUp 0.6s ease 0.05s forwards;
  }

  .section-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: linear-gradient(90deg, rgba(99,102,241,0.12), rgba(139,92,246,0.12));
    border: 1px solid rgba(99,102,241,0.28);
    color: #4f46e5;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 999px;
  }

  .pill-dot {
    width: 6px; height: 6px;
    background: #6366f1;
    border-radius: 50%;
    animation: pulse 2s ease infinite;
  }

  @keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%     { opacity:0.4; transform:scale(1.5); }
  }

  .section-title {
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(135deg,#4f46e5,#8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* ── Drop-zone card ── */
  .dropzone-card {
    background: var(--up-bg);
    border: 2px dashed var(--up-border);
    border-radius: 20px;
    padding: 44px 32px;
    text-align: center;
    transition: border-color 0.3s ease, background 0.3s ease, transform 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    opacity: 0;
    animation: fadeUp 0.7s ease 0.15s forwards;
  }

  .dropzone-card::before {
    content:'';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(99,102,241,0.07), transparent 70%);
    pointer-events: none;
  }

  .dropzone-card:hover {
    border-color: var(--up-border-hov);
    background: var(--up-bg-hov);
    transform: translateY(-3px);
  }

  /* Animated ring around icon */
  .upload-icon-wrap {
    position: relative;
    width: 90px; height: 90px;
    margin: 0 auto 20px;
  }

  .upload-icon {
    width: 90px; height: 90px;
    background: linear-gradient(135deg, rgba(99,102,241,0.14), rgba(139,92,246,0.14));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    position: relative;
    z-index: 1;
    transition: transform 0.3s ease;
  }

  .dropzone-card:hover .upload-icon { transform: scale(1.08); }

  .ring {
    position: absolute;
    inset: -8px;
    border-radius: 50%;
    border: 2px solid rgba(99,102,241,0.25);
    animation: ringPulse 2.4s ease infinite;
  }

  .ring2 {
    position: absolute;
    inset: -18px;
    border-radius: 50%;
    border: 2px solid rgba(139,92,246,0.14);
    animation: ringPulse 2.4s ease 0.6s infinite;
  }

  @keyframes ringPulse {
    0%,100% { opacity:0.8; transform:scale(1); }
    50%     { opacity:0.3; transform:scale(1.06); }
  }

  .dropzone-title {
    font-size: 17px;
    font-weight: 700;
    color: var(--up-title);
    margin-bottom: 8px;
  }

  .dropzone-sub {
    font-size: 13px;
    color: var(--up-sub);
    margin-bottom: 20px;
    line-height: 1.55;
  }

  /* Format badges */
  .badge-row {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 8px;
  }

  .badge {
    background: var(--up-badge-bg);
    border: 1px solid var(--up-badge-brd);
    color: var(--up-badge-txt);
    font-size: 11px;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 999px;
    letter-spacing: 0.5px;
  }

  /* ── Steps row ── */
  .steps-row {
    display: flex;
    justify-content: center;
    gap: 0;
    margin: 28px 0 0;
    flex-wrap: wrap;
    opacity: 0;
    animation: fadeUp 0.6s ease 0.30s forwards;
  }

  .step-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    flex: 1;
    min-width: 120px;
    position: relative;
  }

  /* connector line between steps */
  .step-item:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 20px;
    right: -50%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, rgba(99,102,241,0.3), rgba(139,92,246,0.1));
  }

  .step-num {
    width: 40px; height: 40px;
    background: var(--up-step-num-bg);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 800;
    color: white;
    position: relative;
    z-index: 1;
    box-shadow: 0 4px 12px rgba(99,102,241,0.30);
  }

  .step-icon { font-size: 18px; }

  .step-label {
    font-size: 11.5px;
    font-weight: 600;
    color: var(--up-step-txt);
    text-align: center;
    line-height: 1.4;
  }

  /* ── Tip card ── */
  .tip-card {
    margin-top: 20px;
    background: var(--up-tip-bg);
    border: 1px solid var(--up-tip-brd);
    border-radius: 14px;
    padding: 14px 20px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    opacity: 0;
    animation: fadeUp 0.6s ease 0.45s forwards;
  }

  .tip-icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }

  .tip-text {
    font-size: 12.5px;
    color: var(--up-tip-txt);
    line-height: 1.6;
    font-weight: 500;
  }

  .tip-text strong { color: #4f46e5; font-weight: 700; }

  @keyframes fadeUp {
    from { opacity:0; transform:translateY(22px); }
    to   { opacity:1; transform:translateY(0); }
  }
</style>

<div class="upload-wrapper" id="upload-root">

  <!-- Header -->
  <div class="section-header">
    <div class="section-pill"><span class="pill-dot"></span>Upload</div>
    <h2 class="section-title">Unggah Video Rekaman CCTV</h2>
  </div>

  <!-- Steps -->
  <div class="steps-row">
    <div class="step-item">
      <div class="step-num">1</div>
      <div class="step-icon">📹</div>
      <div class="step-label">Unggah<br>Video</div>
    </div>
    <div class="step-item">
      <div class="step-num">2</div>
      <div class="step-icon">🔍</div>
      <div class="step-label">Deteksi &amp;<br>Klasifikasi</div>
    </div>
    <div class="step-item">
      <div class="step-num">3</div>
      <div class="step-icon">📊</div>
      <div class="step-label">Lihat<br>Hasil Analisis</div>
    </div>
    <div class="step-item">
      <div class="step-num">4</div>
      <div class="step-icon">🤖</div>
      <div class="step-label">Hasil<br>Evaluasi AI</div>
    </div>
  </div>

  <!-- Tip -->
  <div class="tip-card">
    <div class="tip-icon">💡</div>
    <div class="tip-text">
      <strong>Tips:</strong> Pastikan video rekaman CCTV memiliki kualitas yang cukup baik
      (tidak terlalu gelap/blur) agar akurasi deteksi optimal.
    </div>
  </div>

</div>

<script>
(function() {
  var root = document.getElementById('upload-root');
  function applyTheme() {
    var html = window.parent.document.documentElement;
    var body = window.parent.document.body;
    var dark = html.getAttribute('data-theme') === 'dark' ||
               body.classList.contains('dark') ||
               window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.classList.toggle('dark-mode', dark);
  }
  applyTheme();
  new MutationObserver(applyTheme).observe(window.parent.document.documentElement,
    { attributes: true, attributeFilter: ['data-theme','class'] });
  new MutationObserver(applyTheme).observe(window.parent.document.body,
    { attributes: true, attributeFilter: ['class','data-theme'] });
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
})();
</script>
""", height=350)

    # ── Real Streamlit file uploader ──
    video_file = st.file_uploader(
        "Pilih file video rekaman CCTV untuk dianalisis",
        type=["mp4"],
        help="Upload video rekaman CCTV dalam format untuk dianalisis"
    )

    return video_file
