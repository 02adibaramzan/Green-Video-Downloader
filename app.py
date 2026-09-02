import streamlit as st
import yt_dlp
import os
import uuid
from datetime import datetime
import time
import threading
import base64

# Page configuration
st.set_page_config(
    page_title="PK Video Downloader",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Pakistan Flag Colors */
    :root {
        --pk-green: #01411C;
        --pk-white: #FFFFFF;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #01411C 0%, #006400 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .header-container h1 {
        color: white !important;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .header-container p {
        color: rgba(255,255,255,0.9);
        margin: 10px 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Flag styling */
    .flag-container {
        display: inline-block;
        margin-right: 15px;
        vertical-align: middle;
    }
    
    .flag-svg {
        width: 60px;
        height: 45px;
        border-radius: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Card styling */
    .stButton>button {
        background: linear-gradient(135deg, #01411C 0%, #006400 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(1, 65, 28, 0.4);
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        width: 100%;
    }
    
    /* Feature badges */
    .feature-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 8px 16px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.9rem;
    }
    
    /* Section headers */
    .section-header {
        background: rgba(1, 65, 28, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0 15px 0;
        border-left: 4px solid #01411C;
    }
    
    .section-header h3 {
        color: #01411C;
        margin: 0;
        font-size: 1.3rem;
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.1rem;
        margin: 20px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: white;
        margin-top: 3rem;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Auto-cleanup function
def cleanup_old_files():
    """Delete files older than 30 minutes"""
    while True:
        time.sleep(1800)  # 30 minutes
        current_time = datetime.now()
        for filename in os.listdir(DOWNLOAD_DIR):
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if (current_time - file_time).total_seconds() > 1800:
                    os.remove(file_path)
            except:
                pass

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

# Pakistan Flag SVG
flag_svg = """
<svg class="flag-svg" viewBox="0 0 120 90" xmlns="http://www.w3.org/2000/svg">
    <rect width="30" height="90" fill="#FFFFFF"/>
    <rect x="30" width="90" height="90" fill="#01411C"/>
    <circle cx="75" cy="45" r="20" fill="#FFFFFF"/>
    <circle cx="82" cy="45" r="16" fill="#01411C"/>
    <polygon points="85,45 88,52 95,52 89,57 91,64 85,60 79,64 81,57 75,52 82,52" fill="#FFFFFF"/>
</svg>
"""

# Header
st.markdown(f"""
<div class="header-container">
    <div class="flag-container">
        {flag_svg}
    </div>
    <h1 style="display: inline-block; vertical-align: middle;">PK Video Downloader</h1>
    <p>Professional Video Downloader for Rutube, YouTube & More</p>
    <div style="margin-top: 15px;">
        <span class="feature-badge">⚡ Fast</span>
        <span class="feature-badge">🛡️ Secure</span>
        <span class="feature-badge">🎯 Unlimited</span>
        <span class="feature-badge">🇵🇰 Made in Pakistan</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'download_complete' not in st.session_state:
    st.session_state.download_complete = False
if 'downloaded_file' not in st.session_state:
    st.session_state.downloaded_file = None

# Main form
with st.container():
    # Basic Information Section
    st.markdown('<div class="section-header"><h3>🔗 Basic Information</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        url = st.text_input(
            "Video/Channel URL",
            placeholder="https://rutube.ru/channel/... or https://youtube.com/...",
            help="Paste the video or channel URL here"
        )
    
    with col2:
        items = st.text_input(
            "Number of Videos",
            value="all",
            help="Enter number (e.g., 5) or 'all' for complete playlist"
        )
    
    dl_mode = st.selectbox(
        "Download Mode",
        options=["🎥 Video Only", "🎵 Audio Only (MP3)", "🖼️ Video + Thumbnail", "📸 Thumbnail Only"],
        index=0
    )
    
    # Video Quality Section
    st.markdown('<div class="section-header"><h3>🎬 Video Quality & Format</h3></div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        video_quality = st.selectbox(
            "Video Quality",
            options=["Best Quality", "1080p (Full HD)", "720p (HD)", "480p (SD)", "360p (Low)"],
            index=0
        )
    
    with col4:
        output_format = st.selectbox(
            "Output Format",
            options=["MP4", "MKV", "WebM", "AVI"],
            index=0
        )
    
    # Advanced Options Section
    st.markdown('<div class="section-header"><h3>⚙️ Advanced Options</h3></div>', unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        download_subtitles = st.checkbox(
            "📝 Download Subtitles (EN/UR)",
            value=False,
            help="Download available subtitles in English and Urdu"
        )
    
    with col6:
        embed_metadata = st.checkbox(
            "ℹ️ Embed Metadata",
            value=True,
            help="Embed title, date, and other metadata in the file"
        )
    
    # Download Button
    st.markdown("")
    download_clicked = st.button("🚀 Start Download", type="primary", use_container_width=True)
    
    # Process download
    if download_clicked:
        if not url:
            st.error("❌ Please enter a valid URL!")
        else:
            with st.spinner("🔄 Processing your request..."):
                try:
                    # Generate unique task ID
                    task_id = str(uuid.uuid4())[:8]
                    timestamp = datetime.now().strftime('%Y%m%d')
                    output_path = os.path.join(DOWNLOAD_DIR, f"{task_id}_{timestamp}_%(title)s.%(ext)s")
                    
                    # yt-dlp options
                    ydl_opts = {
                        'outtmpl': output_path,
                        'ignoreerrors': True,
                        'nooverwrites': True,
                        'quiet': False,
                        'no_warnings': False,
                    }
                    
                    # Playlist items
                    if items != 'all':
                        try:
                            ydl_opts['playlist_items'] = f"1-{int(items)}"
                        except:
                            st.error("❌ Invalid number of items!")
                            st.stop()
                    
                    # Video quality mapping
                    quality_map = {
                        'Best Quality': 'bestvideo+bestaudio/best',
                        '1080p (Full HD)': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                        '720p (HD)': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                        '480p (SD)': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
                        '360p (Low)': 'bestvideo[height<=360]+bestaudio/best[height<=360]'
                    }
                    
                    # Download mode handling
                    mode_map = {
                        "🎥 Video Only": "2",
                        "🎵 Audio Only (MP3)": "1",
                        "🖼️ Video + Thumbnail": "3",
                        "📸 Thumbnail Only": "4"
                    }
                    
                    selected_mode = mode_map[dl_mode]
                    
                    if selected_mode == '1':  # Audio only
                        ydl_opts['format'] = 'bestaudio/best'
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '320',
                        }]
                    elif selected_mode == '2':  # Video
                        ydl_opts['format'] = quality_map.get(video_quality, 'best')
                        if output_format != 'MP4':
                            ydl_opts['postprocessors'] = [{
                                'key': 'FFmpegVideoConvertor',
                                'preferedformat': output_format.lower(),
                            }]
                    elif selected_mode == '3':  # Video + Thumbnail
                        ydl_opts['format'] = quality_map.get(video_quality, 'best')
                        ydl_opts['writethumbnail'] = True
                    elif selected_mode == '4':  # Thumbnail only
                        ydl_opts['skip_download'] = True
                        ydl_opts['writethumbnail'] = True
                    
                    # Subtitles
                    if download_subtitles:
                        ydl_opts['writesubtitles'] = True
                        ydl_opts['writeautomaticsub'] = True
                        ydl_opts['subtitleslangs'] = ['en', 'ur']
                    
                    # Metadata embedding
                    if embed_metadata:
                        if 'postprocessors' not in ydl_opts:
                            ydl_opts['postprocessors'] = []
                        ydl_opts['postprocessors'].append({
                            'key': 'FFmpegMetadata',
                        })
                    
                    # Download
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        status_text.text("📥 Extracting video information...")
                        progress_bar.progress(20)
                        
                        info = ydl.extract_info(url, download=True)
                        
                        if info:
                            status_text.text("💾 Processing file...")
                            progress_bar.progress(60)
                            
                            filename = ydl.prepare_filename(info)
                            
                            # Handle audio conversion
                            if selected_mode == '1':
                                filename = filename.rsplit('.', 1)[0] + '.mp3'
                            
                            # Handle format conversion
                            if selected_mode == '2' and output_format != 'MP4':
                                filename = filename.rsplit('.', 1)[0] + f'.{output_format.lower()}'
                            
                            if os.path.exists(filename):
                                progress_bar.progress(100)
                                status_text.text("✅ Download complete!")
                                
                                # Store in session state
                                st.session_state.download_complete = True
                                st.session_state.downloaded_file = filename
                                
                                # Success message
                                st.markdown("""
                                <div class="success-message">
                                    <h3>✅ Download Successful!</h3>
                                    <p>Your file is ready to download below</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Download button
                                with open(filename, "rb") as file:
                                    st.download_button(
                                        label="📥 Download File",
                                        data=file,
                                        file_name=os.path.basename(filename),
                                        mime="application/octet-stream",
                                        use_container_width=True
                                    )
                            else:
                                st.error("❌ File not found after download!")
                        else:
                            st.error("❌ Could not extract video information!")
                            
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("""
<div class="footer">
    <p>🇵🇰 Made with ❤️ in Pakistan</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">© 2026 PK Video Downloader. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
