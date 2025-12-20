import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time

# ================== 1. CẤU HÌNH TRANG CHUYÊN NGHIỆP ==================
st.set_page_config(
    page_title="Math Kids Pro",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Khởi tạo Session
if "step" not in st.session_state: st.session_state.step = 1
if "num" not in st.session_state: st.session_state.num = 0

# ================== 2. CSS ĐẲNG CẤP (3D & NEUMORPHISM) ==================
st.markdown("""
<style>
    /* 1. NỀN CHUYỂN ĐỘNG */
    .stApp {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        font-family: 'Segoe UI', 'Roboto', Helvetica, Arial, sans-serif;
    }

    /* 2. KHUNG CARD CHÍNH */
    .pro-card {
        background-color: #ffffff;
        border-radius: 35px;
        padding: 30px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
        text-align: center;
        border: 6px solid #fff;
        margin-top: 10px;
        margin-bottom: 20px;
        position: relative;
    }

    /* 3. CHỮ SỐ SIÊU TO */
    .super-number {
        font-size: 160px;
        line-height: 1.1;
        font-weight: 900;
        background: -webkit-linear-gradient(#ff6b6b, #ff8e53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(4px 4px 0px rgba(0,0,0,0.1));
        animation: popIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        margin: 10px 0;
    }

    /* 4. CHỮ HƯỚNG DẪN */
    .instruction {
        font-size: 1.4rem;
        color: #57606f;
        font-weight: 700;
        margin-bottom: 10px;
    }

    /* 5. NÚT BẤM 3D CAO CẤP */
    div.stButton > button {
        width: 100%;
        height: 70px;
        font-size: 20px;
        font-weight: 800;
        text-transform: uppercase;
        color: white;
        border: none;
        border-radius: 18px;
        cursor: pointer;
        transition: all 0.1s;
        box-shadow: 0 6px 0 rgba(0,0,0,0.2); /* Đổ bóng 3D */
        margin-bottom: 10px;
    }

    div.stButton > button:active {
        transform: translateY(6px); /* Hiệu ứng lún xuống */
        box-shadow: 0 0 0 rgba(0,0,0,0.2);
    }

    /* MÀU NÚT THEO CHỨC NĂNG */
    /* Màu Tím (Nghe câu hỏi) */
    .btn-question { background: linear-gradient(to bottom, #a55eea, #8854d0); }
    
    /* Màu Xanh Lá (Nghe đáp án/Đếm) */
    .btn-answer { background: linear-gradient(to bottom, #26de81, #20bf6b); }
    
    /* Màu Vàng (Đổi số) */
    .btn-change { background: linear-gradient(to bottom, #fed330, #f7b731); }
    
    /* Màu Xanh Dương (Tiếp theo) */
    .btn-next { background: linear-gradient(to bottom, #45aaf2, #2d98da); }

    /* ICON */
    .char-item {
        font-size: 80px;
        display: inline-block;
        margin: 5px;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes popIn { 0% { transform: scale(0); } 100% { transform: scale(1); } }
    @keyframes float { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-10px);} }

    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== 3. XỬ LÝ ÂM THANH (BLOCKING) ==================
def play_sound_and_wait(text, wait_seconds):
    """Đọc âm thanh và bắt buộc chờ đọc xong"""
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        with st.spinner(f"🔊 Cô đang đọc: '{text}'..."):
            time.sleep(wait_seconds)
    except Exception as e:
        st.error(f"Lỗi âm thanh: {e}")

def generate_data():
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice([
        ("🐰", "Thỏ"), ("🍎", "Táo"), ("⭐", "Sao"), 
        ("🎈", "Bóng"), ("🍄", "Nấm"), ("🐠", "Cá"),
        ("🚗", "Xe"), ("🦋", "Bướm")
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
    <div class="pro-card">
        <div style="font-size:100px; animation: float 3s infinite;">🎓</div>
        <h1>MATH KIDS PRO</h1>
        <p class="instruction">Học toán tư duy cùng AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("🚀 BẮT ĐẦU HỌC"):
            play_sound_and_wait("Chào mừng bé! Hôm nay chúng mình cùng học số đếm nhé!", 3)
            st.session_state.step = 2
            st.rerun()

# --- BƯỚC 2: NHẬN BIẾT SỐ (CÓ NÚT ĐỌC CÂU HỎI) ---
elif st.session_state.step == 2:
    st.markdown(f"""
    <div class="pro-card">
        <p class="instruction">Bé hãy nhìn xem đây là số mấy?</p>
        <div class="super-number">{st.session_state.num}</div>
    </div>
    """, unsafe_allow_html=True)

    # Hàng nút 1: Nghe câu hỏi & Nghe đáp án
    c1, c2 = st.columns(2)
    with c1:
        # Nút mới bạn yêu cầu
        if st.button("🔊 NGHE CÂU HỎI"):
            play_sound_and_wait("Bé hãy nhìn xem, đây là số mấy?", 3)
    with c2:
        if st.button("🗣️ ĐÂY LÀ SỐ...?"):
            play_sound_and_wait(f"Đây là số {st.session_state.num}", 2)

    # Hàng nút 2: Đổi số & Tiếp tục
    c3, c4 = st.columns(2)
    with c3:
        if st.button("🔄 ĐỔI SỐ KHÁC"):
            generate_data()
            st.rerun()
    with c4:
        if st.button("➡️ XEM HÌNH ẢNH"):
            play_sound_and_wait(f"Đúng rồi! Số {st.session_state.num}. Cùng xem hình nhé!", 3)
            st.session_state.step = 3
            st.rerun()

# --- BƯỚC 3: HỌC ĐẾM (CÓ NÚT ĐỌC CÂU HỎI) ---
elif st.session_state.step == 3:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
    <div class="pro-card">
        <p class="instruction">Đố bé: Có bao nhiêu <b>{st.session_state.name}</b> ở đây?</p>
        <div style="min-height: 120px; margin: 10px 0;">{html_icons}</div>
        <h1 style="font-size: 60px !important; margin:0; color:#555;">{st.session_state.num}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Hàng nút 1
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔊 NGHE CÂU HỎI"):
            play_sound_and_wait(f"Đố bé biết có bao nhiêu bạn {st.session_state.name} ở đây?", 4)
    with c2:
        if st.button("1️⃣2️⃣3️⃣ ĐẾM CÙNG CÔ"):
            play_sound_and_wait(f"Có tất cả {st.session_state.num} bạn {st.session_state.name}", 3)
            
    # Hàng nút 2 (Full width)
    if st.button("➡️ LÀM BÀI TẬP KIỂM TRA"):
        play_sound_and_wait("Bây giờ bé hãy tự mình chọn đáp án đúng nhé!", 3)
        st.session_state.step = 4
        st.rerun()

# --- BƯỚC 4: TRẮC NGHIỆM (CÓ NÚT ĐỌC CÂU HỎI) ---
elif st.session_state.step == 4:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
    <div class="pro-card">
        <p class="instruction">Bé hãy chọn số đúng cho hình này:</p>
        <div style="min-height: 120px; margin-bottom: 20px;">{html_icons}</div>
    </div>
    """, unsafe_allow_html=True)

    # Nút đọc câu hỏi cho phần thi
    if st.button("🔊 ĐỌC CÂU HỎI BÀI THI"):
        play_sound_and_wait("Bé hãy đếm kỹ xem có bao nhiêu hình, rồi bấm vào số đúng ở dưới nhé!", 5)

    # 3 Nút đáp án
    cols = st.columns(3)
    for idx, choice in enumerate(st.session_state.choices):
        with cols[idx]:
            if st.button(f"{choice}", key=f"quiz_{idx}"):
                if choice == st.session_state.num:
                    st.balloons()
                    play_sound_and_wait("Chính xác! Bé thông minh quá! Hoan hô!", 3)
                    generate_data()
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("Chưa đúng!")
                    play_sound_and_wait(f"Số {choice} chưa đúng. Bé thử lại nhé!", 3)

    st.write("")
    if st.button("⬅️ QUAY LẠI HỌC SỐ"):
        st.session_state.step = 2
        st.rerun()

# Footer 3D
st.markdown("""
<div style='text-align:center; margin-top:40px; color:#fff; font-weight:bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.2)'>
    AI EDU SYSTEM PRO 2025
</div>
""", unsafe_allow_html=True)
