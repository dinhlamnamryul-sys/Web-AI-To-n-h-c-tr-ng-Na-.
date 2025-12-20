import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time

# ================== 1. CẤU HÌNH TRANG (FULL MÀN HÌNH) ==================
st.set_page_config(
    page_title="Bé Vui Học Toán",
    page_icon="🐰",
    layout="centered", # Tập trung vào giữa màn hình cho bé dễ nhìn
    initial_sidebar_state="collapsed" # Ẩn luôn thanh bên
)

# Khởi tạo biến lưu trữ
if "step" not in st.session_state: st.session_state.step = 1
if "num" not in st.session_state: st.session_state.num = 0

# ================== 2. SIÊU GIAO DIỆN (CLEAN & BEAUTIFUL) ==================
st.markdown("""
<style>
    /* 1. NỀN HOẠT HÌNH CHUYỂN ĐỘNG */
    .stApp {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #a18cd1, #fbc2eb);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
    }
    
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* 2. KHUNG CHỨA NỘI DUNG (GLASSMORPHISM) */
    .game-card {
        background: rgba(255, 255, 255, 0.85); /* Nền trắng trong suốt */
        backdrop-filter: blur(10px); /* Hiệu ứng mờ kính */
        border-radius: 40px;
        padding: 40px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
        border: 5px solid #fff;
        text-align: center;
        margin-top: 20px;
    }

    /* 3. ICON VÀ CHỮ */
    .hero-icon {
        font-size: 120px;
        display: inline-block;
        filter: drop-shadow(0 10px 10px rgba(0,0,0,0.2));
        animation: float 3s ease-in-out infinite;
        cursor: pointer;
    }
    
    .char-item {
        font-size: 90px;
        margin: 5px;
        display: inline-block;
        transition: transform 0.2s;
        cursor: pointer;
    }
    .char-item:hover { transform: scale(1.3) rotate(10deg); }

    h1 {
        color: #ff6b81;
        font-size: 60px !important;
        text-shadow: 3px 3px 0 #fff;
        margin: 0;
        padding: 0;
    }
    
    .question {
        font-size: 28px;
        color: #555;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* 4. HIỆU ỨNG BAY LƯỢN */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }

    /* 5. NÚT BẤM 3D (ĐẸP NHẤT) */
    div.stButton > button {
        width: 100%;
        height: 70px;
        border-radius: 25px;
        font-size: 24px;
        font-weight: 900; /* Chữ đậm */
        border: none;
        box-shadow: 0 8px 0 #dfe6e9; /* Tạo khối 3D dưới đáy */
        transition: all 0.1s;
        transform: translateY(0);
        color: white;
        margin-bottom: 10px;
    }

    /* Khi bấm nút thì nút lún xuống */
    div.stButton > button:active {
        transform: translateY(8px);
        box-shadow: 0 0 0 #dfe6e9;
    }

    /* Màu sắc riêng cho từng nút */
    /* Nút Đọc (Xanh lá) */
    div.stButton > button:first-child { background: #2ecc71; box-shadow: 0 8px 0 #27ae60; }
    /* Nút Đổi câu (Vàng) */
    div.stButton > button:nth-child(1) { background: #f1c40f; box-shadow: 0 8px 0 #f39c12; } 
    /* Nút Bài tập (Xanh dương) */
    div.stButton > button:last-child { background: #3498db; box-shadow: 0 8px 0 #2980b9; }

    /* Ẩn menu mặc định của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ================== 3. LOGIC XỬ LÝ ==================
def play_sound(text, delay=0):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        if delay > 0:
            with st.spinner("⏳ Cô đang nói..."):
                time.sleep(delay)
    except:
        pass

def generate_question():
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice([
        ("🐰", "Chú Thỏ"), ("🍎", "Quả Táo"), ("⭐", "Ngôi Sao"), 
        ("🎈", "Bóng Bay"), ("🍄", "Cây Nấm"), ("🐠", "Con Cá"),
        ("🐣", "Gà Con"), ("🦋", "Bươm Bướm"), ("🚗", "Ô Tô")
    ])
    # Tạo đáp án trắc nghiệm
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices: choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices

# Tạo câu hỏi lần đầu
if st.session_state.num == 0:
    generate_question()

# ================== 4. GIAO DIỆN CHÍNH ==================

# --- MÀN HÌNH 1: CHÀO MỪNG ---
if st.session_state.step == 1:
    st.markdown("""
    <div class="game-card">
        <div style="font-size: 130px; animation: float 3s infinite;">🎡</div>
        <h1>BÉ VUI HỌC TOÁN</h1>
        <p class="question">Ứng dụng học đếm thông minh cho bé</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Nút bắt đầu to ở giữa
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 BẮT ĐẦU CHƠI", type="primary"):
            play_sound("Chào mừng bé! Chúng mình cùng đi đếm số nhé!", delay=3)
            st.session_state.step = 2
            st.rerun()

# --- MÀN HÌNH 2: HỌC ĐẾM ---
elif st.session_state.step == 2:
    # Tạo hình ảnh icon
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
    <div class="game-card">
        <p class="question">Bé hãy đếm xem có bao nhiêu <b>{st.session_state.name}</b>?</p>
        <div style="min-height: 150px;">{html_icons}</div>
        <hr style="border: 2px dashed #eee;">
        <h1 style="color: #ff4757; font-size: 100px;">{st.session_state.num}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # 3 Nút chức năng
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔊 Đọc mẫu"):
            play_sound(f"Có {st.session_state.num} {st.session_state.name}")
    with c2:
        if st.button("🔄 Đổi câu"):
            generate_question()
            st.rerun()
    with c3:
        if st.button("➡️ Bài tập"):
            play_sound("Bây giờ bé hãy chọn đáp án đúng nhé!", delay=2.5)
            st.session_state.step = 3
            st.rerun()

# --- MÀN HÌNH 3: TRẮC NGHIỆM ---
elif st.session_state.step == 3:
    # Chỉ hiện hình, không hiện số
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
    <div class="game-card">
        <p class="question">Đố bé biết có bao nhiêu {st.session_state.name}?</p>
        <div style="min-height: 150px;">{html_icons}</div>
        <p style="color:#aaa; font-size:16px;">(Bé hãy bấm vào số đúng bên dưới nhé)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 3 Nút đáp án to
    cols = st.columns(3)
    for idx, choice in enumerate(st.session_state.choices):
        with cols[idx]:
            # CSS hack để chỉnh màu nút đáp án cho đẹp
            if st.button(f"{choice}", key=f"btn_{idx}"):
                if choice == st.session_state.num:
                    st.balloons() # Bóng bay
                    st.success("🎉 CHÍNH XÁC! BÉ GIỎI QUÁ!")
                    play_sound("Hoan hô! Bé trả lời đúng rồi!", delay=2)
                    generate_question() # Tạo câu mới
                    st.session_state.step = 2 # Quay về màn hình học
                    st.rerun()
                else:
                    st.error("SAI RỒI! BÉ ĐẾM LẠI NHÉ!")
                    play_sound("Chưa đúng đâu. Bé thử lại nhé!")

    st.write("")
    st.write("")
    if st.button("⬅️ Quay lại học đếm"):
        st.session_state.step = 2
        st.rerun()
