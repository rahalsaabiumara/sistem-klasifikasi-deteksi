import streamlit as st


def render(anim, close_anim, anchor):
    """Render section Fitur — dengan dark mode support."""
    anchor("section-fitur")

    st.components.v1.html("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  /* ══════════════════════════════════════
     CSS VARIABLES — Light mode (default)
  ══════════════════════════════════════ */
  :root {
    --bg-card:          #ffffff;
    --bg-summary:       linear-gradient(135deg, rgba(59,130,246,0.06), rgba(16,185,129,0.06));
    --border-card:      rgba(229,231,235,0.9);
    --border-summary:   rgba(59,130,246,0.12);

    --text-card-title:  #1f2937;
    --text-card-desc:   #6b7280;
    --text-summary:     #4b5563;
    --text-subtitle:    #9ca3af;

    --shadow-hover:     rgba(0,0,0,0.09);
    --border-hover:     rgba(139,92,246,0.2);
  }

  /* ══════════════════════════════════════
     CSS VARIABLES — Dark mode
  ══════════════════════════════════════ */
  .dark-mode {
    --bg-card:          #1e2330;
    --bg-summary:       linear-gradient(135deg, rgba(59,130,246,0.12), rgba(16,185,129,0.10));
    --border-card:      rgba(255,255,255,0.08);
    --border-summary:   rgba(59,130,246,0.25);

    --text-card-title:  #f1f5f9;
    --text-card-desc:   #94a3b8;
    --text-summary:     #cbd5e1;
    --text-subtitle:    #64748b;

    --shadow-hover:     rgba(0,0,0,0.40);
    --border-hover:     rgba(139,92,246,0.35);
  }

  /* ── Wrapper ── */
  .fitur-wrapper {
    font-family: 'Plus Jakarta Sans', sans-serif;
    padding: 8px 4px 24px;
  }

  /* ── Header ── */
  .section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 32px;
    opacity: 0;
    animation: fadeUp 0.6s ease 0.05s forwards;
  }

  .section-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: linear-gradient(90deg, rgba(16,185,129,0.12), rgba(59,130,246,0.12));
    border: 1px solid rgba(16,185,129,0.28);
    color: #059669;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 999px;
  }

  .pill-dot {
    width: 6px; height: 6px;
    background: #059669;
    border-radius: 50%;
    animation: pulse 2s ease infinite;
  }

  @keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%     { opacity: 0.4; transform: scale(1.5); }
  }

  .section-title {
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(135deg, #1d4ed8, #059669);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* ── Subtitle ── */
  .section-subtitle {
    font-size: 14px;
    color: var(--text-subtitle);
    margin-bottom: 28px;
    font-weight: 500;
    opacity: 0;
    animation: fadeUp 0.6s ease 0.15s forwards;
  }

  /* ── Cards grid ── */
  .fitur-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 16px;
  }

  .fitur-card {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 18px;
    padding: 24px 22px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
    opacity: 0;
    transition: transform 0.28s cubic-bezier(0.34,1.56,0.64,1),
                box-shadow 0.28s ease,
                border-color 0.28s ease;
    position: relative;
    overflow: hidden;
  }

  .fitur-card:nth-child(1) { animation: fadeUp 0.55s ease 0.20s forwards; }
  .fitur-card:nth-child(2) { animation: fadeUp 0.55s ease 0.30s forwards; }
  .fitur-card:nth-child(3) { animation: fadeUp 0.55s ease 0.40s forwards; }
  .fitur-card:nth-child(4) { animation: fadeUp 0.55s ease 0.50s forwards; }
  .fitur-card:nth-child(5) { animation: fadeUp 0.55s ease 0.60s forwards; }
  .fitur-card:nth-child(6) { animation: fadeUp 0.55s ease 0.70s forwards; }

  /* top accent bar */
  .fitur-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 18px 18px 0 0;
    opacity: 0;
    transition: opacity 0.28s ease;
  }

  .fitur-card:hover::before { opacity: 1; }

  .fitur-card.c1::before { background: linear-gradient(90deg, #3b82f6, #6366f1); }
  .fitur-card.c2::before { background: linear-gradient(90deg, #8b5cf6, #ec4899); }
  .fitur-card.c3::before { background: linear-gradient(90deg, #10b981, #3b82f6); }
  .fitur-card.c4::before { background: linear-gradient(90deg, #f59e0b, #ef4444); }
  .fitur-card.c5::before { background: linear-gradient(90deg, #06b6d4, #3b82f6); }
  .fitur-card.c6::before { background: linear-gradient(90deg, #8b5cf6, #10b981); }

  .fitur-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 14px 32px var(--shadow-hover);
    border-color: var(--border-hover);
  }

  /* Number badge */
  .card-number {
    position: absolute;
    top: 18px; right: 18px;
    font-size: 11px;
    font-weight: 700;
    color: rgba(156,163,175,0.5);
    letter-spacing: 1px;
  }

  /* Icon bubble */
  .card-icon-wrap {
    width: 48px; height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
    transition: transform 0.25s ease;
  }

  .fitur-card:hover .card-icon-wrap { transform: scale(1.1) rotate(-4deg); }

  .bg-blue   { background: linear-gradient(135deg, rgba(59,130,246,0.14), rgba(99,102,241,0.14)); }
  .bg-purple { background: linear-gradient(135deg, rgba(139,92,246,0.14), rgba(236,72,153,0.14)); }
  .bg-green  { background: linear-gradient(135deg, rgba(16,185,129,0.14), rgba(59,130,246,0.14)); }
  .bg-orange { background: linear-gradient(135deg, rgba(245,158,11,0.14), rgba(239,68,68,0.14)); }
  .bg-cyan   { background: linear-gradient(135deg, rgba(6,182,212,0.14),  rgba(59,130,246,0.14)); }
  .bg-indigo { background: linear-gradient(135deg, rgba(139,92,246,0.14), rgba(16,185,129,0.14)); }

  .card-content { flex: 1; }

  .card-title {
    font-size: 14.5px;
    font-weight: 700;
    color: var(--text-card-title);
    margin-bottom: 6px;
    line-height: 1.3;
  }

  .card-desc {
    font-size: 12.5px;
    color: var(--text-card-desc);
    line-height: 1.55;
    font-weight: 500;
  }

  /* ── Bottom summary bar ── */
  .summary-bar {
    margin-top: 24px;
    background: var(--bg-summary);
    border: 1px solid var(--border-summary);
    border-radius: 16px;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    gap: 14px;
    opacity: 0;
    animation: fadeUp 0.6s ease 0.80s forwards;
  }

  .summary-icon { font-size: 22px; }

  .summary-text {
    font-size: 13px;
    color: var(--text-summary);
    line-height: 1.6;
    font-weight: 500;
  }

  .summary-text strong {
    color: #2563eb;
    font-weight: 700;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
  }
</style>

<div class="fitur-wrapper" id="fitur-root">

  <!-- Header -->
  <div class="section-header">
    <div class="section-pill">
      <span class="pill-dot"></span>
      Fitur
    </div>
    <h2 class="section-title">Fitur Unggulan</h2>
  </div>

  <p class="section-subtitle">Semua yang Anda butuhkan untuk menganalisis aktivitas pembelajaran siswa</p>

  <!-- Cards grid -->
  <div class="fitur-grid">

    <div class="fitur-card c1">
      <div class="card-number">01</div>
      <div class="card-icon-wrap bg-blue">🎥</div>
      <div class="card-content">
        <div class="card-title">Input Video CCTV</div>
        <div class="card-desc">Unggah video rekaman CCTV aktivitas kelas langsung ke sistem untuk diproses</div>
      </div>
    </div>

    <div class="fitur-card c2">
      <div class="card-number">02</div>
      <div class="card-icon-wrap bg-purple">🔍</div>
      <div class="card-content">
        <div class="card-title">Deteksi Objek</div>
        <div class="card-desc">YOLOv11 mendeteksi setiap siswa secara akurat di setiap frame video</div>
      </div>
    </div>

    <div class="fitur-card c3">
      <div class="card-number">03</div>
      <div class="card-icon-wrap bg-green">🧠</div>
      <div class="card-content">
        <div class="card-title">Klasifikasi Aktivitas</div>
        <div class="card-desc">Mengklasifikasikan siswa: <strong style="color:#059669">memperhatikan</strong> vs <strong style="color:#dc2626">tidak memperhatikan</strong></div>
      </div>
    </div>

    <div class="fitur-card c4">
      <div class="card-number">04</div>
      <div class="card-icon-wrap bg-orange">📊</div>
      <div class="card-content">
        <div class="card-title">Visualisasi Hasil</div>
        <div class="card-desc">Tampilkan bounding box berwarna dengan label klasifikasi pada video</div>
      </div>
    </div>

    <div class="fitur-card c5">
      <div class="card-number">05</div>
      <div class="card-icon-wrap bg-cyan">📈</div>
      <div class="card-content">
        <div class="card-title">Persentase Perhatian</div>
        <div class="card-desc">Hitung dan tampilkan persentase tingkat perhatian siswa secara keseluruhan</div>
      </div>
    </div>

    <div class="fitur-card c6">
      <div class="card-number">06</div>
      <div class="card-icon-wrap bg-indigo">🤖</div>
      <div class="card-content">
        <div class="card-title">Insight & Rekomendasi AI</div>
        <div class="card-desc">Menghasilkan insight dan rekomendasi dari AI untuk meningkatkan pembelajaran</div>
      </div>
    </div>

  </div>

  <!-- Summary bar -->
  <div class="summary-bar">
    <div class="summary-icon">✨</div>
    <div class="summary-text">
      Semua fitur dirancang untuk membantu guru mendapatkan <strong>insight berbasis data</strong>
      guna meningkatkan kualitas dan efektivitas proses pembelajaran di kelas.
    </div>
  </div>

</div>

<script>
// Deteksi dark mode dari parent Streamlit dan toggle class .dark-mode
(function() {
  var root = document.getElementById('fitur-root');

  function applyTheme() {
    var parentDoc = window.parent.document;
    var htmlEl    = parentDoc.documentElement;
    var bodyEl    = parentDoc.body;
    var isDark    =
      htmlEl.getAttribute('data-theme') === 'dark' ||
      bodyEl.classList.contains('dark') ||
      window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (isDark) {
      root.classList.add('dark-mode');
    } else {
      root.classList.remove('dark-mode');
    }
  }

  applyTheme();

  // Pantau perubahan tema secara dinamis
  var observer = new MutationObserver(applyTheme);
  observer.observe(window.parent.document.documentElement, {
    attributes: true, attributeFilter: ['data-theme', 'class']
  });
  observer.observe(window.parent.document.body, {
    attributes: true, attributeFilter: ['class', 'data-theme']
  });

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
})();
</script>
""", height=500)
    st.divider()