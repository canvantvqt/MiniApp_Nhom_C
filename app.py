"""Mini App Nhóm C: Vận động thể chất và thói quen ngồi.
Giao diện nâng cấp cho dự án STEM Tin học 9 – Nhóm C, Lớp 9C.
Các hàm xử lí dữ liệu vẫn được gọi từ logic.py hiện có.
"""
import io
from pathlib import Path

import streamlit as st
import pandas as pd

from logic import (
    REQUIRED_COLUMNS,
    prepare_dataframe,
    validate_dataframe,
    summarize_dataframe,
    create_message,
)

# 1. CẤU HÌNH
st.set_page_config(
    page_title="Vận động thể chất – Thói quen ngồi",
    page_icon="🏃",
    layout="wide",
)

# 2. ĐỌC DỮ LIỆU – giữ nguyên cấu trúc file của dự án
@st.cache_data
def load_sample():
    return pd.read_csv("data/du_lieu_mo_phong_30_HS.csv")


def read_uploaded(file):
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(
            file,
            sheet_name="Du_lieu_khao_sat",
            skiprows=2,
        )
    raise ValueError("Chỉ hỗ trợ tệp CSV hoặc Excel (.xlsx, .xls).")


def dataframe_to_excel(data):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        data.to_excel(writer, index=False, sheet_name="Ket_qua_phan_tich")
    return output.getvalue()


