import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time

# ================== 1. CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Bé Vui Học Toán 3D",
    page_icon="🐰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Khởi tạo Session
if "step" not in st.session_state: st.session_state.step = 1
if "num" not in st.session_state: st.session_state.num = 0

# ================== 2. CSS "SIÊU NỔI 3D" & BUTTON KẸO DẺO ==================
st.markdown("""
<style>
    /* 1. NỀN CẦU VỒNG TƯƠI SÁNG */
    .stApp {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
    }

    /* 2. KHUNG CARD 3D BAY LƠ LỬNG */
    .game-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 40px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1), 0 5px 15px rgba(0,0,0,0.05); 
        text-align: center;
        border: 8px solid #fff;
        margin-top: 10px;
        margin-bottom: 30px;
        animation: floatCard 5s ease-in-out infinite;
    }

    @keyframes floatCard {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* 3. SỐ HỌC KHỔNG LỒ */
    .super-number {
        font-size: 160px;
        line-height: 1.2;
        font-weight: 900;
        color: #ff6b6b;
        text-shadow: 5px 5px 0px #fff, 8px 8px 0px rgba(0,0,0,0.1);
        margin: 10px 0;
        animation: pop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    /* 4. BUTTON STYLE "KẸO DẺO" (QUAN TRỌNG NHẤT) */
    div.stButton > button {
        width: 100%;
        height: 75px;
        font-size: 24px !important;
        font-weight: 900 !important;
        color: white !important;
        border: 4px solid white !important; /* Viền trắng tạo độ nổi */
        border-radius: 50px !important; /* Bo tròn như viên kẹo */
        cursor: pointer;
        margin-bottom: 15px;
        text-transform: uppercase;
        box-shadow: 0 6px 0 rgba(0,0,0,0.15), 0 10px 20px rgba(0,0,0,0.1); /* Bóng đổ 3D */
        transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        top: 0;
    }

    /* Hiệu ứng khi bấm nút */
    div.stButton > button:active {
        top: 6px; /* Nút lún xuống */
        box-shadow: 0 0 0 rgba(0,0,0,0.15), inset 0 5px 10px rgba(0,0,0,0.1) !important;
    }

    /* Hiệu ứng Rung (Pulse) cho nút Bắt đầu */
    @keyframes pulse-btn {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation button {
        animation: pulse-btn 1.5s infinite;
    }

    /* 5. ICON MINH HỌA */
    .char-item {
        font-size: 90px;
        display: inline-block;
        margin: 5px;
        filter: drop-shadow(0 8px 5px rgba(0,0,0,0.1)); 
        transition: transform 0.3s;
        cursor: pointer;
    }
    .char-item:hover { transform: scale(1.2) rotate(15deg); }

    .instruction { font-size: 26px; color: #57606f; font-weight: bold; margin-bottom: 10px; }

    @keyframes pop { 0% { transform: scale(0); opacity: 0;} 100% { transform: scale(1); opacity: 1;} }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== 3. XỬ LÝ ÂM THANH ==================
def play_sound_and_wait(text, wait_seconds):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        with st.spinner(f"🔊 Cô đang đọc: '{text}'..."):
            time.sleep(wait_seconds)
    except Exception as e:
        st.error(f"Lỗi: {e}")

def generate_data():
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice([
        ("🐰", "Thỏ"), ("🍎", "Táo"), ("⭐", "Sao"), 
        ("🎈", "Bóng"), ("🍄", "Nấm"), ("🐠", "Cá"),
        ("🚗", "Xe"), ("🦋", "Bươm")
    ])
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices: choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices

if st.session_state.num == 0:
    generate_data()

# ================== 4. GIAO DIỆN CHÍNH ==================

# --- BƯỚC 1: INTRO (TRANG CHỦ) ---
if st.session_state.step == 1:
    st.markdown("""
    <div class="game-card">
        <div style="font-size:120px; margin-bottom:10px; animation: bounce 2s infinite;">🎡</div>
        <h1 style="color:#ff4757; font-size:55px; text-shadow: 4px 4px 0 #fff; margin:0;">BÉ VUI HỌC TOÁN</h1>
        <p class="instruction" style="color:#2ed573;">Vừa học vừa chơi - Thảnh thơi điểm 10</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        # Nút Start: Màu gradient Đỏ Cam Rực Rỡ + Class Pulse
        st.markdown('<div class="pulse-animation">', unsafe_allow_html=True)
        st.markdown("""<style>div.stButton > button {
            background: linear-gradient(to bottom, #ff6b6b, #ee5253) !important;
            border-color: #ff9f43 !important;
            height: 90px !important;
            font-size: 30px !important;
        }</style>""", unsafe_allow_html=True)
        
        if st.button("🚀 BẮT ĐẦU NGAY"):
            play_sound_and_wait("Chào mừng bé! Hôm nay chúng mình cùng học số đếm nhé!", 4)
            st.session_state.step = 2
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- BƯỚC 2: HỌC SỐ ---
elif st.session_state.step == 2:
    st.markdown(f"""
    <div class="game-card">
        <p class="instruction">Bé hãy nhìn xem đây là số mấy?</p>
        <div class="super-number">{st.session_state.num}</div>
    </div>
    """, unsafe_allow_html=True)

    # Hàng 1
    c1, c2 = st.columns(2)
    with c1:
        # Nút Tím (Mộng mơ)
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 NGHE CÂU HỎI"):
            play_sound_and_wait("Bé hãy nhìn xem, đây là số mấy?", 3)
            
    with c2:
        # Nút Xanh Dương (Hy vọng)
        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #74b9ff, #0984e3);}}</style>""", unsafe_allow_html=True)
        if st.button("🗣️ ĐÂY LÀ SỐ...?"):
            play_sound_and_wait(f"Đây là số {st.session_state.num}", 2)

    # Hàng 2
    c3, c4 = st.columns(2)
    with c3:
        # Nút Vàng (Năng động)
        st.markdown(f"""<style>div.stButton:nth-of-type(3) > button {{background: linear-gradient(to bottom, #ffeaa7, #fdcb6e); color: #d35400 !important;}}</style>""", unsafe_allow_html=True)
        if st.button("🔄 ĐỔI SỐ KHÁC"):
            generate_data()
            st.rerun()
            
    with c4:
        # Nút Hồng (Yêu thương) - Nút chuyển tiếp quan trọng
        st.markdown(f"""<style>div.stButton:nth-of-type(4) > button {{background: linear-gradient(to bottom, #fd79a8, #e84393);}}</style>""", unsafe_allow_html=True)
        if st.button("➡️ XEM HÌNH ẢNH"):
            play_sound_and_wait(f"Đúng rồi! Số {st.session_state.num}. Cùng xem hình nhé!", 5)
            st.session_state.step = 3
            st.rerun()

# --- BƯỚC 3: HỌC ĐẾM ---
elif st.session_state.step == 3:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
    <div class="game-card">
        <p class="instruction">Đố bé: Có bao nhiêu <b>{st.session_state.name}</b>?</p>
        <div style="min-height: 120px; margin: 10px 0;">{html_icons}</div>
        <h1 style="font-size: 80px !important; color:#ff6b81; margin:0; text-shadow: 2px 2px 0 #fff;">{st.session_state.num}</h1>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        # Nút Tím
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 NGHE CÂU HỎI"):
            play_sound_and_wait(f"Đố bé biết có bao nhiêu bạn {st.session_state.name} ở đây?", 5)
            
    with c2:
        # Nút Xanh Mint
        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #55efc4, #00b894);}}</style>""", unsafe_allow_html=True)
        if st.button("🔢 ĐẾM CÙNG CÔ"):
            play_sound_and_wait(f"Có tất cả {st.session_state.num} bạn {st.session_state.name}", 3)

    # Nút Bài tập (Cam Đậm) - Nút to
    st.markdown(f"""<style>div.stButton:nth-of-type(3) > button {{background: linear-gradient(to bottom, #fab1a0, #e17055); height: 80px;}}</style>""", unsafe_allow_html=True)
    if st.button("🎮 CHƠI TRÒ CHƠI"):
        play_sound_and_wait("Bây giờ bé hãy tự mình chọn đáp án đúng nhé!", 3)
        st.session_state.step = 4
        st.rerun()

# --- BƯỚC 4: BÀI TẬP ---
elif st.session_state.step == 4:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
    <div class="game-card">
        <p class="instruction">Bé hãy chọn số đúng cho hình này:</p>
        <div style="min-height: 120px; margin-bottom: 20px;">{html_icons}</div>
    </div>
    """, unsafe_allow_html=True)

    # Nút Câu hỏi
    st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
    if st.button("🔊 NGHE CÂU HỎI"):
        play_sound_and_wait("Bé hãy đếm kỹ xem có bao nhiêu hình, rồi bấm vào số đúng ở dưới nhé!", 6)

    # 3 Nút đáp án (Xanh Cyan)
    cols = st.columns(3)
    for idx, choice in enumerate(st.session_state.choices):
        with cols[idx]:
            # Mỗi nút đáp án có màu hơi khác nhau một chút cho sinh động
            colors = [("#81ecec", "#00cec9"), ("#74b9ff", "#0984e3"), ("#a29bfe", "#6c5ce7")]
            c_light, c_dark = colors[idx % 3]
            
            st.markdown(f"""<style>div.stButton:nth-of-type({idx+2}) > button {{background: linear-gradient(to bottom, {c_light}, {c_dark}); font-size: 35px !important;}}</style>""", unsafe_allow_html=True)
            
            if st.button(f"{choice}", key=f"quiz_{idx}"):
                if choice == st.session_state.num:
                    st.balloons()
                    play_sound_and_wait("Chính xác! Bé thông minh quá! Hoan hô!", 4)
                    generate_data()
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("Chưa đúng!")
                    play_sound_and_wait(f"Số {choice} chưa đúng. Bé thử lại nhé!", 3)

    st.write("")
    # Nút Quay lại (Xám) - Nhỏ hơn chút
    st.markdown(f"""<style>div.stButton:last-child > button {{background: linear-gradient(to bottom, #dfe6e9, #b2bec3); color: #636e72 !important; height: 50px; font-size: 18px !important;}}</style>""", unsafe_allow_html=True)
    if st.button("⬅️ QUAY LẠI HỌC SỐ"):
        st.session_state.step = 2
        st.rerun()
