import streamlit as st


def render():
    """Render hero section — landing page utama."""
    st.components.v1.html("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  .hero-wrapper {
    font-family: 'Plus Jakarta Sans', sans-serif;
    text-align: center;
    padding: 64px 24px 56px;
    position: relative;
    overflow: hidden;
    border-radius: 24px;
  }

  /* Animated mesh background */
  .hero-wrapper::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse 80% 60% at 20% 30%, rgba(59,130,246,0.12) 0%, transparent 60%),
      radial-gradient(ellipse 60% 80% at 80% 70%, rgba(139,92,246,0.10) 0%, transparent 60%),
      radial-gradient(ellipse 50% 50% at 50% 50%, rgba(16,185,129,0.06) 0%, transparent 70%);
    animation: meshShift 8s ease-in-out infinite alternate;
    z-index: 0;
  }

  @keyframes meshShift {
    0%   { opacity: 0.7; transform: scale(1) rotate(0deg); }
    100% { opacity: 1;   transform: scale(1.05) rotate(1deg); }
  }

  .hero-content { position: relative; z-index: 1; }

  /* Badge */
  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(90deg, rgba(59,130,246,0.15), rgba(139,92,246,0.15));
    border: 1px solid rgba(139,92,246,0.3);
    color: #8b5cf6;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 20px;
    border-radius: 999px;
    margin-bottom: 28px;
    opacity: 0;
    animation: fadeUp 0.6s ease 0.2s forwards;
    backdrop-filter: blur(8px);
  }

  .badge-dot {
    width: 6px; height: 6px;
    background: #8b5cf6;
    border-radius: 50%;
    animation: pulse 2s ease infinite;
  }

  @keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%     { opacity: 0.5; transform: scale(1.4); }
  }

  /* Title */
  .hero-title {
    font-size: clamp(34px, 5.5vw, 62px);
    font-weight: 800;
    line-height: 1.12;
    margin: 0 0 18px;
    background: linear-gradient(135deg, #1d4ed8 0%, #7c3aed 45%, #059669 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    opacity: 0;
    animation: fadeUp 0.7s ease 0.4s forwards;
  }

  /* Subtitle */
  .hero-subtitle {
    font-size: clamp(15px, 2vw, 19px);
    color: #6b7280;
    margin: 0 auto 14px;
    max-width: 580px;
    line-height: 1.6;
    opacity: 0;
    animation: fadeUp 0.7s ease 0.6s forwards;
  }

  /* Typewriter */
  .typewriter-wrapper {
    font-size: clamp(16px, 2.2vw, 21px);
    font-weight: 600;
    min-height: 38px;
    margin: 0 auto 40px;
    opacity: 0;
    animation: fadeUp 0.7s ease 0.8s forwards;
  }

  .typewriter-prefix { color: #9ca3af; }

  .typewriter-text {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
  }

  .typewriter-cursor {
    display: inline-block;
    width: 2.5px;
    height: 1.1em;
    background: #8b5cf6;
    margin-left: 3px;
    vertical-align: middle;
    border-radius: 2px;
    animation: blink 0.75s step-end infinite;
  }

  @keyframes blink {
    0%,100% { opacity: 1; } 50% { opacity: 0; }
  }

  /* Stats */
  .hero-stats {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    flex-wrap: wrap;
    margin-bottom: 44px;
    opacity: 0;
    animation: fadeUp 0.7s ease 1.0s forwards;
  }

  .stat-card {
    text-align: center;
    padding: 16px 32px;
    position: relative;
  }

  .stat-card + .stat-card::before {
    content: '';
    position: absolute;
    left: 0; top: 20%; height: 60%;
    width: 1px;
    background: rgba(107,114,128,0.2);
  }

  .stat-number {
    font-size: 22px;
    font-weight: 800;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
  }

  .stat-label {
    font-size: 10px;
    color: #9ca3af;
    font-weight: 600;
    margin-top: 4px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  /* CTA Buttons */
  .hero-cta {
    display: flex;
    gap: 14px;
    justify-content: center;
    flex-wrap: wrap;
    opacity: 0;
    animation: fadeUp 0.7s ease 1.2s forwards;
  }

  .btn-primary {
    background: linear-gradient(135deg, #3b82f6 0%, #7c3aed 100%);
    color: white;
    border: none;
    padding: 15px 40px;
    font-size: 15px;
    font-weight: 700;
    font-family: 'Plus Jakarta Sans', sans-serif;
    border-radius: 14px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 6px 24px rgba(59,130,246,0.38);
    transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1);
    letter-spacing: 0.3px;
    position: relative;
    overflow: hidden;
  }

  .btn-primary::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
    opacity: 0;
    transition: opacity 0.25s;
  }

  .btn-primary:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 12px 32px rgba(59,130,246,0.45);
  }

  .btn-primary:hover::after { opacity: 1; }
  .btn-primary:active { transform: translateY(0) scale(0.98); }

  .btn-secondary {
    background: rgba(255,255,255,0.04);
    color: #6b7280;
    border: 1.5px solid rgba(107,114,128,0.3);
    padding: 15px 36px;
    font-size: 15px;
    font-weight: 600;
    font-family: 'Plus Jakarta Sans', sans-serif;
    border-radius: 14px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.25s ease;
    backdrop-filter: blur(8px);
  }

  .btn-secondary:hover {
    border-color: #7c3aed;
    color: #7c3aed;
    transform: translateY(-3px);
    background: rgba(124,58,237,0.06);
    box-shadow: 0 6px 20px rgba(124,58,237,0.12);
  }

  /* Floating icons */
  .floating-icons {
    position: absolute;
    width: 100%; height: 100%;
    top: 0; left: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
  }

  .float-icon {
    position: absolute;
    font-size: 26px;
    opacity: 0.10;
    animation: floatAnim 7s ease-in-out infinite;
  }

  .float-icon:nth-child(1) { top:8%;    left:4%;   animation-delay:0s;   animation-duration:6s; }
  .float-icon:nth-child(2) { top:15%;   right:6%;  animation-delay:1s;   animation-duration:8s; }
  .float-icon:nth-child(3) { bottom:22%;left:7%;   animation-delay:2s;   animation-duration:7s; }
  .float-icon:nth-child(4) { bottom:12%;right:4%;  animation-delay:0.5s; animation-duration:9s; }
  .float-icon:nth-child(5) { top:48%;   left:2%;   animation-delay:1.5s; animation-duration:6.5s; }
  .float-icon:nth-child(6) { top:42%;   right:2%;  animation-delay:2.5s; animation-duration:7.5s; }

  @keyframes floatAnim {
    0%,100% { transform: translateY(0) rotate(0deg); }
    33%     { transform: translateY(-16px) rotate(6deg); }
    66%     { transform: translateY(10px) rotate(-5deg); }
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .hero-divider {
    margin-top: 56px;
    height: 1px;
    background: linear-gradient(90deg,
      transparent, rgba(59,130,246,0.25), rgba(139,92,246,0.25), transparent);
  }

  /* ─── MULAI SEKARANG big CTA below hero ─── */
  .cta-section {
    margin-top: 36px;
    display: flex;
    justify-content: center;
  }

  .btn-mulai {
    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
    color: white;
    border: none;
    padding: 18px 56px;
    font-size: 17px;
    font-weight: 800;
    font-family: 'Plus Jakarta Sans', sans-serif;
    border-radius: 16px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 8px 32px rgba(37,99,235,0.40), 0 2px 8px rgba(124,58,237,0.25);
    transition: all 0.28s cubic-bezier(0.34,1.56,0.64,1);
    letter-spacing: 0.5px;
    position: relative;
    overflow: hidden;
    opacity: 0;
    animation: fadeUp 0.8s ease 1.4s forwards;
  }

  .btn-mulai::before {
    content: '';
    position: absolute;
    top: -50%; left: -60%;
    width: 40%; height: 200%;
    background: rgba(255,255,255,0.18);
    transform: skewX(-20deg);
    transition: left 0.5s ease;
  }

  .btn-mulai:hover::before { left: 120%; }

  .btn-mulai:hover {
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 16px 40px rgba(37,99,235,0.45), 0 4px 16px rgba(124,58,237,0.3);
  }

  .btn-mulai:active { transform: translateY(0) scale(0.98); }

  .btn-icon {
    font-size: 20px;
    animation: rocketBounce 2s ease-in-out infinite;
  }

  @keyframes rocketBounce {
    0%,100% { transform: translateY(0) rotate(-30deg); }
    50%     { transform: translateY(-4px) rotate(-30deg); }
  }
</style>

<div class="hero-wrapper">
  <div class="floating-icons">
    <span class="float-icon">📷</span>
    <span class="float-icon">🎓</span>
    <span class="float-icon">🤖</span>
    <span class="float-icon">📊</span>
    <span class="float-icon">🔍</span>
    <span class="float-icon">✨</span>
  </div>

  <div class="hero-content">
    <div class="hero-badge">
      <span class="badge-dot"></span>
      Powered by YOLOv11 &amp; Gemini AI
    </div>

    <h1 class="hero-title">Selamat Datang di EduDetect</h1>

    <p class="hero-subtitle">
      Website Sistem Klasifikasi dan Deteksi Aktivitas Pembelajaran Siswa
    </p>

    <div class="typewriter-wrapper">
      <span class="typewriter-prefix">Deteksi siswa yang&nbsp;</span>
      <span class="typewriter-text" id="tw-text"></span>
      <span class="typewriter-cursor"></span>
    </div>

    <div class="hero-stats">
      <div class="stat-card">
        <div class="stat-number">YOLOv11</div>
        <div class="stat-label">Model Deteksi</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">Gemini AI</div>
        <div class="stat-label">Model Evaluasi</div>
      </div>
    </div>

    <div class="hero-cta">
      <button class="btn-secondary" onclick="(function(){
        var el = window.parent.document.getElementById('section-tentang');
        if(el) el.scrollIntoView({behavior:'smooth', block:'start'});
      })()">📖 Pelajari Lebih Lanjut</button>
    </div>

    <!-- Big MULAI SEKARANG button -->
    <div class="cta-section">
      <button class="btn-mulai" onclick="(function(){
        var el = window.parent.document.getElementById('section-upload');
        if(el) el.scrollIntoView({behavior:'smooth', block:'start'});
      })()">
        <span class="btn-icon">🚀</span>
        MULAI SEKARANG
      </button>
    </div>
  </div>

  <div class="hero-divider"></div>
</div>

<script>
  var phrases = [
    "memperhatikan pelajaran",
    "tidak memperhatikan pelajaran",
  ];
  var el = document.getElementById('tw-text');
  var pi = 0, ci = 0, deleting = false, speed = 70;

  function type() {
    var current = phrases[pi];
    if (!deleting) {
      ci++;
      el.textContent = current.substring(0, ci);
      if (ci === current.length) {
        setTimeout(function(){ deleting = true; tick(); }, 1800);
        return;
      }
    } else {
      ci--;
      el.textContent = current.substring(0, ci);
      if (ci === 0) {
        deleting = false;
        pi = (pi + 1) % phrases.length;
        setTimeout(tick, 400);
        return;
      }
    }
    setTimeout(tick, deleting ? 35 : speed);
  }

  function tick() { type(); }
  setTimeout(tick, 1400);
</script>
""", height=720)
    st.divider()