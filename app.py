import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from logic import REQUIRED_COLUMNS, prepare_dataframe, validate_dataframe, summarize_dataframe, create_message

st.set_page_config(page_title="Vận động thể chất và thói quen ngồi", page_icon="🏃", layout="wide")

st.title("🏃 Mini App: Vận động thể chất và thói quen ngồi")
st.caption("Sản phẩm STEM Tin học 9 – sử dụng dữ liệu khảo sát ẩn danh để phân tích và truyền thông sức khỏe học đường.")

with st.expander("Mục tiêu và cách sử dụng", expanded=False):
    st.markdown("""
    1. Tải tệp Excel/CSV khảo sát hoặc dùng dữ liệu mẫu.
    2. Kiểm tra dữ liệu, xem thống kê và biểu đồ.
    3. Đọc thông điệp gợi ý để thảo luận về thói quen vận động và ngồi lâu.

    **Lưu ý:** Mốc 60 phút vận động/ngày là mốc tham khảo giáo dục cho lứa tuổi học sinh, không dùng để chẩn đoán sức khỏe cá nhân. Mốc ngồi liên tục trên 60 phút là quy ước của dự án nhằm nhắc nhở nghỉ giải lao, không phải ngưỡng y tế.
    """)

@st.cache_data
def load_sample():
    return pd.read_csv("data/du_lieu_mo_phong_30_HS.csv")

def read_uploaded(file):
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file, sheet_name="Du_lieu_khao_sat", skiprows=2)
    raise ValueError("Chỉ hỗ trợ tệp CSV hoặc Excel (.xlsx, .xls).")

tab1, tab2, tab3 = st.tabs(["Tự kiểm tra thói quen", "Phân tích khảo sát", "Kiến thức & an toàn"])

with tab1:
    st.subheader("Tự xem lại thói quen của em")
    c1, c2 = st.columns(2)
    with c1:
        activity = st.number_input("Phút vận động vừa–mạnh trong một ngày", min_value=0, max_value=1440, value=45, step=5)
        days = st.slider("Số ngày có vận động trong tuần", 0, 7, 4)
    with c2:
        sitting = st.number_input("Thời gian ngồi liên tục lâu nhất (phút/lần)", min_value=0, max_value=1440, value=75, step=5)
        activity_type = st.selectbox("Hoạt động thường tham gia", ["Đi bộ", "Chạy bộ", "Đạp xe", "Bóng đá", "Cầu lông", "Bơi", "Thể dục/thể thao khác", "Ít vận động"])
    st.info(create_message(activity, sitting))
    st.caption(f"Hoạt động đã chọn: {activity_type} · Số ngày vận động: {days}/7 ngày. Đây là công cụ tự phản ánh, không phải đánh giá y tế.")

with tab2:
    st.subheader("Nạp dữ liệu khảo sát")
    uploaded = st.file_uploader("Chọn tệp Excel hoặc CSV", type=["xlsx", "xls", "csv"])
    use_sample = st.checkbox("Dùng dữ liệu mô phỏng 30 học sinh để xem thử", value=uploaded is None)
    try:
        if uploaded is not None:
            raw = read_uploaded(uploaded)
        elif use_sample:
            raw = load_sample()
        else:
            raw = pd.DataFrame(columns=REQUIRED_COLUMNS)

        if len(raw) == 0:
            st.warning("Chưa có dữ liệu. Hãy tải tệp khảo sát hoặc chọn dữ liệu mô phỏng.")
        else:
            data = prepare_dataframe(raw)
            issues = validate_dataframe(data)
            if issues:
                st.warning("Cần kiểm tra dữ liệu trước khi sử dụng kết quả:")
                for issue in issues:
                    st.write("• " + issue)
            else:
                st.success(f"Dữ liệu hợp lệ về cấu trúc: {len(data)} bản ghi.")
            summary = summarize_dataframe(data)
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Số học sinh", summary["total"])
            k2.metric("Vận động dưới 60 phút", summary["activity_below_60"])
            k3.metric("Vận động từ 60 phút", summary["activity_at_least_60"])
            k4.metric("Ngồi liên tục trên 60 phút", summary["sitting_over_60"])

            st.markdown("**Bảng dữ liệu đã xử lý**")
            st.dataframe(data, use_container_width=True, hide_index=True)

            chart_data = pd.DataFrame({
                "Nhóm": ["Vận động dưới 60 phút", "Vận động từ 60 phút", "Ngồi liên tục trên 60 phút"],
                "Số học sinh": [summary["activity_below_60"], summary["activity_at_least_60"], summary["sitting_over_60"]]
            }).set_index("Nhóm")
            st.markdown("**Biểu đồ thống kê**")
            st.bar_chart(chart_data)

            st.markdown("**Liên hệ kiến thức Tin học 9**")
            st.write(f"- COUNTIF: đếm {summary['activity_below_60']} học sinh có thời gian vận động dưới 60 phút/ngày.")
            st.write(f"- COUNTIF: đếm {summary['sitting_over_60']} học sinh có thời gian ngồi liên tục trên 60 phút/lần.")
            st.write(f"- SUMIF: tổng số phút vận động của nhóm dưới 60 phút là {summary['sum_minutes_below_60']:.0f} phút.")
            st.write(f"- IF kết hợp OR: tạo thông điệp khi vận động dưới 60 phút hoặc ngồi liên tục trên 60 phút.")

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                data.to_excel(writer, index=False, sheet_name="Ket_qua_phan_tich")
            st.download_button("Tải bảng kết quả Excel", data=output.getvalue(),
                               file_name="Ket_qua_phan_tich_nhom_C.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Không thể đọc hoặc xử lý tệp: {e}")
        st.info("Kiểm tra tên cột và cấu trúc tệp theo mẫu khảo sát đi kèm trong thư mục data.")

with tab3:
    st.subheader("Kiến thức và nguyên tắc an toàn")
    st.markdown("""
    **Thông điệp dự án:** *Bớt ngồi lâu – tăng vận động – sống khỏe mỗi ngày.*

    - WHO khuyến nghị trẻ em và thanh thiếu niên 5–17 tuổi nên có trung bình ít nhất 60 phút/ngày hoạt động thể chất mức vừa đến mạnh trong tuần.
    - Trong Mini App, ngưỡng ngồi liên tục trên 60 phút là quy ước truyền thông do nhóm dự án lựa chọn để khuyến khích nghỉ giải lao và vận động nhẹ.
    - Dữ liệu khảo sát do học sinh tự khai báo nên có thể có sai số; kết quả chỉ phản ánh tập thể khảo sát.
    - Không nhập họ tên, số điện thoại, địa chỉ hoặc thông tin nhận dạng cá nhân. Chỉ sử dụng mã học sinh đã ẩn danh.
    - Ứng dụng không chẩn đoán, không đưa ra chỉ định điều trị và không thay thế tư vấn của nhân viên y tế.
    - AI được dùng để hỗ trợ nhóm trong quá trình tìm ý tưởng, tạo và giải thích mã nguồn; ứng dụng không gọi API AI trả phí khi vận hành.
    """)

st.divider()
st.caption("Sản phẩm minh họa phục vụ học tập STEM – Tin học 9. Dữ liệu mẫu là dữ liệu mô phỏng, không phải kết quả khảo sát thực tế.")
