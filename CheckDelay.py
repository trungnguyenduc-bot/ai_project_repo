import sqlite3
import os
import unicodedata

# === Hàm chuẩn hóa: bỏ dấu + chữ thường ===
def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    return text.lower().replace(" ", "")  # 👉 bỏ luôn khoảng trắng để lọc "timhieu"

# === Cấu hình thư mục chứa database ===
folder_path = r"E:\LamViec\FileTeam\26-08-2025\Vinh 684120140434\ThucHIen"  # 👉 THAY đường dẫn tại đây

# === Phần mở rộng hợp lệ ===
db_extensions = ('.db', '.sqlite', '.sqlite3')

# === Tìm file database ===
db_files = [f for f in os.listdir(folder_path) if f.endswith(db_extensions)]

if not db_files:
    print("❌ Không có file database nào.")
    exit()

# === Danh sách kết quả ===
results = []

# === Duyệt từng file ===
for db_file in db_files:
    db_path = os.path.join(folder_path, db_file)
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
                            if "timhieu" in normalized:  # ✅ Lọc không dấu + không cách
                                results.append((db_file, description))
            except:
                pass  # Bỏ qua bảng lỗi

        conn.close()

    except Exception as e:
        print(f"⚠️ Lỗi khi xử lý file {db_file}: {e}")

# === In kết quả ===
print("\n📋 CÁC MÔ TẢ CHỨA 'tìm hiểu' (mọi dạng viết):\n")
for filename, description in results:
    print(f"{filename} | {description}")
