import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time

# ================== 1. CẤU HÌNH TRANG & TRẠNG THÁI ==================
st.set_page_config(page_title="Bé Vui Học Toán", page_icon="🐰", layout="centered")

if "step" not in st.session_state:
    st.session_state.step = 1
if "score" not in st.session_state:
    st.session_state.score = 0

# ================== 2. BỘ CSS "LONG LANH" (MAGIC UI) ==================
# Phần này tạo hiệu ứng nền, nút bấm đẹp và hoạt hình
st.markdown("""
<style>
    /* Nền chuyển màu nhẹ nhàng (Pastel Gradient) */
    .stApp {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fad0c4, #a18cd1);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Hiệu ứng thẻ bài (Card) nổi bật */
    .card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        text-align: center;
        border: 4px solid #fff;
        margin-bottom: 20px;
    }

    /* Hiệu ứng chữ và icon */
    .big-emoji { font-size: 100px; animation: bounce 2s infinite; }
    .medium-emoji { font-size: 60px; margin: 5px; display:inline-block; transition: transform 0.2s; }
    .medium-emoji:hover { transform: scale(1.2); }
    
    h1 { color: #ff6b6b; text-shadow: 2px 2px 0px #fff; }
    .question-text { font-size: 28px; color: #555; font-weight: bold; }
    .highlight { color: #e056fd; font-size: 35px; }

    /* Animation nhún nhảy */
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
        40% {transform: translateY(-20px);}
        60% {transform: translateY(-10px);}
    }

    /* Tùy chỉnh nút bấm Streamlit cho đẹp */
    div.stButton > button {
        width: 100%;
        height: 70px;
        border-radius: 20px;
        font-size: 28px;
        font-weight: bold;
        background: linear-gradient(to bottom, #89f7fe, #66a6ff);
        border: none;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        background: linear-gradient(to bottom, #66a6ff, #89f7fe);
    }
    
    /* Ẩn menu mặc định của Streamlit cho gọn */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== 3. DỮ LIỆU & HÀM HỖ TRỢ ==================

data_objects = {
    "🐰": "Chú Thỏ", "🍎": "Quả Táo", "⭐": "Ngôi Sao", 
    "🎈": "Bóng Bay", "🚗": "Ô Tô", "🐯": "Chú Hổ", 
    "🍄": "Cây Nấm", "🌻": "Bông Hoa"
}

text_numbers = {
    1: "Một", 2: "Hai", 3: "Ba", 4: "Bốn", 5: "Năm",
    6: "Sáu", 7: "Bảy", 8: "Tám", 9: "Chín", 10: "Mười"
}

def play_sound(text):
    """Phát âm thanh mượt mà qua bộ nhớ đệm"""
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
    except:
        pass # Bỏ qua nếu lỗi mạng

def generate_question():
    """Tạo câu hỏi ngẫu nhiên mới"""
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice(list(data_objects.items()))
    
    # Tạo đáp án trắc nghiệm (1 đúng, 2 sai)
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices:
            choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices

# Khởi tạo câu hỏi lần đầu
if "num" not in st.session_state:
    generate_question()

# ================== 4. GIAO DIỆN CHÍNH (LOGIC CŨ - GIAO DIỆN MỚI) ==================

# --- BƯỚC 1: MÀN HÌNH CHÀO ---
if st.session_state.step == 1:
    st.markdown("""
        <div class="card">
            <div class="big-emoji">👋</div>
            <h1>BÉ VUI HỌC TOÁN</h1>
            <p class="question-text">Chào mừng bé đến với lớp học của Thỏ Con!</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 BẮT ĐẦU HỌC NÀO"):
        st.session_state.step = 2
        play_sound("Xin chào các bạn nhỏ. Hôm nay chúng mình cùng đếm số nhé!")
        st.rerun()

# --- BƯỚC 2: HỌC ĐẾM (HIỆN SỐ VÀ HÌNH) ---
elif st.session_state.step == 2:
    # Hiển thị hình ảnh
    img_html = "".join([f'<span class="medium-emoji">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
        <div class="card">
            <p class="question-text">Bé hãy đếm cùng Thỏ nhé!</p>
            <div style="margin: 20px 0;">{img_html}</div>
            <hr>
            <p class="question-text">Có tất cả <span class="highlight">{st.session_state.num}</span> {st.session_state.name}</p>
            <p style="color:gray; font-size:20px">({text_numbers[st.session_state.num]})</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔊 Đọc lại"):
            play_sound(f"Có {text_numbers[st.session_state.num]} {st.session_state.name}")
    with c2:
        if st.button("➡️ Luyện tập"):
            st.session_state.step = 3
            play_sound(f"Bây giờ đố bé biết có bao nhiêu {st.session_state.name}?")
            st.rerun()

# --- BƯỚC 3: LUYỆN TẬP (TRẮC NGHIỆM THAY VÌ NHẬP SỐ) ---
elif st.session_state.step == 3:
    # Hiển thị hình ảnh (không hiện số)
    img_html = "".join([f'<span class="medium-emoji" style="animation: bounce 3s infinite;">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
    
    st.markdown(f"""
        <div class="card">
            <p class="question-text">Đố bé có bao nhiêu {st.session_state.name}?</p>
            <div style="margin: 20px 0;">{img_html}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 3 Nút bấm to thay vì ô nhập liệu nhỏ xíu
    cols = st.columns(3)
    for idx, choice in enumerate(st.session_state.choices):
        with cols[idx]:
            if st.button(f"{choice}", key=f"btn_{idx}"):
                if choice == st.session_state.num:
                    st.balloons() # Hiệu ứng bóng bay
                    play_sound("Hoan hô! Bé trả lời đúng rồi!")
                    time.sleep(1.5)
                    generate_question() # Tạo câu mới
                    st.session_state.step = 2 # Quay lại vòng lặp học -> thi
                    st.rerun()
                else:
                    st.error("Chưa đúng rồi! Bé đếm lại kỹ nhé!")
                    play_sound("Sai rồi. Con thử lại đi!")

# ================== FOOTER ==================
st.markdown("<div style='text-align:center; color:#fff; padding:20px;'>© 2025 AI Math for Kids</div>", unsafe_allow_html=True)