# 3. NHẬN DIỆN GIAO DIỆN
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Be Vietnam Pro','Segoe UI',Arial,sans-serif;}
.stApp {background:linear-gradient(180deg,#fff7ed 0%,#fff1e8 48%,#fff8f2 100%);color:#3b211c;}
.block-container {max-width:1480px;padding-top:1rem;padding-bottom:2rem;}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#ffead5 0%,#ffe1d6 55%,#fff1e8 100%);border-right:1px solid #f2c5ae;}
.top-strip {background:linear-gradient(90deg,#fff0d9,#ffe1d5);border:1px solid #f0c4a7;border-radius:15px;padding:.7rem 1rem;margin:.1rem 0 1rem;color:#5a2a20;}
.top-strip strong {color:#9f1d1d;}
.hero {background:linear-gradient(110deg,#8f1717 0%,#b52a1d 48%,#f07824 100%);padding:1.2rem 1.5rem;border-radius:19px;color:white;margin:.65rem 0 1rem;box-shadow:0 9px 25px #9f1d1d26;}
.hero h1 {color:white!important;font-size:clamp(1.45rem,2.7vw,2.15rem);font-weight:800;margin:.2rem 0 .25rem;}
.hero p {color:#edf4ff;margin:0;}
.eyebrow {display:inline-block;background:#ffffff20;border:1px solid #ffffff60;border-radius:99px;padding:.28rem .7rem;font-size:.76rem;font-weight:800;letter-spacing:.03em;}
.section-title {font-size:1.3rem;font-weight:800;color:#9f1d1d;margin:.3rem 0;}
.section-sub {color:#79564d;margin-bottom:1rem;}
.feature-card {height:100%;min-height:150px;background:linear-gradient(145deg,#fffdf9,#fff0e5);border:1px solid #f1d2bd;border-radius:17px;padding:1rem 1.05rem;box-shadow:0 4px 14px #8f321510;}
.feature-card h3 {font-size:1rem;color:#9f1d1d;font-weight:800;margin:.35rem 0;}
.feature-card p {font-size:.88rem;line-height:1.5;color:#70574f;margin:0;}
.feature-icon {font-size:2rem;line-height:1.2;}
div[data-testid="stMetric"] {background:#fffdf9;border:1px solid #efcfba;border-radius:15px;padding:.85rem .95rem;}
div[data-testid="stMetricValue"] {color:#a5221b;font-weight:800;}
.stButton>button,.stDownloadButton>button {border-radius:11px;font-weight:750;min-height:2.55rem;}
div[data-testid="stDataFrame"] {border:1px solid #efcfba;border-radius:12px;overflow:hidden;}
div[data-testid="stTabs"] button {font-weight:750;}
.stButton>button, .stDownloadButton>button {border:1px solid #b52a1d;color:#8f1717;background:#fff8f1;}
.stButton>button:hover, .stDownloadButton>button:hover {background:#9f1d1d;color:white;border-color:#9f1d1d;}
input:focus, textarea:focus {border-color:#e87524!important;box-shadow:0 0 0 .15rem #f9c18b!important;}
.panel-note {background:#fff0df;border:1px solid #f1c69f;border-radius:13px;padding:.8rem 1rem;color:#71351f;}
.footer {text-align:center;color:#805d51;font-size:.82rem;line-height:1.7;padding:1rem .5rem;}
</style>
""", unsafe_allow_html=True)

# Banner ảnh: đặt hero_nhom_c.png cùng thư mục với app.py.
hero_path = Path(__file__).with_name("hero_nhom_c.png")
if hero_path.exists():
    st.image(str(hero_path), use_container_width=True)

st.markdown(
    '<div class="top-strip">🏫 <strong>TRƯỜNG TH, THCS & THPT TRƯNG VƯƠNG</strong>'
    ' &nbsp; · &nbsp; DỰ ÁN STEM TIN HỌC 9'
    ' &nbsp; · &nbsp; <strong>NHÓM C – LỚP 9C</strong></div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🏃 MINI APP · NHÓM C")
    st.markdown("**VẬN ĐỘNG THỂ CHẤT & THÓI QUEN NGỒI**")
    st.caption("LỚP 9C · DỮ LIỆU VÌ SỨC KHỎE HỌC ĐƯỜNG")
    st.divider()
    st.markdown("### 🧭 CÁC KHU VỰC")
    st.markdown("- 🏃 Tự kiểm tra thói quen")
    st.markdown("- 📊 Phân tích khảo sát")
    st.markdown("- 📘 Kiến thức & an toàn")
    st.divider()
    st.markdown("💗 **Thông điệp**")
    st.write("Bớt ngồi lâu – tăng vận động – sống khỏe mỗi ngày!")
    st.caption("Sản phẩm học tập, không thay thế tư vấn y tế.")

st.markdown(
    '<div class="hero"><span class="eyebrow">MINI APP STEM · NHÓM C · LỚP 9C</span>'
    '<h1>🏃 Vận động thể chất và thói quen ngồi</h1>'
    '<p>Bớt ngồi lâu – tăng vận động – sống khỏe mỗi ngày! '
    'Cùng quan sát dữ liệu và xây dựng thói quen tích cực.</p></div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs([
    "🏃 Tự kiểm tra thói quen",
    "📊 Phân tích khảo sát",
    "📘 Kiến thức & an toàn",
])

# 4. TỰ KIỂM TRA THÓI QUEN
with tab1:
    st.markdown(
        '<div class="section-title">💗 Tự xem lại thói quen của em</div>'
        '<div class="section-sub">Điền thông tin gần đúng để xem thông điệp gợi ý. '
        'Không cần nhập tên hoặc dữ liệu định danh.</div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns([1, 1])
    with left:
        with st.container(border=True):
            st.markdown("#### 👟 Hoạt động thể chất")
            activity = st.number_input(
                "Phút vận động vừa–mạnh trong một ngày",
                min_value=0, max_value=1440, value=45, step=5,
            )
            days = st.slider("Số ngày có vận động trong tuần", 0, 7, 4)
            activity_type = st.selectbox(
                "Hoạt động thường tham gia",
                ["Đi bộ", "Chạy bộ", "Đạp xe", "Bóng đá", "Cầu lông",
                 "Bơi", "Thể dục/thể thao khác", "Ít vận động"],
            )
    with right:
        with st.container(border=True):
            st.markdown("#### 🪑 Thói quen ngồi")
            sitting = st.number_input(
                "Thời gian ngồi liên tục lâu nhất (phút/lần)",
                min_value=0, max_value=1440, value=75, step=5,
            )
            st.markdown(
                '<div class="panel-note">⏰ Hãy thử đứng dậy, vươn vai hoặc đi lại '
                'nhẹ nhàng sau một khoảng thời gian ngồi học.</div>',
                unsafe_allow_html=True,
            )

    st.markdown("#### 📌 Thông điệp dành cho em")
    message = create_message(activity, sitting)
    st.info(f"🌱 {message}")
    m1, m2, m3 = st.columns(3)
    m1.metric("👟 Vận động mỗi ngày", f"{activity} phút")
    m2.metric("📅 Số ngày vận động", f"{days}/7 ngày")
    m3.metric("🪑 Ngồi liên tục lâu nhất", f"{sitting} phút")
    st.caption(
        f"Hoạt động đã chọn: {activity_type} · "
        "Mốc 60 phút/ngày và ngồi liên tục trên 60 phút là các mốc tham khảo/quy ước giáo dục."
    )

# 5. PHÂN TÍCH KHẢO SÁT
with tab2:
    st.markdown(
        '<div class="section-title">📊 Khám phá dữ liệu khảo sát</div>'
        '<div class="section-sub">Tải dữ liệu khảo sát đã ẩn danh hoặc chọn dữ liệu mô phỏng '
        'để thực hành phân tích.</div>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown("#### 📂 Nguồn dữ liệu")
        uploaded = st.file_uploader(
            "Chọn tệp Excel hoặc CSV",
            type=["xlsx", "xls", "csv"],
            key="survey_upload",
        )
        use_sample = st.checkbox(
            "🧪 Dùng dữ liệu mô phỏng 30 học sinh để xem thử",
            value=uploaded is None,
        )

    try:
        if uploaded is not None:
            raw = read_uploaded(uploaded)
            source_label = "Tệp khảo sát được tải lên"
        elif use_sample:
            raw = load_sample()
            source_label = "Dữ liệu mô phỏng – 30 học sinh"
        else:
            raw = pd.DataFrame(columns=REQUIRED_COLUMNS)
            source_label = "Chưa chọn dữ liệu"

        if len(raw) == 0:
            st.warning("Chưa có dữ liệu. Hãy tải tệp khảo sát hoặc chọn dữ liệu mô phỏng.")
        else:
            data = prepare_dataframe(raw)
            st.caption(f"📌 Nguồn đang xem: {source_label}")
            issues = validate_dataframe(data)
            if issues:
                st.warning("Cần kiểm tra dữ liệu trước khi sử dụng kết quả:")
                for issue in issues:
                    st.write("• " + issue)
            else:
                st.success(f"Dữ liệu hợp lệ về cấu trúc: {len(data)} bản ghi.")

            summary = summarize_dataframe(data)
            st.markdown("#### 🌟 Các chỉ số nổi bật")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("👥 Số học sinh", summary["total"])
            k2.metric("🏃 Vận động dưới 60 phút", summary["activity_below_60"])
            k3.metric("💪 Vận động từ 60 phút", summary["activity_at_least_60"])
            k4.metric("🪑 Ngồi liên tục trên 60 phút", summary["sitting_over_60"])

            chart_data = pd.DataFrame({
                "Nhóm": [
                    "Vận động dưới 60 phút",
                    "Vận động từ 60 phút",
                    "Ngồi liên tục trên 60 phút",
                ],
                "Số học sinh": [
                    summary["activity_below_60"],
                    summary["activity_at_least_60"],
                    summary["sitting_over_60"],
                ],
            })
            st.markdown("#### 📈 Biểu đồ thống kê")
            st.bar_chart(chart_data.set_index("Nhóm"), use_container_width=True)

            with st.expander("🧮 Liên hệ kiến thức Tin học 9: COUNTIF – SUMIF – IF", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(
                        f"**COUNTIF:** Đếm {summary['activity_below_60']} học sinh "
                        "có thời gian vận động dưới 60 phút/ngày."
                    )
                    st.write(
                        f"**COUNTIF:** Đếm {summary['sitting_over_60']} học sinh "
                        "ngồi liên tục trên 60 phút/lần."
                    )
                with c2:
                    st.write(
                        f"**SUMIF:** Tổng số phút vận động của nhóm dưới 60 phút là "
                        f"{summary['sum_minutes_below_60']:.0f} phút."
                    )
                    st.write(
                        "**IF kết hợp OR:** Tạo thông điệp khi vận động dưới 60 phút "
                        "hoặc ngồi liên tục trên 60 phút."
                    )

            with st.expander("🔍 Xem bảng dữ liệu đã xử lí"):
                st.dataframe(data, use_container_width=True, hide_index=True)

            st.download_button(
                "⬇️ Tải bảng kết quả Excel",
                data=dataframe_to_excel(data),
                file_name="Ket_qua_phan_tich_nhom_C.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
    except Exception as e:
        st.error(f"Không thể đọc hoặc xử lý tệp: {e}")
        st.info(
            "Kiểm tra tên cột và cấu trúc tệp theo mẫu khảo sát đi kèm "
            "trong thư mục data."
        )

# 6. KIẾN THỨC & AN TOÀN
with tab3:
    st.markdown(
        '<div class="section-title">📘 Kiến thức nền và nguyên tắc an toàn</div>'
        '<div class="section-sub">Hiểu thông điệp vận động, cách đọc dữ liệu '
        'và giới hạn của sản phẩm học tập.</div>',
        unsafe_allow_html=True,
    )
    a, b, c = st.columns(3)
    for col, icon, title, desc in [
        (a, "🏃", "Vận động mỗi ngày", "WHO khuyến nghị trẻ em và thanh thiếu niên 5–17 tuổi nên có trung bình ít nhất 60 phút/ngày hoạt động thể chất mức vừa đến mạnh trong tuần."),
        (b, "🪑", "Hạn chế ngồi lâu", "Đứng dậy, vươn vai hoặc đi lại nhẹ nhàng giúp tạo nhịp nghỉ trong thời gian học tập và sử dụng thiết bị."),
        (c, "📊", "Đọc dữ liệu có trách nhiệm", "Khảo sát tự khai báo có thể có sai số; kết quả chỉ phản ánh tập thể tham gia khảo sát."),
    ]:
        col.markdown(
            f'<div class="feature-card"><div class="feature-icon">{icon}</div>'
            f'<h3>{title}</h3><p>{desc}</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### 🎯 Các mốc của dự án")
    r1, r2 = st.columns(2)
    r1.metric("👟 Vận động tham khảo", "≥ 60 phút/ngày")
    r2.metric("🪑 Nhắc nghỉ giải lao", "Ngồi liên tục > 60 phút")
    st.info(
        "Mốc 60 phút vận động/ngày là mốc tham khảo giáo dục. "
        "Mốc ngồi liên tục trên 60 phút là quy ước truyền thông của dự án, "
        "không phải ngưỡng y tế."
    )

    with st.expander("🤖 Vai trò của AI trong dự án"):
        st.write(
            "AI được dùng để hỗ trợ nhóm tìm ý tưởng, tạo bản nháp và giải thích mã nguồn. "
            "Khi ứng dụng vận hành, Python thực hiện các phép tính theo quy tắc đã lập trình; "
            "ứng dụng không gọi API AI trả phí."
        )

    st.warning(
        "Không dùng ứng dụng để chẩn đoán, xếp loại sức khỏe hoặc so sánh công khai "
        "từng học sinh. Không nhập họ tên, số điện thoại, địa chỉ hay thông tin nhận dạng cá nhân."
    )
    st.caption(
        "Dữ liệu khảo sát cần được ẩn danh và chỉ sử dụng khi đã được phép. "
        "Dữ liệu mô phỏng không phải kết quả khảo sát thực tế."
    )

# 7. CHÂN TRANG
st.divider()
st.markdown(
    '<div class="footer">'
    '🏃 <b>DỮ LIỆU VÌ SỨC KHỎE HỌC ĐƯỜNG</b><br>'
    'Mini App STEM – Tin học 9 · <b>Nhóm C – Lớp 9C</b><br>'
    'Bớt ngồi lâu · Tăng vận động · Sống khỏe mỗi ngày<br>'
    '💗 TVS · Dữ liệu trung thực – Truyền thông có trách nhiệm'
    '</div>',
    unsafe_allow_html=True,
)

