import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time
import os # Thư viện để làm việc với file hệ thống

# ================== 1. CẤU HÌNH & KHỞI TẠO THƯ MỤC LƯU TRỮ ==================
st.set_page_config(
    page_title="Hệ Thống Giáo Dục Mầm Non AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tên thư mục để lưu file (sẽ tự tạo nếu chưa có)
UPLOAD_FOLDER = "thu_vien_so"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Khởi tạo Session State
if "step" not in st.session_state: st.session_state.step = 1

# ================== 2. CSS GIAO DIỆN (GIỮ NGUYÊN ĐỘ ĐẸP) ==================
st.markdown("""
<style>
    /* Nền màu gradient động */
    .stApp {
        background: linear-gradient(-45deg, #a18cd1, #fbc2eb, #fad0c4, #ff9a9e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Card nổi */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 2px solid rgba(255, 255, 255, 0.18);
        text-align: center;
        margin-bottom: 20px;
    }

    /* Sidebar trong suốt */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
    }

    h1 { color: #ff6b6b; text-shadow: 1px 1px 0 #fff; margin: 0;}
    
    /* Nút bấm đẹp */
    div.stButton > button {
        width: 100%;
        height: 55px;
        border-radius: 15px;
        font-size: 20px;
        font-weight: bold;
        background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
        color: #2c3e50;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ================== 3. HÀM HỖ TRỢ HỆ THỐNG ==================
def play_sound(text, delay=0):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        if delay > 0:
            with st.spinner("Cô giáo đang nói..."):
                time.sleep(delay)
    except:
        pass

def save_uploaded_file(uploaded_file):
    """Lưu file từ giao diện vào ổ cứng"""
    try:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except:
        return False

def get_file_type(filename):
    """Xác định loại file dựa trên đuôi"""
    ext = filename.split('.')[-1].lower()
    if ext in ['png', 'jpg', 'jpeg', 'gif']: return 'image'
    if ext in ['mp4', 'mov', 'avi']: return 'video'
    if ext in ['mp3', 'wav']: return 'audio'
    return 'unknown'

# Logic tạo câu hỏi toán
def generate_math_question():
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice([
        ("🐰", "Con Thỏ"), ("🍎", "Quả Táo"), ("⭐", "Ngôi Sao"), 
        ("🎈", "Bóng Bay"), ("🍄", "Cây Nấm"), ("🐠", "Con Cá")
    ])
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices: choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices

if "num" not in st.session_state: generate_math_question()

# ================== 4. GIAO DIỆN CHÍNH ==================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3069/3069172.png", width=80)
    st.title("MENU")
    menu = st.radio("", ["🐰 Bé Học Toán", "📂 Kho Học Liệu (Đám Mây)"])
    st.info("💡 File tải lên sẽ được lưu vĩnh viễn trong thư mục 'thu_vien_so'")

# --- CHỨC NĂNG 1: BÉ HỌC TOÁN ---
if menu == "🐰 Bé Học Toán":
    if st.session_state.step == 1:
        st.markdown('<div class="main-card"><h1>👋 BÉ VUI HỌC TOÁN</h1><p>Chào mừng bé đến lớp học AI</p></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("🚀 BẮT ĐẦU"):
                play_sound("Chào mừng bé! Chúng mình cùng học nào", delay=3)
                st.session_state.step = 2
                st.rerun()
    
    elif st.session_state.step == 2:
        img_html = "".join([f'<span style="font-size:50px; margin:5px;">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
        st.markdown(f'<div class="main-card"><p>Bé hãy đếm: <b>{st.session_state.name}</b></p><div>{img_html}</div><h1 style="font-size:60px; color:red">{st.session_state.num}</h1></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔊 Đọc"): play_sound(f"Có {st.session_state.num} {st.session_state.name}")
        with c2:
            if st.button("➡️ Bài Tập"):
                play_sound("Bé hãy chọn đáp án đúng nhé", delay=2)
                st.session_state.step = 3
                st.rerun()

    elif st.session_state.step == 3:
        img_html = "".join([f'<span style="font-size:50px; margin:5px;">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
        st.markdown(f'<div class="main-card"><p>Có bao nhiêu {st.session_state.name}?</p><div>{img_html}</div></div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, choice in enumerate(st.session_state.choices):
            with cols[idx]:
                if st.button(str(choice), key=f"ans_{idx}"):
                    if choice == st.session_state.num:
                        st.balloons()
                        play_sound("Đúng rồi! Bé giỏi quá", delay=2)
                        generate_math_question()
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error("Sai rồi")
                        play_sound("Sai rồi bé ơi")

# --- CHỨC NĂNG 2: KHO HỌC LIỆU (LƯU Ổ CỨNG) ---
elif menu == "📂 Kho Học Liệu (Đám Mây)":
    st.markdown('<div class="main-card"><h1>📂 KHO HỌC LIỆU SỐ</h1><p>Dữ liệu được lưu trữ an toàn trên máy chủ</p></div>', unsafe_allow_html=True)

    # 1. Phần upload
    with st.expander("⬆️ Tải tài liệu mới (Bấm vào đây)", expanded=True):
        uploaded_files = st.file_uploader("Chọn file (Ảnh, Video, Nhạc)", accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if save_uploaded_file(uploaded_file):
                    st.success(f"Đã lưu: {uploaded_file.name}")
            time.sleep(1) # Đợi xíu cho file lưu xong
            st.rerun() # Load lại trang để hiện file mới

    st.markdown("---")
    
    # 2. Phần hiển thị (Quét file từ ổ cứng)
    st.subheader("📚 Tài liệu hiện có:")
    
    # Lấy danh sách file trong thư mục
    files = os.listdir(UPLOAD_FOLDER)
    
    if len(files) == 0:
        st.info("Chưa có file nào trong thư mục 'thu_vien_so'.")
    else:
        # Hiển thị dạng lưới
        cols = st.columns(2)
        for i, filename in enumerate(files):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file_type = get_file_type(filename)
            
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"""
                    <div style="background:white; padding:15px; border-radius:15px; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:20px; border:1px solid #eee;">
                        <h4 style="color:#2980b9; margin:0">📄 {filename}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Hiển thị nội dung dựa trên loại file
                    if file_type == 'image':
                        st.image(file_path, use_container_width=True)
                    elif file_type == 'video':
                        st.video(file_path)
                    elif file_type == 'audio':
                        st.audio(file_path)
                    else:
                        st.warning("Định dạng không hỗ trợ xem trước")
                    
                    # Nút xóa file
                    if st.button("🗑️ Xóa file", key=f"del_{filename}"):
                        os.remove(file_path)
                        st.rerun()

# Footer
st.markdown("<br><hr><center style='color:#999'>© 2025 AI Education System</center>", unsafe_allow_html=True)
