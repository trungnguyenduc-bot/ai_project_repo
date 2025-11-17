import os
import sqlite3
import shutil
from datetime import datetime, timedelta

# === Cấu hình thư mục gốc ===
FOLDER = r"C:\Users\dungt\Downloads\review\1109\rework"
TREN12P_FOLDER = os.path.join(FOLDER, "Tren_12P")
os.makedirs(TREN12P_FOLDER, exist_ok=True)

def parse_custom_timestamp(ts_str):
    try:
        if ts_str in (None, '', 'null'):
            return None
        parts = ts_str.split("-")
        if len(parts) == 7:
            date_part = "-".join(parts[:6])
            ms_part = parts[6].ljust(6, "0")  # '077' -> '077000'
            full_ts = f"{date_part}-{ms_part}"
            return datetime.strptime(full_ts, "%Y-%m-%d-%H-%M-%S-%f").timestamp()
        else:
            return None
    except:
        return None

def format_duration(seconds):
    return str(timedelta(seconds=int(seconds)))

def analyze_db_file(path):
    """Trả về tổng thời gian hoạt động (giây) của file DB"""
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='text_events'")
        if not cursor.fetchone():
            conn.close()
            return None

        cursor.execute("SELECT timestamp FROM text_events ORDER BY timestamp")
        raw_rows = cursor.fetchall()
        conn.close()

        timestamps = []
        for row in raw_rows:
            ts = parse_custom_timestamp(row[0])
            if ts is not None:
                timestamps.append(ts)

        if len(timestamps) < 2:
            return None

        timestamps.sort()
        total_active_time = timestamps[-1] - timestamps[0]
        return round(total_active_time, 2)

    except Exception as e:
        print(f"[ERROR] {path}: {e}")
        return None

def process_and_move(folder):
    moved_files = []

    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".db") or file.endswith(".dp"):
                full_path = os.path.join(root, file)
                result = analyze_db_file(full_path)

                if result and result >= 12 * 60:  # >= 12 phút
                    print(f"✅ {file} có thời gian hoạt động {format_duration(result)} → move sang Tren_12P")

                    dest_path = os.path.join(TREN12P_FOLDER, file)
                    if os.path.exists(dest_path):
                        base, ext = os.path.splitext(file)
                        count = 1
                        while os.path.exists(dest_path):
                            new_name = f"{base}_{count}{ext}"
                            dest_path = os.path.join(TREN12P_FOLDER, new_name)
                            count += 1

                    shutil.move(full_path, dest_path)
                    moved_files.append(file)

    print(f"\n📦 Đã chuyển {len(moved_files)} file vào: {TREN12P_FOLDER}")
    return moved_files

def main():
    moved = process_and_move(FOLDER)
    print("\nDanh sách file đã chuyển:")
    for f in moved:
        print(" -", f)

if __name__ == "__main__":
    main()
