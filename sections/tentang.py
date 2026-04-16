import streamlit as st


def render(anim, close_anim, anchor):
    """Render section Tentang EduDetect — dengan dark mode support."""
    anchor("section-tentang")

    st.components.v1.html("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  /* ══════════════════════════════════════
     CSS VARIABLES — Light mode (default)
  ══════════════════════════════════════ */
  :root {
    --bg-card:          #ffffff;
    --bg-main-card:     linear-gradient(135deg, rgba(59,130,246,0.05) 0%, rgba(139,92,246,0.04) 50%, rgba(16,185,129,0.04) 100%);
    --bg-legend:        linear-gradient(135deg, rgba(16,185,129,0.06), rgba(239,68,68,0.06));
    --bg-feat-card:     #ffffff;

    --border-main:      rgba(139,92,246,0.15);
    --border-feat:      rgba(229,231,235,0.8);
    --border-legend:    rgba(107,114,128,0.12);

    --text-body:        #4b5563;
    --text-title:       #1f2937;
    --text-card-title:  #1f2937;
    --text-feat-desc:   #6b7280;
    --text-legend-sub:  #9ca3af;
    --text-legend-main: #374151;
    --text-legend-label:#9ca3af;
    --text-subtitle:    #6b7280;

    --shadow-hover:     rgba(0,0,0,0.08);
  }

  /* ══════════════════════════════════════
     CSS VARIABLES — Dark mode
  ══════════════════════════════════════ */
  .dark-mode {
    --bg-card:          #1e2330;
    --bg-main-card:     linear-gradient(135deg, rgba(59,130,246,0.10) 0%, rgba(139,92,246,0.09) 50%, rgba(16,185,129,0.08) 100%);
    --bg-legend:        linear-gradient(135deg, rgba(16,185,129,0.10), rgba(239,68,68,0.10));
    --bg-feat-card:     #1e2330;

    --border-main:      rgba(139,92,246,0.30);
    --border-feat:      rgba(255,255,255,0.08);
    --border-legend:    rgba(255,255,255,0.10);

    --text-body:        #cbd5e1;
    --text-title:       #f1f5f9;
    --text-card-title:  #f1f5f9;
    --text-feat-desc:   #94a3b8;
    --text-legend-sub:  #64748b;
    --text-legend-main: #e2e8f0;
    --text-legend-label:#64748b;
    --text-subtitle:    #94a3b8;

    --shadow-hover:     rgba(0,0,0,0.35);
  }

  /* ── Wrapper ── */
  .tentang-wrapper {
    font-family: 'Plus Jakarta Sans', sans-serif;
    padding: 8px 4px 24px;
  }

  /* ── Section header ── */
  .section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 28px;
    opacity: 0;
    animation: fadeUp 0.6s ease 0.1s forwards;
  }

  .section-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: linear-gradient(90deg, rgba(59,130,246,0.12), rgba(139,92,246,0.12));
    border: 1px solid rgba(139,92,246,0.25);
    color: #7c3aed;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 999px;
  }

  .pill-dot {
    width: 6px; height: 6px;
    background: #7c3aed;
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
    background: linear-gradient(135deg, #1d4ed8, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* ── Main card ── */
  .main-card {
    background: var(--bg-main-card);
    border: 1px solid var(--border-main);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    opacity: 0;
    animation: fadeUp 0.7s ease 0.2s forwards;
  }

  .main-card::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(139,92,246,0.12), transparent 70%);
    pointer-events: none;
  }

  .main-card::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 140px; height: 140px;
    background: radial-gradient(circle, rgba(59,130,246,0.10), transparent 70%);
    pointer-events: none;
  }

  .card-icon-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
  }

  .card-icon {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, #3b82f6, #7c3aed);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(124,58,237,0.28);
  }

  .card-title-text {
    font-size: 17px;
    font-weight: 700;
    color: var(--text-card-title);
  }

  .card-body {
    font-size: 14.5px;
    line-height: 1.75;
    color: var(--text-body);
    position: relative;
    z-index: 1;
  }

  .highlight-green { color: #059669; font-weight: 700; }
  .highlight-red   { color: #dc2626; font-weight: 700; }
  .highlight-blue  { color: #2563eb; font-weight: 700; }

  /* ── Feature mini-cards grid ── */
  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px;
    margin-bottom: 24px;
  }

  .feat-card {
    background: var(--bg-feat-card);
    border: 1px solid var(--border-feat);
    border-radius: 16px;
    padding: 20px 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    opacity: 0;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    position: relative;
    overflow: hidden;
  }

  .feat-card:nth-child(1) { animation: fadeUp 0.6s ease 0.30s forwards; }
  .feat-card:nth-child(2) { animation: fadeUp 0.6s ease 0.42s forwards; }
  .feat-card:nth-child(3) { animation: fadeUp 0.6s ease 0.54s forwards; }
  .feat-card:nth-child(4) { animation: fadeUp 0.6s ease 0.66s forwards; }

  .feat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
  }

  .feat-card.blue::before   { background: linear-gradient(90deg, #3b82f6, #6366f1); }
  .feat-card.purple::before { background: linear-gradient(90deg, #8b5cf6, #ec4899); }
  .feat-card.green::before  { background: linear-gradient(90deg, #10b981, #3b82f6); }
  .feat-card.orange::before { background: linear-gradient(90deg, #f59e0b, #ef4444); }

  .feat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px var(--shadow-hover);
    border-color: rgba(139,92,246,0.3);
  }

  .feat-icon  { font-size: 26px; }

  .feat-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-card-title);
    line-height: 1.3;
  }

  .feat-desc {
    font-size: 12px;
    color: var(--text-feat-desc);
    line-height: 1.5;
  }

  /* ── Color legend ── */
  .legend-card {
    background: var(--bg-legend);
    border: 1px solid var(--border-legend);
    border-radius: 16px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 32px;
    flex-wrap: wrap;
    opacity: 0;
    animation: fadeUp 0.6s ease 0.78s forwards;
  }

  .legend-title {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-legend-label);
    text-transform: uppercase;
    letter-spacing: 1px;
    flex-basis: 100%;
    margin-bottom: -8px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .legend-box {
    width: 14px; height: 14px;
    border-radius: 4px;
    flex-shrink: 0;
  }

  .legend-box.green { background: #10b981; box-shadow: 0 0 8px rgba(16,185,129,0.4); }
  .legend-box.red   { background: #ef4444; box-shadow: 0 0 8px rgba(239,68,68,0.4); }

  .legend-text { font-size: 13.5px; font-weight: 600; color: var(--text-legend-main); }
  .legend-sub  { font-size: 12px;   color: var(--text-legend-sub); font-weight: 400; }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
  }
</style>

<div class="tentang-wrapper" id="tentang-root">

  <!-- Header -->
  <div class="section-header">
    <div class="section-pill">
      <span class="pill-dot"></span>
      Tentang
    </div>
    <h2 class="section-title">Tentang EduDetect</h2>
  </div>

  <!-- Main description card -->
  <div class="main-card">
    <div class="card-icon-row">
      <div class="card-icon">🎯</div>
      <div class="card-title-text">Apa itu EduDetect?</div>
    </div>
    <p class="card-body">
      EduDetect merupakan sistem berbasis website yang memanfaatkan model algoritma <span class="highlight-blue">YOLOv11</span> untuk melakukan
      deteksi dan klasifikasi aktivitas siswa secara otomatis dari video rekaman CCTV selama proses
      pembelajaran di kelas. Pengguna cukup mengunggah video rekaman, kemudian sistem akan menganalisis
      setiap frame untuk mengidentifikasi perilaku siswa — mengklasifikasikannya ke dalam kategori
      <span class="highlight-green">memperhatikan</span> dan <span class="highlight-red">tidak memperhatikan</span>,
      serta menghitung persentase tingkat perhatian siswa secara keseluruhan.
      <br><br>
      Sistem juga menghasilkan output berupa visualisasi bounding box, label klasifikasi, serta
      insight dan rekomendasi berbasis <span class="highlight-blue">Gemini AI</span> yang dapat
      digunakan sebagai bahan evaluasi oleh guru untuk meningkatkan efektivitas proses pembelajaran.
    </p>
  </div>

  <!-- Mini feature cards -->
  <div class="features-grid">
    <div class="feat-card blue">
      <div class="feat-icon">🎥</div>
      <div class="feat-title">Input Video CCTV</div>
      <div class="feat-desc">Unggah rekaman aktivitas kelas secara langsung</div>
    </div>
    <div class="feat-card purple">
      <div class="feat-icon">🔍</div>
      <div class="feat-title">Deteksi Objek</div>
      <div class="feat-desc">YOLOv11 mendeteksi setiap siswa di setiap frame</div>
    </div>
    <div class="feat-card green">
      <div class="feat-icon">📊</div>
      <div class="feat-title">Visualisasi Hasil</div>
      <div class="feat-desc">Bounding box berwarna untuk setiap klasifikasi</div>
    </div>
    <div class="feat-card orange">
      <div class="feat-icon">🤖</div>
      <div class="feat-title">Insight AI</div>
      <div class="feat-desc">Rekomendasi cerdas berbasis Gemini AI</div>
    </div>
  </div>

  <!-- Color legend -->
  <div class="legend-card">
    <div class="legend-title">Kode Warna Bounding Box</div>
    <div class="legend-item">
      <div class="legend-box green"></div>
      <div>
        <div class="legend-text">Hijau</div>
        <div class="legend-sub">Siswa memperhatikan</div>
      </div>
    </div>
    <div class="legend-item">
      <div class="legend-box red"></div>
      <div>
        <div class="legend-text">Merah</div>
        <div class="legend-sub">Siswa tidak memperhatikan</div>
      </div>
    </div>
  </div>

</div>

<script>
// Deteksi dark mode dari parent Streamlit dan toggle class .dark-mode
(function() {
  var root = document.getElementById('tentang-root');

  function applyTheme() {
    var parentDoc = window.parent.document;
    // Streamlit menambahkan atribut data-theme="dark" pada <html> saat dark mode
    var htmlEl   = parentDoc.documentElement;
    var bodyEl   = parentDoc.body;
    var isDark   =
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

  // Pantau perubahan tema secara dinamis (misal user ganti tema di tengah sesi)
  var observer = new MutationObserver(applyTheme);
  observer.observe(window.parent.document.documentElement, {
    attributes: true, attributeFilter: ['data-theme', 'class']
  });
  observer.observe(window.parent.document.body, {
    attributes: true, attributeFilter: ['class', 'data-theme']
  });

  // Fallback: cek via prefers-color-scheme
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
})();
</script>
""", height=700)
    st.divider()