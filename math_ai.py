import streamlit as st
import random
from gtts import gTTS
import uuid
import os
import time

# ================== 1. CẤU HÌNH HỆ THỐNG ==================
st.set_page_config(
    page_title="Trường Mầm Non Diệu Kỳ",
    page_icon="🏰",
    layout="wide", # Dùng màn hình rộng để chứa nhiều thứ
    initial_sidebar_state="collapsed"
)

# ================== 2. QUẢN LÝ ĐIỀU HƯỚNG ==================
if "page" not in st.session_state:
    st.session_state.page = "home" # Mặc định là trang chủ

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ================== 3. CSS "VƯỜN THÚ" SINH ĐỘNG ==================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&display=swap');

    /* NỀN CHUNG */
    .stApp {
        background: url('https://img.freepik.com/free-vector/landscape-with-green-hills-blue-sky_1308-32332.jpg') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Baloo 2', cursive;
    }

    /* Ẩn các thành phần thừa */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem;}

    /* TITLE */
    .title-text {
        color: #FF6F00;
        text-shadow: 3px 3px 0px #FFF;
        font-size: 50px;
        text-align: center;
        background: rgba(255,255,255,0.8);
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 20px;
        animation: float 3s infinite ease-in-out;
    }

    /* CARD MENU (Các nút chọn chức năng) */
    .menu-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 20px;
        text-align: center;
        cursor: pointer;
        transition: transform 0.3s;
        border: 4px solid #fff;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        height: 300px; /* Chiều cao cố định */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .menu-card:hover {
        transform: scale(1.05) translateY(-10px);
        border-color: #FFEB3B;
        background: #FFFDE7;
    }

    .menu-img {
        width: 150px;
        height: 150px;
        object-fit: contain;
        margin-bottom: 15px;
    }

    .menu-btn {
        background-color: #FF9800;
        color: white;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin-top: 10px;
    }

    /* ANIMATIONS */
    @keyframes float { 0% {transform: translateY(0px);} 50% {transform: translateY(-10px);} 100% {transform: translateY(0px);} }
    @keyframes swing { 0% {transform: rotate(10deg);} 50% {transform: rotate(-10deg);} 100% {transform: rotate(10deg);} }

    /* CON VẬT TRANG TRÍ (DECOR) */
    .monkey-decor {
        position: fixed;
        top: -20px;
        right: 50px;
        width: 100px;
        animation: swing 3s infinite ease-in-out;
        z-index: 99;
    }
    .bird-decor {
        position: fixed;
        top: 20%;
        left: 20px;
        width: 80px;
        animation: float 2s infinite;
        z-index: 99;
    }
    
    /* NÚT QUAY LẠI */
    .back-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 100;
        background: #FF5252;
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        border: 2px solid white;
    }
