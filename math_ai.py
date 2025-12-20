import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time
from PIL import Image

# ================== 1. CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Hệ Thống Giáo Dục Mầm Non AI",
    page_icon="🎓",
    layout="wide", # Dùng màn hình rộng để hiển thị kho học liệu đẹp hơn
    initial_sidebar_state="expanded"
)

# Khởi tạo Session State
if "step" not in st.session_state: st.session_state.step = 1
if "uploaded_files" not in st.session_state: st.session_state.uploaded_files = []

# ================== 2. SIÊU CSS (GIAO DIỆN LONG LANH) ==================
st.markdown("""
<style>
    /* Nền cầu vồng chuyển động */
    .stApp {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #a18cd1, #fbc2eb);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Card (Khung nội dung) */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        border: 4px solid #fff;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Sidebar (Thanh bên) đẹp hơn */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.8);
        border-right: 2px solid #fff;
    }

    /* Tiêu đề & Chữ */
    h1 { color: #ff6f61; text-shadow: 2px 2px 0 #fff; margin:0;}
    h2 { color: #6a11cb; }
    .big-text { font-size: 24px; color: #555; }
    
    /* Animation cho icon */
    .bounce { animation: bounce 2s infinite; display: inline-block; font-size: 80px;}
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
        40% {transform: translateY(-20px);}
        60% {transform: translateY(-10px);}
    }

    /* Nút bấm (Button) */
    div.stButton > button {
        width: 100%;
        height: 60px;
        border-radius: 20px;
        font-size: 22px;
        font-weight: bold;
        background: linear-gradient(45deg, #85FFBD 0%, #FFFB7D 100%);
        color: #444;
        border: 2px solid #fff;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.03);
        background: linear-gradient(45deg, #FFFB7D 0%, #85FFBD 100%);
    }

    /* Vùng tải file (Uploader) */
    [data-testid="stFileUploader"] {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 20px;
        border: 2px dashed #888;
    }
</style>
""", unsafe_allow_html=True)

# ================== 3. HÀM HỖ TRỢ ==================
def play_sound(text, delay=0):
    """Phát âm thanh và đợi (nếu cần)"""
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', autoplay=True)
        if delay > 0:
            with st.spinner("Đang nói..."):
                time.sleep(delay)
    except:
        pass

def generate_math_question():
    st.session_state.num = random.randint(1, 10)
    st.session_state.icon, st.session_state.name = random.choice([
        ("🐰", "Con Thỏ"), ("🍎", "Quả Táo"), ("⭐", "Ngôi Sao"), 
        ("🎈", "Bóng Bay"), ("🍄", "Cây Nấm"), ("🐠", "Con Cá")
    ])
    # Tạo đáp án
    choices = [st.session_state.num]
    while len(choices) < 3:
        fake = random.randint(1, 10)
        if fake not in choices: choices.append(fake)
    random.shuffle(choices)
    st.session_state.choices = choices

if "num" not in st.session_state: generate_math_question()

# ================== 4. THANH ĐIỀU HƯỚNG (SIDEBAR) ==================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=100)
    st.markdown("## 🎈 MENU CHÍNH")
    
    menu = st.radio(
        "",
        ["🐰 Bé Học Toán", "📂 Kho Học Liệu (Tải File)"],
        index=0
    )
    
    st.markdown("---")
    st.info("💡 Mẹo: Giáo viên có thể tải video bài giảng lên 'Kho Học Liệu' để trình chiếu.")

