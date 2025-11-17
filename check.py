import sqlite3
import os
import unicodedata
import shutil

# === Hàm chuẩn hóa: bỏ dấu + chữ thường ===
def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    return text.lower().replace(" ", "")

# === Cấu hình thư mục chứa database ===
folder_path = r"\\172.16.8.10\GDS Project\Record_video\gds-02\DucPD1\20-08-2025\Vinh 684120140434\Sang"
timhieu_folder = os.path.join(folder_path, "timhieu")

# Tạo folder đích nếu chưa tồn tại
os.makedirs(timhieu_folder, exist_ok=True)

# === Phần mở rộng hợp lệ ===
db_extensions = ('.db', '.sqlite', '.sqlite3')

# === Tìm file database ===
db_files = [f for f in os.listdir(folder_path) if f.endswith(db_extensions)]

if not db_files:
    print("❌ Không có file database nào.")
    exit()

# === Danh sách kết quả ===
results = []
moved_files = []

# === Duyệt từng file ===
for db_file in db_files:
    db_path = os.path.join(folder_path, db_file)
    file_has_match = False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Danh sách bảng
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            try:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cursor.fetchall()]
                if 'task_description' in columns:
                    cursor.execute(f"SELECT task_description FROM {table}")
                    rows = cursor.fetchall()
                    for row in rows:
                        description = row[0]
                        if description:
                            normalized = normalize_text(description)
                            if "timhieu" in normalized:
                                results.append((db_file, description))
                                file_has_match = True
            except:
                pass  # Bỏ qua bảng lỗi

        conn.close()

        # Nếu file có dữ liệu khớp -> di chuyển
        if file_has_match:
            dest_path = os.path.join(timhieu_folder, db_file)

            # Nếu file trùng tên, đổi tên để tránh ghi đè
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(db_file)
                count = 1
                while os.path.exists(dest_path):
                    new_name = f"{base}_{count}{ext}"
                    dest_path = os.path.join(timhieu_folder, new_name)
                    count += 1

            shutil.move(db_path, dest_path)
            moved_files.append(db_file)

    except Exception as e:
        print(f"⚠️ Lỗi khi xử lý file {db_file}: {e}")

# === In kết quả ===
print("\n📋 CÁC MÔ TẢ CHỨA 'tìm hiểu':\n")
for filename, description in results:
    print(f"{filename} | {description}")

print("\n📦 Đã di chuyển các file:")
for f in moved_files:
    print(f" - {f}")

print(f"\n✅ Tổng cộng {len(moved_files)} file đã được chuyển sang: {timhieu_folder}")
