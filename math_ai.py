import streamlit as st
import random

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="AI Mầm Non - Bé Vui Học",
    page_icon="🐻",
    layout="centered"
)

# --- CSS GIAO DIỆN THÂN THIỆN ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #fff1eb, #ace0f9);
}
.card {
    background-color: white;
    padding: 30px;
    border-radius: 25px;
    text-align: center;
    font-size: 28px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}
.stButton>button {
    font-size: 22px;
    border-radius: 20px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="card">
    <h1>🏫 TRƯỜNG MẦM NON AI</h1>
    <h2>🤖 BÉ VUI HỌC CÙNG AI</h2>
    <p>ĐẾM SỐ – NHẬN BIẾT MÀU SẮC</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- DANH SÁCH CON VẬT ---
animals = ["🐶", "🐱", "🐰", "🐥", "🐸"]

# --- SESSION STATE ---
if "so_luong" not in st.session_state:
    st.session_state.so_luong = 0
    st.session_state.hinh = ""

# --- TẠO BÀI TẬP ---
if st.button("🎲 BẮT ĐẦU TRÒ CHƠI"):
    st.session_state.so_luong = random.randint(1, 5)
    st.session_state.hinh = random.choice(animals)

# --- HIỂN THỊ BÀI ---
if st.session_state.so_luong > 0:
    st.markdown(f"""
    <div class="card">
        <p>🐾 Bé hãy đếm xem có bao nhiêu con vật nhé!</p>
        <p style="font-size:50px;">
        {st.session_state.hinh * st.session_state.so_luong}
        </p>
    </div>
    """, unsafe_allow_html=True)

    tra_loi = st.number_input(
        "👉 Bé nhập số:",
        min_value=1,
        max_value=5,
        step=1
    )

    if st.button("✅ KIỂM TRA"):
        if tra_loi == st.session_state.so_luong:
            st.balloons()
            st.success("🎉 GIỎI QUÁ! BÉ LÀM ĐÚNG RỒI!")
        else:
            st.error("😊 CHƯA ĐÚNG, BÉ ĐẾM LẠI NHÉ!")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Sản phẩm AI dành cho trẻ mầm non – Cô giáo Lò Thị Hạnh-Trường MN Na Ư")

