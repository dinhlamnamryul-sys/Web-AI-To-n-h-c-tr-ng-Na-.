import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Bé Vui Học Toán Cùng Thỏ Con",
    page_icon="🐰",
    layout="wide"
)

# ================== CSS CHUYỂN ĐỘNG & GIAO DIỆN (MAGIC CSS) ==================
st.markdown("""
<style>
/* 1. NỀN HOẠT HÌNH */
.stApp {
    background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
    background-attachment: fixed;
    font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
}

/* 2. HIỆU ỨNG CHUYỂN ĐỘNG (ANIMATIONS) */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
    40% {transform: translateY(-30px);}
    60% {transform: translateY(-15px);}
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

@keyframes wiggle {
    0% { transform: rotate(0deg); }
    25% { transform: rotate(5deg); }
    50% { transform: rotate(0deg); }
    75% { transform: rotate(-5deg); }
    100% { transform: rotate(0deg); }
}

/* 3. THIẾT KẾ CÁC KHỐI (CARDS) */
.main-card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 30px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border: 5px solid #FF9A9E;
    text-align: center;
    margin-bottom: 20px;
}

/* 4. NHÂN VẬT & CHỮ */
.character {
    font-size: 150px;
    display: inline-block;
    animation: float 3s ease-in-out infinite; /* Nhân vật bay bay */
    cursor: pointer;
}

.object-item {
    font-size: 80px;
    display: inline-block;
    margin: 10px;
    animation: bounce 2s infinite; /* Đồ vật nhún nhảy */
}

.big-title {
    font-size: 40px;
    color: #FF6B6B;
    text-shadow: 2px 2px #fff;
    font-weight: bold;
    animation: pulse 2s infinite;
}

.instruction {
    font-size: 28px;
    color: #4A4A4A;
    margin: 15px 0;
}

/* 5. NÚT BẤM (BUTTONS) */
div.stButton > button {
    width: 100%;
    height: 80px;
    font-size: 30px !important;
    font-weight: bold !important;
    border-radius: 25px !important;
    background: linear-gradient(to right, #56CCF2, #2F80ED) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    transition: transform 0.2s !important;
}

div.stButton > button:hover {
    transform: scale(1.05) !important;
    background: linear-gradient(to right, #2F80ED, #56CCF2) !important;
}

/* Nút sai màu đỏ */
.wrong-btn > button {
    background: linear-gradient(to right, #ff9966, #ff5e62) !important;
}
</style>
""", unsafe_allow_html=True)

# ================== LOGIC CHƯƠNG TRÌNH ==================

# Dữ liệu hình ảnh (Icon to đẹp)
do_vat = {
    "🍎": "quả táo",
    "🍄": "cây nấm",
    "🐠": "chú cá",
    "🦋": "bươm bướm",
    "🍕": "bánh pizza",
    "⭐": "ngôi sao",
    "🎈": "bóng bay",
    "🐣": "gà con"
}

chu_so = {
    1: "Một", 2: "Hai", 3: "Ba", 4: "Bốn", 5: "Năm",
    6: "Sáu", 7: "Bảy", 8: "Tám", 9: "Chín", 10: "Mười"
}

def phat_am_thanh(text):
    try:
        sound_file = BytesIO()
        tts = gTTS(text=text, lang="vi")
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format="audio/mp3", autoplay=True)
    except:
        pass

def tao_cau_hoi_moi():
    st.session_state.so = random.randint(1, 10)
    st.session_state.hinh, st.session_state.ten = random.choice(list(do_vat.items()))
    
    # Tạo đáp án
    dap_an_dung = st.session_state.so
    lua_chon = [dap_an_dung]
    while len(lua_chon) < 3:
        r = random.randint(1, 10)
        if r not in lua_chon: lua_chon.append(r)
    random.shuffle(lua_chon)
    st.session_state.lua_chon_buoc3 = lua_chon
    
    # Đáp án bước 4
    dap_an_sau = st.session_state.so + 1
    lua_chon_4 = [dap_an_sau]
    while len(lua_chon_4) < 3:
        r = random.randint(1, 11)
        if r not in lua_chon_4: lua_chon_4.append(r)
    random.shuffle(lua_chon_4)
    st.session_state.lua_chon_buoc4 = lua_chon_4

if "buoc" not in st.session_state:
    st.session_state.buoc = 1
    tao_cau_hoi_moi()

# ================== GIAO DIỆN CHÍNH ==================

# Căn giữa nội dung bằng cột
c1, c2, c3 = st.columns([1, 2, 1])

