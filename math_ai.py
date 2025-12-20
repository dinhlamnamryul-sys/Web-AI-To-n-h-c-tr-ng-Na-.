import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time
import speech_recognition as sr  # <--- THƯ VIỆN AI MỚI: Đôi tai của máy tính

# ================== 1. CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Bé Vui Học Toán AI",
    page_icon="🐰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khởi tạo Session
if "step" not in st.session_state: st.session_state.step = 1
if "num" not in st.session_state: st.session_state.num = 0
if "unit" not in st.session_state: st.session_state.unit = "" 

# ================== 2. CSS & ANIMATION ==================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); font-family: 'Comic Sans MS', sans-serif; }
    .game-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 40px; padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); 
        text-align: center; border: 6px solid #fff;
        min-height: 350px; display: flex; flex-direction: column;
        justify-content: center; align-items: center;
    }
    .super-number { font-size: 160px; font-weight: 900; color: #ff6b6b; text-shadow: 4px 4px 0px #fff; margin: 0; }
    
    /* BUTTON STYLE */
    div.stButton > button {
        width: 100%; height: 70px; font-size: 20px !important; font-weight: 800 !important;
        color: white !important; border: 3px solid white !important; border-radius: 30px !important;
        box-shadow: 0 5px 0 rgba(0,0,0,0.15); transition: all 0.2s;
    }
    div.stButton > button:active { top: 4px; box-shadow: none; }
    
    .char-item { font-size: 80px; display: inline-block; margin: 10px; filter: drop-shadow(0 5px 2px rgba(0,0,0,0.1)); }
    .instruction { font-size: 24px; color: #57606f; font-weight: bold; margin-bottom: 20px; }
    
    /* Hiệu ứng mic thu âm */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 82, 82, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(255, 82, 82, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 82, 82, 0); }
    }
    .mic-listening { animation: pulse 1.5s infinite; border-color: #ff5252 !important; color: #ff5252 !important; }

    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 2rem; max-width: 1000px; }
</style>
""", unsafe_allow_html=True)

# ================== 3. HÀM XỬ LÝ LOGIC & AI ==================

# AI 1: Text-to-Speech (Nói)
def play_sound_and_wait(text, wait_seconds):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        with st.spinner(f"🔊 Cô đang nói..."):
            time.sleep(wait_seconds)
    except Exception:
        time.sleep(wait_seconds)

# AI 2: Speech-to-Text (Nghe) - NEW FEATURE
def listen_to_answer():
    r = sr.Recognizer()
    mic = sr.Microphone()
    
    status_placeholder = st.empty()
    status_placeholder.info("🎤 Đang lắng nghe bé nói... (Bé hãy nói to nhé!)")
    
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5) # Lọc tiếng ồn
            audio = r.listen(source, timeout=5, phrase_time_limit=3) # Nghe trong tối đa 5s
        
        status_placeholder.success("⏳ Đang suy nghĩ...")
        # Gửi âm thanh lên Google để dịch sang chữ
        text = r.recognize_google(audio, language="vi-VN")
        return text.lower() # Trả về chữ thường (ví dụ: "số năm", "năm")
    except sr.WaitTimeoutError:
        status_placeholder.warning("Cô không nghe thấy gì cả.")
        return None
    except sr.UnknownValueError:
        status_placeholder.warning("Cô chưa nghe rõ, bé nói lại nhé!")
        return None
    except Exception as e:
        status_placeholder.error(f"Lỗi mic: {e}")
        return None

# Hàm chuyển đổi chữ số tiếng Việt sang số (Xử lý ngôn ngữ tự nhiên cơ bản)
def map_text_to_number(text):
    if not text: return -1
    mapping = {
        "một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5, "lăm": 5,
        "sáu": 6, "bảy": 7, "tám": 8, "chín": 9, "mười": 10,
        "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10
    }
    # Kiểm tra xem trong câu nói của bé có từ khóa số nào không
    for word, number in mapping.items():
        if word in text:
            return number
    return -1

def generate_data():
    st.session_state.num = random.randint(1, 10)
    data_source = [("🐰", "Thỏ", "con"), ("🍎", "Táo", "quả"), ("⭐", "Sao", "ngôi"), 
                   ("🎈", "Bóng", "quả"), ("🍄", "Nấm", "cây"), ("🐠", "Cá", "con"),
                   ("🚗", "Xe", "chiếc"), ("🦋", "Bướm", "con")]
    selected = random.choice(data_source)
    st.session_state.icon, st.session_state.name, st.session_state.unit = selected
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices: choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices
    if "user_answer_text" in st.session_state: del st.session_state.user_answer_text

if st.session_state.num == 0: generate_data()

# ================== 4. GIAO DIỆN CHÍNH ==================

# --- BƯỚC 1: TRANG CHỦ ---
if st.session_state.step == 1:
    st.markdown("""
    <div class="game-card" style="padding: 50px;">
        <div style="font-size:100px; margin-bottom:10px;">🎡</div>
        <h1 style="color:#ff4757; font-size:50px;">BÉ VUI HỌC TOÁN AI</h1>
        <p class="instruction">Học mà chơi - Nói chuyện cùng máy tính</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.markdown("""<style>div.stButton > button {background: linear-gradient(to bottom, #ff6b6b, #ee5253); height: 80px; font-size: 24px !important;}</style>""", unsafe_allow_html=True)
        if st.button("🚀 BẮT ĐẦU NGAY"):
            play_sound_and_wait("Chào mừng bé! Hôm nay chúng mình cùng học số đếm nhé!", 3)
            st.session_state.step = 2
            st.rerun()