</style>
""", unsafe_allow_html=True)

# ================== 4. CÁC HÀM CHỨC NĂNG ==================

def phat_am_thanh(text):
    """Phát âm thanh không bị lỗi"""
    try:
        filename = f"sound_{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang="vi")
        tts.save(filename)
        st.audio(open(filename, "rb").read(), format="audio/mp3", autoplay=True)
        os.remove(filename)
    except:
        pass

# ================== TRANG 1: TRANG CHỦ (MENU) ==================
def trang_chu():
    st.markdown('<h1 class="title-text">🏰 Cổng Thông Tin Mầm Non Bản Em</h1>', unsafe_allow_html=True)
    
    # Trang trí thêm thú
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/2362/2362078.png" class="monkey-decor">', unsafe_allow_html=True)
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/826/826912.png" class="bird-decor">', unsafe_allow_html=True)

    # Hiển thị Menu dạng lưới
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="menu-card">
            <img src="https://cdn-icons-png.flaticon.com/512/3069/3069172.png" class="menu-img">
            <h2 style="color:#E91E63">Toán Học Vui</h2>
            <p>Đếm số cùng Thỏ</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Vào Học Toán 🐰", key="btn_toan", use_container_width=True):
            go_to("toan")

    with c2:
        st.markdown("""
        <div class="menu-card">
            <img src="https://cdn-icons-png.flaticon.com/512/616/616430.png" class="menu-img">
            <h2 style="color:#795548">Thư Viện Truyện</h2>
            <p>Xem truyện cổ tích</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Vào Xem Truyện 🐻", key="btn_truyen", use_container_width=True):
            go_to("truyen")

    with c3:
        st.markdown("""
        <div class="menu-card">
            <img src="https://cdn-icons-png.flaticon.com/512/3064/3064883.png" class="menu-img">
            <h2 style="color:#1565C0">Ca Nhạc Thiếu Nhi</h2>
            <p>Hát cùng Họa Mi</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Vào Nghe Nhạc 🐦", key="btn_nhac", use_container_width=True):
            go_to("nhac")

# ================== TRANG 2: HỌC TOÁN (GAME CŨ) ==================
def trang_hoc_toan():
    if st.button("⬅️ Quay lại", key="back_toan"):
        go_to("home")
    
    # -- Code game toán cũ (rút gọn) --
    if "buoc_toan" not in st.session_state: st.session_state.buoc_toan = 1
    if "so_toan" not in st.session_state: st.session_state.so_toan = 3
    
    st.markdown('<div class="title-text">🐰 Thỏ Con Học Đếm</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3069/3069172.png", width=200)
    
    with col2:
        st.info("Bé hãy đếm xem có bao nhiêu quả táo?")
        st.markdown(f"<h1 style='font-size:60px'>{'🍎 ' * st.session_state.so_toan}</h1>", unsafe_allow_html=True)
        
        ans = st.number_input("Bé nhập số:", 0, 10, 0, key="math_input")
        if st.button("Kiểm tra"):
            if ans == st.session_state.so_toan:
                st.balloons()
                phat_am_thanh("Đúng rồi bé ơi!")
                st.success("Giỏi quá!")
                time.sleep(1)
                st.session_state.so_toan = random.randint(1,5)
                st.rerun()
            else:
                st.error("Thử lại nhé!")
                phat_am_thanh("Sai rồi, thử lại nhé")

# ================== TRANG 3: THƯ VIỆN TRUYỆN (STORYBOOK) ==================
def trang_truyen():
    if st.button("⬅️ Quay lại", key="back_truyen"):
        go_to("home")

    st.markdown('<div class="title-text">🐻 Gấu Kể Chuyện Cổ Tích</div>', unsafe_allow_html=True)
    st.write("")

    # Tab chọn truyện
    tab1, tab2 = st.tabs(["📺 Video Cổ Tích", "📚 Web Đọc Truyện"])

    with tab1:
        st.write("Bé chọn truyện để xem nhé:")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🐢 Rùa và Thỏ")
            # Embed video YouTube (dùng link nhúng an toàn)
            st.video("https://www.youtube.com/watch?v=k_q9461iCw4") 
        with c2:
            st.markdown("### 🐺 Chó Sói và Cừu")
            st.video("https://www.youtube.com/watch?v=0wQ7q0K3Wp0") 

    with tab2:
        st.info("Bố mẹ bấm vào link dưới để mở kho sách truyện khổng lồ cho bé:")
        
        st.markdown("""
        <a href="https://storyweaver.org.in/vi" target="_blank" style="text-decoration: none;">
            <div style="background: #4CAF50; color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold;">
                📖 Mở kho truyện StoryWeaver (Miễn phí)
            </div>
        </a>
        <br>
        <a href="https://giasodau.com/truyen-tranh-ehon-cho-be/" target="_blank" style="text-decoration: none;">
            <div style="background: #2196F3; color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold;">
                📘 Đọc truyện Ehon Nhật Bản
            </div>
        </a>
        """, unsafe_allow_html=True)

# ================== TRANG 4: PHÒNG CA NHẠC ==================
def trang_nhac():
    if st.button("⬅️ Quay lại", key="back_nhac"):
        go_to("home")

    st.markdown('<div class="title-text">🐦 Họa Mi Hót Líu Lo</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image("https://img.youtube.com/vi/3182wcMhXuk/0.jpg")
        st.markdown("**Một con vịt**")
        st.video("https://www.youtube.com/watch?v=3182wcMhXuk")
        
    with c2:
        st.image("https://img.youtube.com/vi/t8b1z_2qYyU/0.jpg")
        st.markdown("**Bống Bống Bang Bang**")
        st.video("https://www.youtube.com/watch?v=t8b1z_2qYyU")

    with c3:
        st.image("https://img.youtube.com/vi/sJ16X-Rz8vU/0.jpg")
        st.markdown("**Cả nhà thương nhau**")
        st.video("https://www.youtube.com/watch?v=sJ16X-Rz8vU")

# ================== MAIN APP LOGIC ==================

# Điều hướng trang
if st.session_state.page == "home":
    trang_chu()
elif st.session_state.page == "toan":
    trang_hoc_toan()
elif st.session_state.page == "truyen":
    trang_truyen()
elif st.session_state.page == "nhac":
    trang_nhac()

# Footer
st.markdown("---")
st.caption("© 2025 - Dự án giáo dục Vùng Cao - Phát triển bởi Giáo viên Tương lai")
