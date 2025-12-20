import streamlit as st
import requests
from streamlit_lottie import st_lottie
from gtts import gTTS
import os
import uuid
import time
import random

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(page_title="Thế Giới Của Bé", page_icon="🌈", layout="wide")

# ================== HÀM TẢI HOẠT HÌNH (LOTTIE) ==================
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Tải sẵn các hoạt hình dễ thương
lottie_welcome = load_lottieurl("https://lottie.host/5a0c968f-955a-4951-9257-657803565072/G8w9TqXqjW.json") # Gấu vẫy tay
lottie_success = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_lk80fpsm.json") # Pháo hoa
lottie_math = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_4kji20Y93r.json") # Số nhảy múa
lottie_music = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_sSf5uQ.json") # Nốt nhạc

# ================== CSS MÀU SẮC RỰC RỠ ==================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        font-family: 'Patrick Hand', cursive; /* Font chữ viết tay giống trẻ con */
    }
    
    /* Tiêu đề lớn */
    h1, h2, h3 {
        color: #FF6F00 !important;
        text-shadow: 2px 2px 0px #FFD54F;
    }
    
    /* Khung nội dung nổi bật */
    .content-box {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 4px solid #4FC3F7;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Nút bấm to đùng */
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        height: 60px;
        font-size: 24px;
        font-weight: bold;
        background-color: #FF4081;
        color: white;
        border: none;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background-color: #F50057;
    }
</style>
""", unsafe_allow_html=True)

# ================== HÀM PHÁT ÂM THANH ==================
def noi_chuyen(text):
    try:
        filename = f"voice_{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang='vi')
        tts.save(filename)
        st.audio(open(filename, "rb").read(), format="audio/mp3", autoplay=True)
        os.remove(filename)
    except:
        pass

# ================== GIAO DIỆN CHÍNH ==================

# --- Header ---
c1, c2 = st.columns([1, 4])
with c1:
    st_lottie(lottie_welcome, height=150, key="welcome")
with c2:
    st.markdown("<h1 style='font-size: 60px; margin-top: 30px;'>🌈 VƯƠNG QUỐC CỦA BÉ</h1>", unsafe_allow_html=True)

# --- Menu Tab ---
tab1, tab2, tab3 = st.tabs(["🧮 HỌC TOÁN VUI", "📺 RẠP CHIẾU PHIM", "🎵 SÂN KHẤU CA NHẠC"])

# ================== TAB 1: HỌC TOÁN (GAME) ==================
with tab1:
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st_lottie(lottie_math, height=200, key="math_anim")
        st.markdown("### Bé ơi, đếm kẹo nào!", unsafe_allow_html=True)
        
        # Logic Game
        if 'so_keo' not in st.session_state:
            st.session_state.so_keo = random.randint(1, 5)
            
        # Hiển thị kẹo (Dùng emoji to)
        html_keo = "".join(["<span style='font-size:50px;'>🍬</span>"] * st.session_state.so_keo)
        st.markdown(html_keo, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.info("Bé hãy chọn số kẹo đúng nhé:")
        # Tạo 3 nút đáp án (1 đúng, 2 sai)
        dap_an_dung = st.session_state.so_keo
        lua_chon = [dap_an_dung, dap_an_dung + 1, abs(dap_an_dung - 1)]
        if dap_an_dung == 1: lua_chon = [1, 2, 3]
        random.shuffle(lua_chon) # Xáo trộn vị trí
        
        def check_ans(x):
            if x == st.session_state.so_keo:
                st.balloons()
                st_lottie(lottie_success, height=150, key="win")
                noi_chuyen("Hoan hô! Bé giỏi quá! Đúng rồi!")
                time.sleep(2)
                st.session_state.so_keo = random.randint(1, 9)
                st.rerun()
            else:
                st.error("Chưa đúng, bé đếm lại nhé!")
                noi_chuyen("Tiếc quá, bé thử lại nào!")

        c_btn1, c_btn2, c_btn3 = st.columns(3)
        with c_btn1:
            if st.button(f"Số {lua_chon[0]}", key="b1"): check_ans(lua_chon[0])
        with c_btn2:
            if st.button(f"Số {lua_chon[1]}", key="b2"): check_ans(lua_chon[1])
        with c_btn3:
            if st.button(f"Số {lua_chon[2]}", key="b3"): check_ans(lua_chon[2])

# ================== TAB 2: RẠP CHIẾU PHIM (Cổ tích) ==================
with tab2:
    st.markdown("### 🍿 Hôm nay Gấu Kể Chuyện gì nào?", unsafe_allow_html=True)
    
    # Chọn truyện
    truyen = st.radio("Bé muốn xem truyện gì?", ["Thỏ và Rùa", "Ba Chú Heo Con", "Cậu Bé Chăn Cừu"], horizontal=True)
    
    col_video, col_info = st.columns([2, 1])
    
    with col_video:
        if truyen == "Thỏ và Rùa":
            # Link youtube embed sạch (ko quảng cáo nếu có thể)
            st.video("https://www.youtube.com/watch?v=k_q9461iCw4")
            if st.button("🔊 Nghe Gấu giới thiệu"):
                noi_chuyen("Đây là câu chuyện về bạn Thỏ ham chơi và bạn Rùa chăm chỉ. Bé xem ai về đích trước nhé!")
        elif truyen == "Ba Chú Heo Con":
            st.video("https://www.youtube.com/watch?v=O1fAfaM7hKY")
        elif truyen == "Cậu Bé Chăn Cừu":
            st.video("https://www.youtube.com/watch?v=vJz5-g-V8f4")

    with col_info:
        st.info("💡 Bài học: Bé nhớ phải chăm chỉ, không được lười biếng và nói dối nhé!")
        st.image("https://cdn-icons-png.flaticon.com/512/3767/3767036.png", width=150)

# ================== TAB 3: SÂN KHẤU CA NHẠC ==================
with tab3:
    c_nhac1, c_nhac2 = st.columns([1, 2])
    
    with c_nhac1:
        st_lottie(lottie_music, height=200, key="music_dance")
        st.markdown("### 💃 Cùng nhảy nào!", unsafe_allow_html=True)
    
    with c_nhac2:
        list_nhac = st.selectbox("Chọn bài hát bé thích:", ["Một Con Vịt", "Baby Shark (Việt)", "Bống Bống Bang Bang"])
        
        if list_nhac == "Một Con Vịt":
            st.video("https://www.youtube.com/watch?v=3182wcMhXuk")
        elif list_nhac == "Baby Shark (Việt)":
            st.video("https://www.youtube.com/watch?v=d_U_sQ6v_2E")
        elif list_nhac == "Bống Bống Bang Bang":
            st.video("https://www.youtube.com/watch?v=t8b1z_2qYyU")

# ================== FOOTER ==================
st.markdown("---")
st.caption("🌟 Ứng dụng AI Giáo dục cho Mầm non - Phiên bản Rực rỡ 🌟")
