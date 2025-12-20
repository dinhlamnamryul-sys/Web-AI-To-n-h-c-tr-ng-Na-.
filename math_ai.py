import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time
import os

# ================== 1. CẤU HÌNH & KHỞI TẠO ==================
st.set_page_config(
    page_title="Hệ Thống Giáo Dục Mầm Non AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

UPLOAD_FOLDER = "thu_vien_so"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if "step" not in st.session_state: st.session_state.step = 1

# ================== 2. CSS "LONG LANH" (ĐÃ CHỈNH SỬA) ==================
st.markdown("""
<style>
    /* Nền gradient hồng phấn dễ thương */
    .stApp {
        background: linear-gradient(135deg, #fceeff 0%, #f5f7fa 100%);
        background-size: 400% 400%;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }

    /* Card nội dung chính */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 35px;
        padding: 40px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 4px solid #fff;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Sidebar kính mờ */
    [data-testid="stSidebar"] {
        background-color: rgba(255,255,255,0.6);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255,255,255,0.5);
    }

    /* Chữ tiêu đề */
    h1 { color: #ff6b81; text-shadow: 2px 2px 0 #fff; margin: 0; font-size: 3em;}
    .big-text { font-size: 28px; color: #555; margin-bottom: 20px;}

    /* ICON NHÂN VẬT SIÊU TO (Đã chỉnh sửa) */
    .char-icon {
        font-size: 110px; /* Tăng kích thước lên to đùng */
        margin: 10px;
        display: inline-block;
        filter: drop-shadow(0 5px 5px rgba(0,0,0,0.1));
        animation: float 3s ease-in-out infinite;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .char-icon:hover { transform: scale(1.2); }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* NÚT BẤM ĐẸP HƠN */
    div.stButton > button {
        width: 100%;
        height: 70px; /* Nút cao hơn */
        border-radius: 25px;
        font-size: 24px;
        font-weight: bold;
        border: none;
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        transition: all 0.3s;
        color: white;
    }

    /* Màu riêng cho từng loại nút */
    /* Nút thường (Mặc định streamlt) */
    div.stButton > button { background: linear-gradient(45deg, #a18cd1, #fbc2eb); }
    
    /* Hiệu ứng hover chung */
    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ================== 3. HÀM HỖ TRỢ ==================
def play_sound(text, delay=0):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        if delay > 0:
            with st.spinner("Cô đang nói..."):
                time.sleep(delay)
    except:
        pass

def generate_math_question():
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice([
        ("🐰", "Con Thỏ"), ("🍎", "Quả Táo"), ("⭐", "Ngôi Sao"), 
        ("🎈", "Bóng Bay"), ("🍄", "Cây Nấm"), ("🐠", "Con Cá"),
        ("🐣", "Gà Con"), ("🦋", "Bươm Bướm")
    ])
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices: choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices

def get_file_type(filename):
    ext = filename.split('.')[-1].lower()
    if ext in ['png', 'jpg', 'jpeg', 'gif']: return 'image'
    if ext in ['mp4', 'mov', 'avi']: return 'video'
    if ext in ['mp3', 'wav']: return 'audio'
    return 'unknown'

if "num" not in st.session_state: generate_math_question()

# ================== 4. GIAO DIỆN SIDEBAR ==================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3468/3468306.png", width=100)
    st.markdown("## 🌈 MENU")
    menu = st.radio("", ["🐰 Bé Học Toán", "📂 Kho Học Liệu"], index=0)
    st.markdown("---")
    st.info("💡 Bấm 'Đổi câu' để lấy bài mới ngẫu nhiên.")

# ================== 5. CHỨC NĂNG 1: BÉ HỌC TOÁN ==================
if menu == "🐰 Bé Học Toán":
    
    # --- Màn hình 1: Chào mừng ---
    if st.session_state.step == 1:
        st.markdown("""
        <div class="main-card">
            <div style="font-size:100px; animation: bounce 2s infinite;">👋</div>
            <h1>BÉ VUI HỌC TOÁN</h1>
            <p class="big-text">Chào mừng bé đến với lớp học AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("🚀 BẮT ĐẦU NGAY", type="primary"):
                play_sound("Chào mừng bé! Chúng mình cùng học đếm nhé!", delay=3)
                st.session_state.step = 2
                st.rerun()

    # --- Màn hình 2: Học đếm (Đã chỉnh to) ---
    elif st.session_state.step == 2:
        # Tạo chuỗi HTML với class 'char-icon' mới (To hơn)
        img_html = "".join([f'<span class="char-icon">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
        
        st.markdown(f"""
        <div class="main-card">
            <p class="big-text">Bé hãy đếm xem có bao nhiêu <b>{st.session_state.name}</b>?</p>
            <div style="margin: 20px 0;">{img_html}</div>
            <h1 style="font-size:90px; color:#ff4757; text-shadow: 3px 3px 0 #fad390;">{st.session_state.num}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # CHỈNH SỬA: Thêm cột thứ 3 cho nút Đổi câu
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔊 Đọc"): 
                play_sound(f"Có {st.session_state.num} {st.session_state.name}")
        
        with col2:
            # Nút đổi câu hỏi mới (Màu vàng cam)
            if st.button("🔄 Đổi Câu"):
                generate_math_question()
                st.rerun()

        with col3:
            if st.button("➡️ Bài Tập"):
                play_sound("Bé hãy chọn đáp án đúng nhé", delay=2)
                st.session_state.step = 3
                st.rerun()

    # --- Màn hình 3: Trắc nghiệm ---
    elif st.session_state.step == 3:
        img_html = "".join([f'<span class="char-icon">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
        
        st.markdown(f"""
        <div class="main-card">
            <p class="big-text">Đố bé có bao nhiêu {st.session_state.name}?</p>
            <div style="margin: 20px 0;">{img_html}</div>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, choice in enumerate(st.session_state.choices):
            with cols[idx]:
                if st.button(str(choice), key=f"ans_{idx}"):
                    if choice == st.session_state.num:
                        st.balloons()
                        play_sound("Hoan hô! Bé giỏi quá", delay=2)
                        generate_math_question() # Tạo câu mới sau khi đúng
                        st.session_state.step = 2 # Quay lại học bài mới
                        st.rerun()
                    else:
                        st.error("Sai rồi")
                        play_sound("Chưa đúng, bé đếm lại nhé")
        
        # Nút quay lại học (nếu bé muốn đếm lại)
        st.write("")
        if st.button("⬅️ Quay lại đếm"):
            st.session_state.step = 2
            st.rerun()

# ================== 6. CHỨC NĂNG 2: KHO HỌC LIỆU ==================
elif menu == "📂 Kho Học Liệu":
    st.markdown('<div class="main-card"><h1>📂 KHO HỌC LIỆU SỐ</h1></div>', unsafe_allow_html=True)

    with st.expander("⬆️ Tải tài liệu mới", expanded=True):
        uploaded_files = st.file_uploader("Chọn file (Ảnh, Video, Nhạc)", accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
                with open(path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            st.success("Đã lưu thành công!")
            time.sleep(1)
            st.rerun()

    st.markdown("---")
    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        st.info("Chưa có file nào.")
    else:
        cols = st.columns(2)
        for i, filename in enumerate(files):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file_type = get_file_type(filename)
            with cols[i % 2]:
                with st.container():
                    st.markdown(f'<div style="background:white; padding:10px; border-radius:15px; margin-bottom:10px; border:1px solid #ddd"><b>{filename}</b></div>', unsafe_allow_html=True)
                    if file_type == 'image': st.image(file_path, use_container_width=True)
                    elif file_type == 'video': st.video(file_path)
                    elif file_type == 'audio': st.audio(file_path)
                    
                    if st.button("🗑️ Xóa", key=f"del_{filename}"):
                        os.remove(file_path)
                        st.rerun()
