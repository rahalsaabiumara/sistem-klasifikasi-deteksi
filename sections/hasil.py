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


def run_analysis(model, video_bytes: bytes) -> dict:
    """
    Jalankan analisis video frame-by-frame.
    Mengembalikan dict berisi semua hasil analisis.
    """
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

        import numpy as _np
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
    Tampilkan frame terakhir + tombol replay
    (dipanggil saat video sudah selesai dan tidak sedang replay).
    """
    anim("reveal-anim", "0ms")
    st.subheader("📹 Memproses Analisis Video...")
    close_anim()

    col1, col2 = st.columns([3, 2])

    with col1:
        anim("reveal-left-anim", "0ms")
        if st.session_state.last_frame_rgb is not None:
            st.image(st.session_state.last_frame_rgb, use_column_width=True)
            st.markdown("""
            <div style="display:flex;align-items:center;justify-content:center;
                        gap:10px;margin-top:10px;padding:12px 0 4px 0;
                        border-top:1px solid rgba(128,128,128,0.2);">
                <span style="font-size:22px;">⏹️</span>
                <span style="font-size:14px;color:gray;font-style:italic;">
                    Video selesai dianalisis
                </span>
            </div>
            """, unsafe_allow_html=True)
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