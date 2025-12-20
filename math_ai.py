import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time

# ================== 1. CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Bé Vui Học Toán",
    page_icon="🐰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Khởi tạo biến
if "step" not in st.session_state: st.session_state.step = 1
if "num" not in st.session_state: st.session_state.num = 0

# ================== 2. GIAO DIỆN (CSS GAME ĐẸP MẮT) ==================
st.markdown("""
<style>
    /* Nền chuyển màu hoạt hình */
    .stApp {
        background: linear-gradient(-45deg, #a18cd1, #fbc2eb, #fad0c4, #ff9a9e);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Khung nội dung (Card) */
    .game-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 40px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        border: 4px solid #fff;
        text-align: center;
        margin-top: 20px;
        backdrop-filter: blur(10px);
    }

    /* Tiêu đề câu hỏi */
    .question {
        font-size: 26px;
        color: #555;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Số học to đùng */
    .big-number {
        font-size: 150px;
        font-weight: 900;
        color: #ff6b81;
        text-shadow: 4px 4px 0px #fff, 6px 6px 0px rgba(0,0,0,0.1);
        margin: 0;
        line-height: 1.2;
        animation: pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    /* Icon nhân vật */
    .char-item {
        font-size: 80px;
        margin: 5px;
        display: inline-block;
        transition: transform 0.2s;
        cursor: pointer;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes pop {
        0% { transform: scale(0); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    /* NÚT BẤM 3D */
    div.stButton > button {
        width: 100%;
        height: 70px;
        border-radius: 20px;
        font-size: 22px;
        font-weight: bold;
        border: none;
        color: white;
        margin-bottom: 10px;
        transition: transform 0.1s;
        box-shadow: 0 6px 0 rgba(0,0,0,0.2);
    }
    div.stButton > button:active {
        transform: translateY(6px);
        box-shadow: none;
    }
    
    /* Màu nút tùy chỉnh */
    .btn-green { background: #2ecc71 !important; } /* Nút Nghe */
    .btn-blue { background: #3498db !important; }  /* Nút Tiếp */
    .btn-orange { background: #f39c12 !important; } /* Nút Đổi */

    /* Ẩn footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ================== 3. LOGIC HỆ THỐNG ==================
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

if st.session_state.num == 0:
    generate_question()

# ================== 4. GIAO DIỆN CHÍNH (FLOW MỚI) ==================

# --- BƯỚC 1: MÀN HÌNH CHÀO ---
if st.session_state.step == 1:
    st.markdown("""
    <div class="game-card">
        <div style="font-size: 100px;">👋</div>
        <h1 style="color:#ff6b81;">BÉ VUI HỌC TOÁN</h1>
        <p class="question">Chào mừng bé đến với lớp học AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 BẮT ĐẦU HỌC"):
            play_sound("Chào mừng bé! Hôm nay chúng mình cùng học số nhé!", delay=3)
            st.session_state.step = 2
            st.rerun()

# --- BƯỚC 2: NHẬN BIẾT SỐ (MỚI THÊM) ---
elif st.session_state.step == 2:
    st.markdown(f"""
    <div class="game-card">
        <p class="question">Đố bé đây là số mấy?</p>
        <p class="big-number">{st.session_state.num}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        # Nút nghe
        if st.button("🔊 Nghe tên số"):
            play_sound(f"Đây là số {st.session_state.num}")
    with c2:
        # Nút đổi số khác nếu bé chán
        if st.button("🔄 Số khác"):
            generate_question()
            st.rerun()
    with c3:
        # Nút chuyển sang đếm hình
        if st.button("➡️ Xem hình"):
            play_sound(f"Đúng rồi, đây là số {st.session_state.num}. Bây giờ chúng mình cùng tập đếm nhé!", delay=4)
            st.session_state.step = 3
            st.rerun()

# --- BƯỚC 3: HỌC ĐẾM TƯƠNG ỨNG (CŨ LÀ BƯỚC 2) ---
elif st.session_state.step == 3:
    # Tạo hình ảnh
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
    <div class="game-card">
        <p class="question">Có bao nhiêu <b>{st.session_state.name}</b> ở đây nhỉ?</p>
        <div style="min-height: 120px;">{html_icons}</div>
        <hr style="border: 2px dashed #eee;">
        <h1 style="font-size: 80px; color: #ff4757; margin:0;">{st.session_state.num}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔊 Đếm cùng cô"):
            play_sound(f"Có tất cả {st.session_state.num} {st.session_state.name}")
    with c2:
        if st.button("➡️ Làm bài tập"):
            play_sound("Bây giờ bé hãy tự chọn đáp án đúng nhé!", delay=2.5)
            st.session_state.step = 4
            st.rerun()

# --- BƯỚC 4: TRẮC NGHIỆM KIỂM TRA ---
elif st.session_state.step == 4:
    # Chỉ hiện hình, không hiện số
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
    <div class="game-card">
        <p class="question">Bé hãy chọn số đúng cho hình này:</p>
        <div style="min-height: 120px;">{html_icons}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3 Nút đáp án
    cols = st.columns(3)
    for idx, choice in enumerate(st.session_state.choices):
        with cols[idx]:
            if st.button(f"{choice}", key=f"ans_{idx}"):
                if choice == st.session_state.num:
                    st.balloons()
                    st.success("🎉 CHÍNH XÁC! BÉ GIỎI QUÁ!")
                    play_sound("Hoan hô! Bé trả lời đúng rồi!", delay=2)
                    
                    # QUAY LẠI BƯỚC 2 (HỌC SỐ MỚI)
                    generate_question()
                    st.session_state.step = 2 
                    st.rerun()
                else:
                    st.error("SAI RỒI! BÉ ĐẾM LẠI NHÉ!")
                    play_sound("Chưa đúng đâu. Bé thử lại đi!")

    st.write("")
    # Nút quay lại học nếu quên
    if st.button("⬅️ Quay lại học số"):
        st.session_state.step = 2
        st.rerun()
