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

# ================== 2. CSS "SIÊU NỔI 3D" (GIỮ NGUYÊN ĐỘ ĐẸP) ==================
st.markdown("""
<style>
    /* 1. NỀN CẦU VỒNG */
    .stApp {
        background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }

    /* 2. KHUNG CARD 3D */
    .game-card {
        background-color: #ffffff;
        border-radius: 40px;
        padding: 30px;
        box-shadow: 0 20px 0 rgba(0,0,0,0.1), 0 40px 60px rgba(0,0,0,0.1); 
        text-align: center;
        border: 5px solid #fff;
        margin-top: 10px;
        margin-bottom: 30px;
        animation: floatCard 6s ease-in-out infinite;
    }

    @keyframes floatCard {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }

    /* 3. SỐ HỌC 3D */
    .super-number {
        font-size: 160px;
        line-height: 1.2;
        font-weight: 900;
        color: #ff4757;
        text-shadow: 4px 4px 0px #ffffff, 8px 8px 0px rgba(0,0,0,0.15);
        margin: 10px 0;
        animation: pop 0.5s;
    }

    /* 4. NÚT BẤM 3D (ĐÃ CHỈNH LẠI MÀU CHO ĐẸP) */
    div.stButton > button {
        width: 100%;
        height: 70px;
        font-size: 22px;
        font-weight: 900 !important;
        color: white;
        border: none;
        border-radius: 20px;
        cursor: pointer;
        position: relative;
        top: 0;
        transition: all 0.1s;
        margin-bottom: 15px;
        text-transform: uppercase;
        box-shadow: 0 8px 0 rgba(0,0,0,0.2); 
    }

    div.stButton > button:active {
        top: 8px;
        box-shadow: 0 0 0 rgba(0,0,0,0.2); 
    }

    /* 5. ICON NỔI */
    .char-item {
        font-size: 90px;
        display: inline-block;
        margin: 5px;
        filter: drop-shadow(0 5px 0px rgba(0,0,0,0.15)); 
        transition: transform 0.2s;
    }
    .char-item:hover { transform: scale(1.2) rotate(10deg); }

    .instruction { font-size: 24px; color: #555; font-weight: bold; margin-bottom: 15px; }

    @keyframes pop { 0% { transform: scale(0); } 100% { transform: scale(1); } }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== 3. XỬ LÝ ÂM THANH (ĐÃ TĂNG THỜI GIAN CHỜ) ==================
def play_sound_and_wait(text, wait_seconds):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        # Hiển thị thông báo để người dùng biết đang chờ âm thanh
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

# --- BƯỚC 1: INTRO ---
if st.session_state.step == 1:
    st.markdown("""
    <div class="game-card">
        <div style="font-size:110px; margin-bottom:10px;">🎡</div>
        <h1 style="color:#ff6b81; font-size:50px; text-shadow: 3px 3px 0 #fff;">BÉ VUI HỌC TOÁN</h1>
        <p class="instruction">Học đếm số cùng AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        # Nút Bắt đầu (Xanh lá)
        st.markdown("""<style>div.stButton > button {background: linear-gradient(to bottom, #2ecc71, #27ae60) !important;}</style>""", unsafe_allow_html=True)
        
        if st.button("🚀 BẮT ĐẦU NGAY"):
            # Tăng lên 4 giây cho câu chào
            play_sound_and_wait("Chào mừng bé! Hôm nay chúng mình cùng học số đếm nhé!", 4)
            st.session_state.step = 2
            st.rerun()

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
        # Nút Nghe câu hỏi (Tím)
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a55eea, #8854d0);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 NGHE CÂU HỎI"):
            play_sound_and_wait("Bé hãy nhìn xem, đây là số mấy?", 3)
            
    with c2:
        # Nút Nghe tên số (Xanh Dương)
        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #3498db, #2980b9);}}</style>""", unsafe_allow_html=True)
        if st.button("🗣️ ĐÂY LÀ SỐ...?"):
            play_sound_and_wait(f"Đây là số {st.session_state.num}", 2)

    # Hàng 2
    c3, c4 = st.columns(2)
    with c3:
        # Nút Đổi số (Vàng)
        st.markdown(f"""<style>div.stButton:nth-of-type(3) > button {{background: linear-gradient(to bottom, #f1c40f, #f39c12);}}</style>""", unsafe_allow_html=True)
        if st.button("🔄 ĐỔI SỐ KHÁC"):
            generate_data()
            st.rerun()
            
    with c4:
        # Nút Tiếp theo (Hồng)
        st.markdown(f"""<style>div.stButton:nth-of-type(4) > button {{background: linear-gradient(to bottom, #ff9ff3, #f368e0);}}</style>""", unsafe_allow_html=True)
        if st.button("➡️ XEM HÌNH ẢNH"):
            # --- ĐÃ SỬA: Tăng thời gian chờ lên 5 giây ---
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
        <h1 style="font-size: 80px !important; color:#ff6b81; text-shadow: 2px 2px 0 #fff;">{st.session_state.num}</h1>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        # Nút Câu hỏi (Tím)
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a55eea, #8854d0);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 NGHE CÂU HỎI"):
            # Tăng lên 5 giây vì câu hỏi dài
            play_sound_and_wait(f"Đố bé biết có bao nhiêu bạn {st.session_state.name} ở đây?", 5)
            
    with c2:
        # Nút Đếm (Xanh lá)
        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #2ecc71, #27ae60);}}</style>""", unsafe_allow_html=True)
        if st.button("🔢 ĐẾM CÙNG CÔ"):
            play_sound_and_wait(f"Có tất cả {st.session_state.num} bạn {st.session_state.name}", 3)

    # Nút Bài tập (Cam)
    st.markdown(f"""<style>div.stButton:nth-of-type(3) > button {{background: linear-gradient(to bottom, #ff9f43, #ee5253);}}</style>""", unsafe_allow_html=True)
    if st.button("➡️ LÀM BÀI TẬP"):
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

    # Nút Câu hỏi (Tím)
    st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a55eea, #8854d0);}}</style>""", unsafe_allow_html=True)
    if st.button("🔊 NGHE CÂU HỎI"):
        # Tăng lên 6 giây cho chắc
        play_sound_and_wait("Bé hãy đếm kỹ xem có bao nhiêu hình, rồi bấm vào số đúng ở dưới nhé!", 6)

    # 3 Nút đáp án (Xanh biển)
    cols = st.columns(3)
    for idx, choice in enumerate(st.session_state.choices):
        with cols[idx]:
            st.markdown(f"""<style>div.stButton:nth-of-type({idx+2}) > button {{background: linear-gradient(to bottom, #48dbfb, #0abde3);}}</style>""", unsafe_allow_html=True)
            
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
    # Nút Quay lại (Xám)
    st.markdown(f"""<style>div.stButton:last-child > button {{background: linear-gradient(to bottom, #95a5a6, #7f8c8d); height: 50px; font-size: 18px;}}</style>""", unsafe_allow_html=True)
    if st.button("⬅️ QUAY LẠI HỌC SỐ"):
        st.session_state.step = 2
        st.rerun()
