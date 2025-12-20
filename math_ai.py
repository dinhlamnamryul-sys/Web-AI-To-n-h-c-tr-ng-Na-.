import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time

# ================== 1. CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Bé Vui Học Toán 3D",
    page_icon="🐰",
    layout="wide",  # Đổi sang wide để có không gian chiều ngang
    initial_sidebar_state="collapsed"
)

# Khởi tạo Session
if "step" not in st.session_state: st.session_state.step = 1
if "num" not in st.session_state: st.session_state.num = 0

# ================== 2. CSS "SIÊU NỔI" & BUTTON (GIỮ NGUYÊN STYLE ĐẸP) ==================
st.markdown("""
<style>
    /* Nền cầu vồng */
    .stApp {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
    }

    /* Card hiển thị (Bên phải) */
    .game-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 40px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); 
        text-align: center;
        border: 6px solid #fff;
        animation: floatCard 5s ease-in-out infinite;
        height: 100%; /* Để card cân đối */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    @keyframes floatCard {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* Số khổng lồ */
    .super-number {
        font-size: 140px;
        line-height: 1.1;
        font-weight: 900;
        color: #ff6b6b;
        text-shadow: 4px 4px 0px #fff;
        margin: 0;
    }

    /* BUTTON STYLE "KẸO DẺO" */
    div.stButton > button {
        width: 100%;
        height: 65px; /* Giảm chiều cao chút cho gọn */
        font-size: 18px !important; /* Chữ vừa phải để không bị tràn */
        font-weight: 800 !important;
        color: white !important;
        border: 3px solid white !important;
        border-radius: 30px !important;
        cursor: pointer;
        margin-bottom: 12px; /* Khoảng cách giữa các nút */
        box-shadow: 0 5px 0 rgba(0,0,0,0.15);
        transition: all 0.2s;
    }

    div.stButton > button:active {
        top: 4px;
        box-shadow: 0 0 0 rgba(0,0,0,0.15);
    }

    .char-item {
        font-size: 80px;
        display: inline-block;
        margin: 5px;
        filter: drop-shadow(0 5px 2px rgba(0,0,0,0.1)); 
    }
    
    .instruction { font-size: 22px; color: #57606f; font-weight: bold; }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Chỉnh container để nút không bị quá to */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }
</style>
""", unsafe_allow_html=True)

# ================== 3. HÀM XỬ LÝ ==================
def play_sound_and_wait(text, wait_seconds):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        with st.spinner(f"🔊 Cô đang nói..."):
            time.sleep(wait_seconds)
    except Exception as e:
        st.error(f"Lỗi âm thanh: {e}")

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

# ================== 4. GIAO DIỆN CHÍNH (LAYOUT MỚI) ==================

