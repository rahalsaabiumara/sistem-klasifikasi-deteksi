import streamlit as st
import cv2
import time
import plotly.graph_objects as go


def _make_donut_chart(percent: int) -> go.Figure:
    """Buat donut chart transparan yang adaptif dark/light mode."""
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=["Memperhatikan", "Tidak Memperhatikan"],
        values=[max(percent, 0), max(100 - percent, 0)],
        hole=0.72,
        marker=dict(
            colors=["#22c55e", "#ef4444"],
            line=dict(color="rgba(0,0,0,0)", width=0)
        ),
        textinfo='none',
        hovertemplate="%{label}: %{value}%<extra></extra>",
        sort=False
    ))
    fig.update_layout(
        template="plotly",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.25,
            xanchor="center", x=0.5,
            font=dict(size=12),
        ),
        annotations=[dict(
            text=f"<b>{percent}%</b>",
            x=0.5, y=0.5,
            font=dict(size=30, family="Arial"),
            showarrow=False,
        )],
        margin=dict(t=20, b=20, l=10, r=10),
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        uirevision=True,
    )
    return fig


def _processing_header():
    """Tampilkan header animasi 'Memproses Analisis Video...' saat video sedang berjalan."""
    st.components.v1.html("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }

  .proc-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 20px 24px;
    background: linear-gradient(135deg,
      rgba(245,158,11,0.08) 0%,
      rgba(239,68,68,0.06) 50%,
      rgba(59,130,246,0.06) 100%);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 18px;
    margin-bottom: 6px;
    animation: fadeUp 0.5s ease forwards;
  }

  /* Spinning loader */
  .loader-ring {
    width: 52px; height: 52px;
    border-radius: 50%;
    border: 4px solid rgba(245,158,11,0.15);
    border-top: 4px solid #f59e0b;
    border-right: 4px solid #ef4444;
    animation: spin 1s linear infinite;
    flex-shrink: 0;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  .proc-text-block { flex: 1; }

  .proc-title {
    font-size: 18px;
    font-weight: 800;
    background: linear-gradient(90deg, #f59e0b, #ef4444, #3b82f6);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 2.5s linear infinite;
    margin-bottom: 6px;
  }

  @keyframes shimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
  }

  /* Animated dots */
  .proc-dots span {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    margin-right: 5px;
    animation: dotBounce 1.2s ease infinite;
  }

  .proc-dots span:nth-child(1) { background:#f59e0b; animation-delay: 0s; }
  .proc-dots span:nth-child(2) { background:#ef4444; animation-delay: 0.2s; }
  .proc-dots span:nth-child(3) { background:#3b82f6; animation-delay: 0.4s; }

  @keyframes dotBounce {
    0%,80%,100% { transform: scale(1);   opacity: 0.6; }
    40%         { transform: scale(1.5); opacity: 1; }
  }

  /* Progress bar */
  .proc-bar-wrap {
    height: 4px;
    background: rgba(245,158,11,0.12);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 10px;
  }

  .proc-bar {
    height: 100%;
    width: 40%;
    background: linear-gradient(90deg, #f59e0b, #ef4444, #3b82f6);
    border-radius: 999px;
    animation: barSlide 1.8s ease-in-out infinite;
  }

  @keyframes barSlide {
    0%   { width: 10%; margin-left: 0%; }
    50%  { width: 50%; margin-left: 30%; }
    100% { width: 10%; margin-left: 90%; }
  }

  /* Status tags */
  .proc-tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 10px;
  }

  .proc-tag {
    font-size: 10.5px;
    font-weight: 700;
    padding: 3px 12px;
    border-radius: 999px;
    letter-spacing: 0.5px;
    animation: fadeUp 0.5s ease forwards;
    opacity: 0;
  }

  .tag-yolo  { background: rgba(245,158,11,0.12); color:#d97706; border:1px solid rgba(245,158,11,0.25); animation-delay:0.2s; }
  .tag-frame { background: rgba(59,130,246,0.10);  color:#2563eb; border:1px solid rgba(59,130,246,0.20); animation-delay:0.4s; }
  .tag-live  { background: rgba(16,185,129,0.10);  color:#059669; border:1px solid rgba(16,185,129,0.20); animation-delay:0.6s; }

  @keyframes fadeUp {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0); }
  }
</style>

<div class="proc-header">
  <div class="loader-ring"></div>
  <div class="proc-text-block">
    <div class="proc-title">Memproses Analisis Video Rekaman CCTV...</div>
    <div class="proc-dots">
      <span></span><span></span><span></span>
    </div>
    <div class="proc-bar-wrap"><div class="proc-bar"></div></div>
    <div class="proc-tags">
      <span class="proc-tag tag-yolo">⚡ YOLOv11 Active</span>
      <span class="proc-tag tag-frame">🎞️ Frame-by-Frame</span>
      <span class="proc-tag tag-live">🔴 Live Analysis</span>
    </div>
  </div>
</div>
""", height=145)


def _finished_header(placeholder):
    """Ganti header 'Memproses...' menjadi 'Berhasil Dianalisis' setelah video selesai."""
    with placeholder:
        st.components.v1.html("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }

  .finished-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 20px 24px;
    background: linear-gradient(135deg,
      rgba(16,185,129,0.08) 0%,
      rgba(59,130,246,0.06) 100%);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 18px;
    margin-bottom: 6px;
  }

  .finished-icon {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #10b981, #3b82f6);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(16,185,129,0.28);
  }

  .finished-text-block { flex: 1; }

  .finished-title {
    font-size: 18px;
    font-weight: 800;
    background: linear-gradient(135deg, #10b981 0%, #3b82f6 60%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
    letter-spacing: -0.2px;
  }

  .finished-tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .finished-tag {
    font-size: 10.5px;
    font-weight: 700;
    padding: 3px 12px;
    border-radius: 999px;
    letter-spacing: 0.5px;
  }

  .tag-done   { background: rgba(16,185,129,0.12); color:#059669; border:1px solid rgba(16,185,129,0.25); }
  .tag-frames { background: rgba(59,130,246,0.10);  color:#2563eb; border:1px solid rgba(59,130,246,0.20); }
  .tag-ai     { background: rgba(139,92,246,0.10);  color:#7c3aed; border:1px solid rgba(139,92,246,0.20); }
</style>

<div class="finished-header">
  <div class="finished-icon">✅</div>
  <div class="finished-text-block">
    <div class="finished-title">Video Rekaman CCTV Berhasil Dianalisis</div>
    <div class="finished-tags">
      <span class="finished-tag tag-done">✔ Deteksi Selesai</span>
      <span class="finished-tag tag-frames">🎞️ Frame-by-Frame</span>
      <span class="finished-tag tag-ai">🤖 YOLOv11</span>
    </div>
  </div>
</div>
""", height=120)


def _done_header():
    """Tampilkan header 'Hasil Analisis Rekaman CCTV' setelah video selesai."""
    st.components.v1.html("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --done-bg: linear-gradient(135deg, rgba(16,185,129,0.07) 0%, rgba(59,130,246,0.06) 100%);
    --done-border: rgba(16,185,129,0.25);
    --done-sub: #4b5563;
  }
  .dark-mode-done {
    --done-bg: linear-gradient(135deg, rgba(16,185,129,0.12) 0%, rgba(59,130,246,0.10) 100%);
    --done-border: rgba(16,185,129,0.35);
    --done-sub: #94a3b8;
  }

  .done-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 20px 24px;
    background: var(--done-bg);
    border: 1px solid var(--done-border);
    border-radius: 18px;
    margin-bottom: 6px;
    animation: fadeUp 0.6s cubic-bezier(.4,0,.2,1) forwards;
  }

  .done-icon-wrap {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #10b981, #3b82f6);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(16,185,129,0.30);
    animation: popIn 0.5s cubic-bezier(.34,1.56,.64,1) 0.2s forwards;
    opacity: 0;
    transform: scale(0.6);
  }

  @keyframes popIn {
    to { opacity:1; transform:scale(1); }
  }

  .done-text { flex: 1; }

  .done-title {
    font-size: 18px;
    font-weight: 800;
    background: linear-gradient(135deg, #10b981 0%, #3b82f6 60%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 5px;
  }

  .done-sub {
    font-size: 13px;
    color: var(--done-sub);
    font-weight: 500;
  }

  /* Status badges */
  .done-badges {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 10px;
  }

  .done-badge {
    font-size: 10.5px;
    font-weight: 700;
    padding: 3px 12px;
    border-radius: 999px;
    opacity: 0;
    animation: fadeUp 0.5s ease forwards;
  }

  .db-green  { background:rgba(16,185,129,0.12); color:#059669; border:1px solid rgba(16,185,129,0.25); animation-delay:0.3s; }
  .db-blue   { background:rgba(59,130,246,0.10); color:#2563eb; border:1px solid rgba(59,130,246,0.20); animation-delay:0.45s; }
  .db-purple { background:rgba(139,92,246,0.10); color:#7c3aed; border:1px solid rgba(139,92,246,0.20); animation-delay:0.60s; }

  @keyframes fadeUp {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0); }
  }
</style>

<div class="done-header" id="done-root">
  <div class="done-icon-wrap">✅</div>
  <div class="done-text">
    <div class="done-title">Hasil Analisis Rekaman CCTV</div>
    <div class="done-sub">Analisis video selesai dilakukan</div>
    <div class="done-badges">
      <span class="done-badge db-green">✔ Deteksi Selesai</span>
      <span class="done-badge db-blue">📊 Persentase Terhitung</span>
      <span class="done-badge db-purple">🤖 Hasil Summary AI Tersedia</span>
    </div>
  </div>
</div>

<script>
(function() {
  var root = document.getElementById('done-root');
  function applyTheme() {
    var html = window.parent.document.documentElement;
    var body = window.parent.document.body;
    var dark = html.getAttribute('data-theme') === 'dark' ||
               body.classList.contains('dark') ||
               window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.classList.toggle('dark-mode-done', dark);
  }
  applyTheme();
  new MutationObserver(applyTheme).observe(window.parent.document.documentElement,
    { attributes:true, attributeFilter:['data-theme','class'] });
  new MutationObserver(applyTheme).observe(window.parent.document.body,
    { attributes:true, attributeFilter:['class','data-theme'] });
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
})();
</script>
""", height=140)


def run_analysis(model, video_bytes: bytes) -> dict:
    """
    Jalankan analisis video frame-by-frame.
    Mengembalikan dict berisi semua hasil analisis.
    """
    # ── Tampilkan header animasi "sedang memproses" ──
    processing_placeholder = st.empty()
    finished_placeholder = st.empty()
    with processing_placeholder:
        _processing_header()

    with open("temp_video.mp4", "wb") as f:
        f.write(video_bytes)

    cap = cv2.VideoCapture("temp_video.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    label_short = {'memperhatikan': 'M', 'tidak_memperhatikan': 'TM'}

    attentive_history, inattentive_history, timeline = [], [], []
    frame_no       = 0
    last_frame_rgb = None
    last_percent   = 0

    col1, col2 = st.columns([3, 2])
    video_placeholder = col1.empty()
    with col2:
        chart_placeholder = st.empty()
        label_placeholder = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        import cv2 as _cv2
        img     = frame.copy()
        results = model.predict(source=frame, conf=0.3, stream=True)

        attentive_count   = 0
        inattentive_count = 0

        for r in results:
            img = r.orig_img.copy()
            for box in r.boxes:
                cls_id      = int(box.cls[0])
                label_name  = model.names[cls_id]
                short_label = label_short.get(label_name, label_name)

                if short_label == 'M':
                    color = (0, 255, 0);  attentive_count += 1
                elif short_label == 'TM':
                    color = (0, 0, 255);  inattentive_count += 1
                else:
                    color = (255, 255, 0)

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                _cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                _cv2.putText(img, short_label, (x1, y1 - 10),
                             _cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        total   = attentive_count + inattentive_count
        percent = int((attentive_count / total) * 100) if total > 0 else 0

        attentive_history.append(attentive_count)
        inattentive_history.append(inattentive_count)
        timeline.append(frame_no / fps)

        img_rgb = _cv2.cvtColor(img, _cv2.COLOR_BGR2RGB)
        video_placeholder.image(img_rgb, channels="RGB", width="stretch")

        chart_placeholder.plotly_chart(
            _make_donut_chart(percent),
            use_container_width=True,
            key=f"chart-live-{frame_no}"
        )
        label_placeholder.markdown(
            "<h5 style='text-align:center;'>Siswa Memperhatikan</h5>",
            unsafe_allow_html=True
        )

        last_frame_rgb = img_rgb
        last_percent   = percent
        frame_no      += 1
        time.sleep(0.03)

    cap.release()

    # ── Ganti header menjadi "Berhasil Dianalisis" ──
    processing_placeholder.empty()
    _finished_header(finished_placeholder)

    # Hitung ringkasan
    total_att     = sum(attentive_history)
    total_inatt   = sum(inattentive_history)
    total_all     = total_att + total_inatt
    final_percent = int((total_att / total_all) * 100) if total_all > 0 else 0

    def summarize_range(times):
        return f"{min(times):.1f}s - {max(times):.1f}s" if times else "Tidak ada data"

    attentive_times, inattentive_times = [], []
    for i in range(len(timeline)):
        (attentive_times if attentive_history[i] > inattentive_history[i]
         else inattentive_times).append(timeline[i])

    return {
        "attentive_history":   attentive_history,
        "inattentive_history": inattentive_history,
        "timeline":            timeline,
        "frame_no":            frame_no,
        "last_frame_rgb":      last_frame_rgb,
        "last_percent":        last_percent,
        "final_percent":       final_percent,
        "att_range":           summarize_range(attentive_times),
        "inatt_range":         summarize_range(inattentive_times),
        "opening_text": (
            "✅ Akurasi persentase siswa yang memperhatikan cukup baik, pertahankan!"
            if final_percent >= 50
            else "⚠️ Akurasi persentase siswa yang memperhatikan kurang baik, harap lebih diperhatikan selama kegiatan belajar mengajar berlangsung."
        ),
    }


def render_static(anim, close_anim, trigger_scroll):
    """
    Tampilkan header selesai + frame terakhir + tombol replay.
    Dipanggil saat video sudah selesai dan tidak sedang replay.
    """
    # ── Header "Hasil Analisis" ──
    _done_header()

    col1, col2 = st.columns([3, 2])

    with col1:
        anim("reveal-left-anim", "0ms")
        if st.session_state.last_frame_rgb is not None:
            st.image(st.session_state.last_frame_rgb, use_column_width=True)
        else:
            st.info("Tidak ada frame video yang tersedia.")

    with col2:
        anim("reveal-right-anim", "100ms")
        st.plotly_chart(
            _make_donut_chart(st.session_state.final_percent),
            use_container_width=True,
            key="chart-static"
        )
        st.markdown(
            "<h5 style='text-align:center;'>Siswa Memperhatikan</h5>",
            unsafe_allow_html=True
        )
        close_anim()
