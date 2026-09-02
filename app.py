import streamlit as st
import yt_dlp
import os

# Page Settings (Website ka Title aur Design)
st.set_page_config(
    page_title=Universal Video Downloader,
    page_icon=📥,
    layout=centered
)

# Attractive UI Customization (Website ka Rang aur Style)
st.markdown(
    style
    .main { background-color #f8f9fa; }
    .stButtonbutton {
        width 100%;
        background-color #28a745;
        color white;
        font-weight bold;
        border-radius 8px;
        padding 12px;
        font-size 18px;
    }
    .stButtonbuttonhover { background-color #218838; }
    style
, unsafe_allow_html=True)

st.title(📥 Premium Video & Audio Downloader)
st.caption(Rutube, YouTube, TikTok, Instagram se muft download karein!)

# Input Section (Jahan user link dale ga)
url = st.text_input(🔗 Video ya Channel ka Link yahan paste karein, placeholder=https...)

col1, col2 = st.columns(2)
with col1
    dl_mode = st.selectbox(
        🛠️ Download Mode Chunein,
        [Sirf Video (Best Quality), Sirf Audio (MP3), Video aur Thumbnail Dono, Sirf Thumbnail]
    )
with col2
    video_quality = st.selectbox(
        🎞️ Video Resolution,
        [Best Quality, 1080p, 720p, 480p]
    )

# Folder jahan server par file save hogi
DOWNLOAD_DIR = downloads
if not os.path.exists(DOWNLOAD_DIR)
    os.makedirs(DOWNLOAD_DIR)

# Options configuration for yt-dlp
def get_ydl_opts(mode, quality)
    opts = {
        'outtmpl' f'{DOWNLOAD_DIR}%(title)s.%(ext)s',
        'ignoreerrors' True,
        'nooverwrites' True,
    }
    
    q_format = bestvideo+bestaudiobest
    if quality == 1080p q_format = bestvideo[height=1080]+bestaudiobest[height=1080]
    elif quality == 720p q_format = bestvideo[height=720]+bestaudiobest[height=720]
    elif quality == 480p q_format = bestvideo[height=480]+bestaudiobest[height=480]

    if mode == Sirf Audio (MP3)
        opts.update({
            'format' 'bestaudiobest',
            'postprocessors' [{
                'key' 'FFmpegExtractAudio',
                'preferredcodec' 'mp3',
                'preferredquality' '192',
            }]
        })
    elif mode == Sirf Thumbnail
        opts.update({'skip_download' True, 'writethumbnail' True})
    elif mode == Video aur Thumbnail Dono
        opts.update({'format' q_format, 'writethumbnail' True})
    else
        opts.update({'format' q_format})
        
    return opts

# Action Button
if st.button(🚀 Processing Shuru Karein)
    if not url
        st.warning(Meharbani karke pehle ek link dalein!)
    else
        with st.spinner(Server par download ho raha hai... thoda intezar karein...)
            try
                ydl_opts = get_ydl_opts(dl_mode, video_quality)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl
                    info = ydl.extract_info(url, download=True)
                    
                    # File ka naam maloom karna taake user ko download button diya ja sake
                    if 'entries' in info  # Agar playlist hai
                        video_title = info['entries'][0]['title']
                        ext = info['entries'][0].get('ext', 'mp4')
                    else
                        video_title = info.get('title', 'video')
                        ext = info.get('ext', 'mp4')
                    
                    if dl_mode == Sirf Audio (MP3) ext = mp3
                    elif dl_mode == Sirf Thumbnail ext = jpg
                    
                    filename = f{video_title}.{ext}
                    filepath = os.path.join(DOWNLOAD_DIR, filename)
                    
                    st.success(🎉 Server par download mukammal!)
                    
                    # User ke liye Direct Download Button (MobilePC mein save karne ke liye)
                    if os.path.exists(filepath)
                        with open(filepath, rb) as file
                            st.download_button(
                                label=💾 Apne Device Mein Save Karein,
                                data=file,
                                file_name=filename,
                                mime=applicationoctet-stream
                            )
                    else
                        st.info(💡 Files server par save ho chuki hain! Multiple files hone ki soorat mein aap downloads folder check kar sakte hain.)
                        
            except Exception as e
                st.error(fKuch galti hui {str(e)})