# --- BƯỚC 1: INTRO (Vẫn giữ giữa cho đẹp, nhưng nút gọn lại) ---
if st.session_state.step == 1:
    st.markdown("""
    <div class="game-card" style="padding: 50px;">
        <div style="font-size:100px; margin-bottom:10px;">🎡</div>
        <h1 style="color:#ff4757; font-size:50px;">BÉ VUI HỌC TOÁN</h1>
        <p class="instruction">Học mà chơi - Chơi mà học</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.markdown("""<style>div.stButton > button {background: linear-gradient(to bottom, #ff6b6b, #ee5253); height: 80px; font-size: 24px !important;}</style>""", unsafe_allow_html=True)
        if st.button("🚀 BẮT ĐẦU NGAY"):
            play_sound_and_wait("Chào mừng bé! Hôm nay chúng mình cùng học số đếm nhé!", 3)
            st.session_state.step = 2
            st.rerun()

# --- BƯỚC 2: HỌC SỐ (LAYOUT CỘT TRÁI - PHẢI) ---
elif st.session_state.step == 2:
    
    # Chia cột: Cột 1 (3 phần) chứa nút, Cột 2 (7 phần) chứa hình
    col_controls, col_display = st.columns([3, 7], gap="large")

    with col_controls:
        st.markdown("### 🎮 Điều khiển")
        
        # 1. Nút Nghe (Tím)
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 Nghe câu hỏi"):
            play_sound_and_wait("Bé hãy nhìn xem, đây là số mấy?", 3)

        # 2. Nút Đọc (Xanh)
        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #74b9ff, #0984e3);}}</style>""", unsafe_allow_html=True)
        if st.button("🗣️ Đây là số...?"):
            play_sound_and_wait(f"Đây là số {st.session_state.num}", 2)

        # 3. Nút Đổi số (Vàng)
        st.markdown(f"""<style>div.stButton:nth-of-type(3) > button {{background: linear-gradient(to bottom, #ffeaa7, #fdcb6e); color: #d35400 !important;}}</style>""", unsafe_allow_html=True)
        if st.button("🔄 Đổi số khác"):
            generate_data()
            st.rerun()

        # 4. Nút Tiếp (Hồng)
        st.markdown(f"""<style>div.stButton:nth-of-type(4) > button {{background: linear-gradient(to bottom, #fd79a8, #e84393);}}</style>""", unsafe_allow_html=True)
        if st.button("➡️ Xem hình ảnh"):
            play_sound_and_wait(f"Đúng rồi! Số {st.session_state.num}. Cùng xem hình nhé!", 4)
            st.session_state.step = 3
            st.rerun()

    with col_display:
        st.markdown(f"""
        <div class="game-card">
            <p class="instruction">Số này là số mấy?</p>
            <div class="super-number">{st.session_state.num}</div>
        </div>
        """, unsafe_allow_html=True)

# --- BƯỚC 3: HỌC ĐẾM (LAYOUT CỘT TRÁI - PHẢI) ---
elif st.session_state.step == 3:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    col_controls, col_display = st.columns([3, 7], gap="large")

    with col_controls:
        st.markdown("### 🎮 Điều khiển")
        
        # Nút Nghe
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 Nghe câu hỏi"):
            play_sound_and_wait(f"Đố bé biết có bao nhiêu bạn {st.session_state.name} ở đây?", 5)
        
        # Nút Đếm
        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #55efc4, #00b894);}}</style>""", unsafe_allow_html=True)
        if st.button("🔢 Đếm cùng cô"):
            play_sound_and_wait(f"Có tất cả {st.session_state.num} bạn {st.session_state.name}", 3)

        # Nút Chơi game
        st.markdown(f"""<style>div.stButton:nth-of-type(3) > button {{background: linear-gradient(to bottom, #fab1a0, #e17055);}}</style>""", unsafe_allow_html=True)
        if st.button("🎮 Chơi trò chơi"):
            play_sound_and_wait("Bây giờ bé hãy tự mình chọn đáp án đúng nhé!", 3)
            st.session_state.step = 4
            st.rerun()

    with col_display:
        st.markdown(f"""
        <div class="game-card">
            <p class="instruction">Có bao nhiêu <b>{st.session_state.name}</b>?</p>
            <div style="margin: 10px 0;">{html_icons}</div>
            <h1 style="font-size: 80px; color:#ff6b81; margin:0;">{st.session_state.num}</h1>
        </div>
        """, unsafe_allow_html=True)

# --- BƯỚC 4: BÀI TẬP ---
elif st.session_state.step == 4:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    col_controls, col_display = st.columns([3, 7], gap="large")
    
    with col_controls:
        st.markdown("### 🎮 Điều khiển")
        
        # Nút Nghe
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 Nghe câu hỏi"):
            play_sound_and_wait("Bé hãy đếm kỹ và chọn số đúng ở bên cạnh nhé!", 5)
            
        # Nút Quay lại
        st.markdown(f"""<style>div.stButton:last-of-type > button {{background: linear-gradient(to bottom, #dfe6e9, #b2bec3); color: #636e72 !important; margin-top: 20px;}}</style>""", unsafe_allow_html=True)
        if st.button("⬅️ Quay lại"):
            st.session_state.step = 2
            st.rerun()

    with col_display:
        st.markdown(f"""
        <div class="game-card">
            <p class="instruction">Hình này ứng với số mấy?</p>
            <div style="margin-bottom: 20px;">{html_icons}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") # Khoảng cách
        # Các nút đáp án nằm dưới hình ảnh cho dễ nhìn
        c1, c2, c3 = st.columns(3)
        for idx, choice in enumerate(st.session_state.choices):
            with [c1, c2, c3][idx]:
                colors = [("#81ecec", "#00cec9"), ("#74b9ff", "#0984e3"), ("#a29bfe", "#6c5ce7")]
                cl, cd = colors[idx]
                st.markdown(f"""<style>div.stButton:nth-of-type({idx + 2}) > button {{background: linear-gradient(to bottom, {cl}, {cd}); font-size: 30px !important; height: 70px;}}</style>""", unsafe_allow_html=True)
                
                if st.button(str(choice), key=f"ans_{idx}"):
                    if choice == st.session_state.num:
                        st.balloons()
                        play_sound_and_wait("Chính xác! Hoan hô bé!", 3)
                        generate_data()
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error("Sai rồi!")
                        play_sound_and_wait("Chưa đúng rồi, bé thử lại nhé!", 2)