# --- BƯỚC 2: HỌC SỐ ---
elif st.session_state.step == 2:
    col_controls, col_display = st.columns([3, 7], gap="large")
    with col_controls:
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 Nghe cô đọc"): play_sound_and_wait(f"Đây là số {st.session_state.num}", 2)
        
        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #ffeaa7, #fdcb6e); color: #d35400 !important;}}</style>""", unsafe_allow_html=True)
        if st.button("🔄 Đổi số khác"):
            generate_data()
            st.rerun()
            
        st.markdown(f"""<style>div.stButton:nth-of-type(3) > button {{background: linear-gradient(to bottom, #fd79a8, #e84393);}}</style>""", unsafe_allow_html=True)
        if st.button("➡️ Sang bài đếm"):
            st.session_state.step = 3
            st.rerun()
    with col_display:
        st.markdown(f"""<div class="game-card"><p class="instruction">Số mấy đây?</p><div class="super-number">{st.session_state.num}</div></div>""", unsafe_allow_html=True)

# --- BƯỚC 3: HỌC ĐẾM ---
elif st.session_state.step == 3:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    col_controls, col_display = st.columns([3, 7], gap="large")
    with col_controls:
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #a29bfe, #6c5ce7);}}</style>""", unsafe_allow_html=True)
        if st.button("🔊 Nghe câu hỏi"): play_sound_and_wait(f"Đố bé biết có bao nhiêu {st.session_state.unit} {st.session_state.name} ở đây?", 4)
        
        st.markdown(f"""<style>div.stButton:nth-of-type(2) > button {{background: linear-gradient(to bottom, #fab1a0, #e17055);}}</style>""", unsafe_allow_html=True)
        if st.button("🎮 Vào bài tập (Có AI)"):
            play_sound_and_wait("Bây giờ bé hãy dùng giọng nói để trả lời nhé!", 3)
            st.session_state.step = 4
            st.rerun()
    with col_display:
        st.markdown(f"""<div class="game-card"><p class="instruction">Có bao nhiêu <b>{st.session_state.name}</b>?</p><div style="margin: 20px 0;">{html_icons}</div></div>""", unsafe_allow_html=True)

# --- BƯỚC 4: BÀI TẬP VỚI AI GIỌNG NÓI ---
elif st.session_state.step == 4:
    html_icons = "".join([f'<span class="char-item">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    col_controls, col_display = st.columns([3, 7], gap="large")
    
    with col_controls:
        st.markdown("### 🎙️ Trả lời bằng giọng nói")
        
        # Nút Micro lớn
        st.markdown(f"""<style>div.stButton:nth-of-type(1) > button {{background: linear-gradient(to bottom, #ff5252, #b33939); font-size: 28px !important; height: 100px; border-radius: 50px !important;}}</style>""", unsafe_allow_html=True)
        
        # LOGIC AI NGHE VÀ XỬ LÝ
        if st.button("🎤 BẤM ĐỂ NÓI"):
            user_text = listen_to_answer() # Gọi hàm nghe
            
            if user_text:
                st.session_state.user_answer_text = user_text # Lưu lại câu bé nói
                detected_num = map_text_to_number(user_text) # AI phân tích số
                
                if detected_num == st.session_state.num:
                    st.balloons()
                    play_sound_and_wait(f"Đúng rồi! Bé giỏi quá! Bé nói là {user_text}", 4)
                    generate_data()
                    st.rerun()
                elif detected_num == -1:
                     play_sound_and_wait(f"Cô nghe thấy bé nói là {user_text}, nhưng cô không hiểu đó là số mấy.", 4)
                else:
                    st.error(f"Sai rồi! Bé nói là số {detected_num}")
                    play_sound_and_wait(f"Sai rồi. Bé nói là {user_text}, nhưng đáp án là {st.session_state.num} cơ.", 4)
        
        # Hiển thị những gì AI nghe được
        if "user_answer_text" in st.session_state:
            st.info(f"👂 Máy tính nghe thấy: '{st.session_state.user_answer_text}'")

        st.markdown(f"""<style>div.stButton:last-of-type > button {{background: linear-gradient(to bottom, #dfe6e9, #b2bec3); color: #636e72 !important; margin-top: 20px;}}</style>""", unsafe_allow_html=True)
        if st.button("⬅️ Quay lại"):
            st.session_state.step = 2
            st.rerun()

    with col_display:
        st.markdown(f"""
        <div class="game-card">
            <p class="instruction">Hãy bấm nút Micro và nói to đáp án!</p>
            <div style="margin-bottom: 20px;">{html_icons}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Vẫn giữ nút bấm cho trường hợp mic hỏng
        st.write("Hoặc bấm chọn số:")
        c1, c2, c3 = st.columns(3)
        for idx, choice in enumerate(st.session_state.choices):
            with [c1, c2, c3][idx]:
                if st.button(str(choice), key=f"ans_{idx}"):
                    if choice == st.session_state.num:
                        st.balloons()
                        play_sound_and_wait("Chính xác!", 2)
                        generate_data()
                        st.rerun()
                    else:
                        st.error("Sai rồi!")