# ================== 5. CHỨC NĂNG 1: BÉ HỌC TOÁN ==================
if menu == "🐰 Bé Học Toán":
    
    # --- Màn hình chào ---
    if st.session_state.step == 1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="bounce">🐰</div>', unsafe_allow_html=True)
        st.markdown('<h1>BÉ VUI HỌC TOÁN</h1>', unsafe_allow_html=True)
        st.markdown('<p class="big-text">Chào mừng bé đến với khu vườn thần tiên!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("🚀 BẮT ĐẦU NGAY"):
                play_sound("Chào mừng bé! Chúng mình cùng đi học đếm nhé!", delay=4)
                st.session_state.step = 2
                st.rerun()

    # --- Màn hình học ---
    elif st.session_state.step == 2:
        img_html = "".join([f'<span style="font-size:60px; margin:5px; display:inline-block; animation:bounce 2s infinite">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
        
        st.markdown(f"""
        <div class="main-card">
            <p class="big-text">Bé hãy đếm xem có bao nhiêu <b>{st.session_state.name}</b>?</p>
            <div>{img_html}</div>
            <h1 style="font-size:80px; color:#ff6b6b">{st.session_state.num}</h1>
            <p>({st.session_state.num} - {["Không","Một","Hai","Ba","Bốn","Năm","Sáu","Bảy","Tám","Chín","Mười"][st.session_state.num]})</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔊 Nghe Đọc"):
                play_sound(f"Có tất cả {st.session_state.num} {st.session_state.name}")
        with col2:
            if st.button("➡️ Bài Tập"):
                play_sound("Bây giờ bé hãy chọn đáp án đúng nhé!", delay=3)
                st.session_state.step = 3
                st.rerun()

    # --- Màn hình kiểm tra ---
    elif st.session_state.step == 3:
        img_html = "".join([f'<span style="font-size:60px; margin:5px;">{st.session_state.icon}</span>' for _ in range(st.session_state.num)])
        
        st.markdown(f"""
        <div class="main-card">
            <p class="big-text">Đố bé có bao nhiêu {st.session_state.name}?</p>
            <div>{img_html}</div>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, choice in enumerate(st.session_state.choices):
            with cols[idx]:
                if st.button(str(choice), key=f"ans_{idx}"):
                    if choice == st.session_state.num:
                        st.balloons()
                        play_sound("Hoan hô! Bé giỏi quá!", delay=2)
                        generate_math_question()
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error("Sai rồi!")
                        play_sound("Chưa đúng, bé đếm lại nhé")

# ================== 6. CHỨC NĂNG 2: KHO HỌC LIỆU ==================
elif menu == "📂 Kho Học Liệu (Tải File)":
    
    st.markdown('<div class="main-card"><h1>📂 KHO HỌC LIỆU SỐ</h1><p>Nơi lưu trữ Video, Hình ảnh, Bài hát cho bé</p></div>', unsafe_allow_html=True)
    
    # --- Khu vực tải file ---
    with st.expander("⬆️ Tải tài liệu mới lên (Bấm vào đây)", expanded=True):
        uploaded_file = st.file_uploader("Chọn file ảnh, video hoặc âm thanh", type=['png', 'jpg', 'mp4', 'mp3', 'wav'])
        
        if uploaded_file is not None:
            # Lưu file vào session state để hiển thị (giả lập lưu trữ)
            file_details = {"name": uploaded_file.name, "type": uploaded_file.type, "data": uploaded_file}
            
            # Kiểm tra xem file đã có chưa để tránh trùng
            if not any(d['name'] == uploaded_file.name for d in st.session_state.uploaded_files):
                st.session_state.uploaded_files.append(file_details)
                st.success(f"Đã tải lên thành công: {uploaded_file.name}")
            else:
                st.info("File này đã có trong danh sách.")

    st.markdown("---")
    st.subheader("📚 Danh Sách Tài Liệu Đã Tải")

    if len(st.session_state.uploaded_files) == 0:
        st.warning("Chưa có tài liệu nào. Hãy tải file lên nhé!")
    else:
        # Hiển thị dạng lưới (Grid)
        cols = st.columns(2) # Chia làm 2 cột
        
        for idx, file in enumerate(st.session_state.uploaded_files):
            with cols[idx % 2]: # Xếp so le
                st.markdown(f"""
                <div style="background:white; padding:15px; border-radius:15px; box-shadow:0 5px 10px rgba(0,0,0,0.1); margin-bottom:20px;">
                    <h3 style="color:#007bff">📄 {file['name']}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Xử lý hiển thị theo loại file
                if "image" in file['type']:
                    st.image(file['data'], use_container_width=True)
                elif "video" in file['type']:
                    st.video(file['data'])
                elif "audio" in file['type']:
                    st.audio(file['data'])
                
                if st.button("🗑️ Xóa", key=f"del_{idx}"):
                    st.session_state.uploaded_files.pop(idx)
                    st.rerun()

# Footer
st.markdown("<br><hr><center style='color:#888'>© 2025 Ứng dụng Giáo dục Mầm non AI</center>", unsafe_allow_html=True)
