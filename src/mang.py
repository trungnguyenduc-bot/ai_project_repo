import socket
import subprocess
import sys

temp = input("nhap dia chi ip:")
IP = socket.gethostbyname(temp)
print("Vui lòng đợi, đang quét tới IP vừa nhập", IP)
# Thuc hien quet cac cong dang mo
try:
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((IP, port))
        if result == 0:
            print("Cổng {}: 	 đang mở".format(port))
        sock.close()

# Kiem tra loi
except KeyboardInterrupt:
    print("Nếu nhấn Ctrl+C để thoát")
    sys.exit()

except socket.error:
    print("Không kết nối đến máy chủ")
    sys.exit()