with c2: # Chỉ hiển thị ở cột giữa cho giống điện thoại/iPad
    
    # --- BƯỚC 1: MÀN HÌNH CHÀO ---
    if st.session_state.buoc == 1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="character">🐰</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-title">BÉ VUI HỌC TOÁN</div>', unsafe_allow_html=True)
        st.markdown('<p class="instruction">Chào mừng bé đến với khu vườn của Thỏ Con!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 BẮT ĐẦU CHƠI NGAY"):
            st.session_state.buoc = 2
            phat_am_thanh("Chào mừng bé! Chúng mình cùng đi đếm số nhé!")
            st.rerun()

    # --- BƯỚC 2: HỌC ĐẾM (HIỆU ỨNG NHÚN NHẢY) ---
    elif st.session_state.buoc == 2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="instruction">Có bao nhiêu <b>{st.session_state.ten}</b> thế nhỉ?</div>', unsafe_allow_html=True)
        
        # Hiển thị đồ vật nhún nhảy
        html_hinh = ""
        for _ in range(st.session_state.so):
            html_hinh += f'<span class="object-item">{st.session_state.hinh}</span>'
        st.markdown(f'<div>{html_hinh}</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="big-title" style="font-size:60px; margin-top:20px">{st.session_state.so}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔊 Nghe"):
                phat_am_thanh(f"Có {chu_so[st.session_state.so]} {st.session_state.ten}")
        with col_btn2:
            if st.button("➡️ Tiếp theo"):
                st.session_state.buoc = 3
                st.rerun()

    # --- BƯỚC 3: TRẮC NGHIỆM (CHỌN SỐ) ---
    elif st.session_state.buoc == 3:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="instruction">Bé hãy chọn số đúng nhé!</div>', unsafe_allow_html=True)
        
        # Đồ vật tĩnh hơn chút để bé đếm
        html_hinh = ""
        for _ in range(st.session_state.so):
            html_hinh += f'<span class="object-item" style="animation: wiggle 2s infinite;">{st.session_state.hinh}</span>'
        st.markdown(f'<div>{html_hinh}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 3 Nút bấm to đùng
        b1, b2, b3 = st.columns(3)
        for i, so in enumerate(st.session_state.lua_chon_buoc3):
            with [b1, b2, b3][i]:
                if st.button(f"{so}", key=f"btn_quiz_{i}"):
                    if so == st.session_state.so:
                        st.balloons()
                        phat_am_thanh("Đúng rồi! Bé giỏi quá!")
                        time.sleep(1)
                        st.session_state.buoc = 4
                        st.rerun()
                    else:
                        st.error("Chưa đúng rồi!")
                        phat_am_thanh("Sai rồi, bé thử lại nhé")

    # --- BƯỚC 4: TƯ DUY (SỐ LIỀN SAU) ---
    elif st.session_state.buoc == 4:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="character">🤔</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instruction">Số nào đứng SAU số <span style="color:red; font-size:50px">{st.session_state.so}</span> ?</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        b1, b2, b3 = st.columns(3)
        for i, so in enumerate(st.session_state.lua_chon_buoc4):
            with [b1, b2, b3][i]:
                if st.button(f"{so}", key=f"btn_logic_{i}"):
                    if so == st.session_state.so + 1:
                        st.balloons()
                        phat_am_thanh("Xuất sắc! Bé thông minh quá!")
                        time.sleep(1.5)
                        st.session_state.buoc = 5
                        st.rerun()
                    else:
                        st.error("Sai rồi!")
                        phat_am_thanh("Bé suy nghĩ thêm nhé")

    # --- BƯỚC 5: PHẦN THƯỞNG ---
    elif st.session_state.buoc == 5:
        st.markdown('<div class="main-card" style="background:#fff9c4">', unsafe_allow_html=True)
        st.markdown('<div class="character">🏆</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-title">CHÚC MỪNG BÉ!</div>', unsafe_allow_html=True)
        st.markdown('<div class="instruction">Bé đã hoàn thành bài học rồi!</div>', unsafe_allow_html=True)
        
        # Ảnh động chúc mừng (GIF từ Giphy)
        st.markdown('<img src="https://media.giphy.com/media/26tOZ42Mg6pbTUPHW/giphy.gif" width="100%" style="border-radius:20px;">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🔄 CHƠI LẠI TỪ ĐẦU"):
            tao_cau_hoi_moi()
            st.session_state.buoc = 2
            st.rerun()

# Footer
st.markdown('<div style="text-align:center; color: #888; margin-top: 50px;">© 2025 Ứng dụng AI Mầm non</div>', unsafe_allow_html=True)
