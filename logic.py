import pandas as pd

REQUIRED_COLUMNS = [
    "Mã HS",
    "Phút vận động vừa-mạnh/ngày",
    "Số ngày vận động/tuần",
    "Hoạt động thể chất thường tham gia",
    "Thời gian ngồi liên tục tối đa (phút/lần)",
]

def _number(series):
    return pd.to_numeric(series, errors="coerce")

def classify_activity_minutes(minutes):
    value = pd.to_numeric(minutes, errors="coerce")
    if pd.isna(value):
        return "Chưa đủ dữ liệu"
    return "Đạt mốc tham khảo 60 phút" if value >= 60 else "Dưới mốc tham khảo 60 phút"

def classify_sitting(minutes):
    value = pd.to_numeric(minutes, errors="coerce")
    if pd.isna(value):
        return "Chưa đủ dữ liệu"
    return "Ngồi liên tục trên 60 phút" if value > 60 else "Không quá 60 phút"

def create_message(activity_minutes, sitting_minutes):
    activity = pd.to_numeric(activity_minutes, errors="coerce")
    sitting = pd.to_numeric(sitting_minutes, errors="coerce")
    if pd.isna(activity) or pd.isna(sitting):
        return "Bổ sung dữ liệu để nhận thông điệp phù hợp."
    if activity < 60 and sitting > 60:
        return "Nên tăng thời gian vận động và chủ động đứng dậy, đi lại sau thời gian ngồi lâu."
    if activity < 60:
        return "Có thể tăng dần hoạt động thể chất phù hợp mỗi ngày."
    if sitting > 60:
        return "Duy trì vận động và nên xen kẽ nghỉ giải lao, đứng dậy sau thời gian ngồi lâu."
    return "Tiếp tục duy trì thói quen vận động và hạn chế ngồi liên tục quá lâu."

def prepare_dataframe(df):
    df = df.copy()
    df.columns = [str(c).strip().replace("–", "-").replace("—", "-") for c in df.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("Thiếu cột bắt buộc: " + ", ".join(missing))

    df = df[REQUIRED_COLUMNS].copy()
    df["Mã HS"] = df["Mã HS"].astype("string").str.strip()
    df["Phút vận động vừa-mạnh/ngày"] = _number(df["Phút vận động vừa-mạnh/ngày"])
    df["Số ngày vận động/tuần"] = _number(df["Số ngày vận động/tuần"])
    df["Thời gian ngồi liên tục tối đa (phút/lần)"] = _number(
        df["Thời gian ngồi liên tục tối đa (phút/lần)"]
    )
    df["Hoạt động thể chất thường tham gia"] = (
        df["Hoạt động thể chất thường tham gia"].fillna("").astype(str).str.strip()
    )

    df["Nhóm vận động"] = df["Phút vận động vừa-mạnh/ngày"].apply(classify_activity_minutes)
    df["Nhóm ngồi liên tục"] = df["Thời gian ngồi liên tục tối đa (phút/lần)"].apply(classify_sitting)
    df["Thông điệp gợi ý"] = df.apply(
        lambda r: create_message(
            r["Phút vận động vừa-mạnh/ngày"],
            r["Thời gian ngồi liên tục tối đa (phút/lần)"]
        ), axis=1
    )
    return df

def validate_dataframe(df):
    issues = []
    if df.empty:
        issues.append("Bảng dữ liệu chưa có bản ghi.")
    if df["Mã HS"].isna().any() or (df["Mã HS"].astype(str).str.strip() == "").any():
        issues.append("Có bản ghi thiếu Mã HS.")
    if df["Mã HS"].duplicated().any():
        issues.append("Có Mã HS bị trùng.")
    for col, low, high, label in [
        ("Phút vận động vừa-mạnh/ngày", 0, 1440, "Phút vận động/ngày"),
        ("Số ngày vận động/tuần", 0, 7, "Số ngày vận động/tuần"),
        ("Thời gian ngồi liên tục tối đa (phút/lần)", 0, 1440, "Thời gian ngồi liên tục"),
    ]:
        values = df[col]
        if values.isna().any():
            issues.append(f"Có dữ liệu thiếu hoặc không hợp lệ ở cột {label}.")
        if ((values < low) | (values > high)).any():
            issues.append(f"Có giá trị ngoài khoảng hợp lý ở cột {label} ({low}–{high}).")
    return issues

def summarize_dataframe(df):
    valid_activity = df["Phút vận động vừa-mạnh/ngày"].dropna()
    below_60 = df["Phút vận động vừa-mạnh/ngày"] < 60
    sitting_over_60 = df["Thời gian ngồi liên tục tối đa (phút/lần)"] > 60
    return {
        "total": int(len(df)),
        "activity_below_60": int(below_60.sum()),
        "activity_at_least_60": int((df["Phút vận động vừa-mạnh/ngày"] >= 60).sum()),
        "sitting_over_60": int(sitting_over_60.sum()),
        "sum_minutes_below_60": float(df.loc[below_60, "Phút vận động vừa-mạnh/ngày"].sum(skipna=True)),
        "sum_minutes_sitting_over_60": float(df.loc[sitting_over_60, "Phút vận động vừa-mạnh/ngày"].sum(skipna=True)),
        "average_activity": float(valid_activity.mean()) if len(valid_activity) else 0.0,
    }
