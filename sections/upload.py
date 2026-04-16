import streamlit as st


def render(anim, close_anim, anchor):
    """
    Render section upload video.
    Mengembalikan objek file yang diupload (atau None jika belum ada).
    """
    anchor("section-upload")

    anim("reveal-anim", "0ms")
    st.subheader("Unggah Video Rekaman CCTV")
    video_file = st.file_uploader(
        "Silahkan unggah video rekaman CCTV disini",
        type=["mp4"]
    )
    close_anim()

    return video_file