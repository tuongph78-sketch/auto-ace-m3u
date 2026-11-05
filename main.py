from pathlib import Path
import requests
import re

def run_full_pipeline():
    folder_path = Path(r"C:\Users\Admin\Desktop\PDF")
    url = "http://bit.ly/aceball111"
    
    print("=== BẮT ĐẦU QUY TRÌNH TỰ ĐỘNG HOÀN CHỈNH ===")
    
    # 1. Tạo thư mục làm việc nếu chưa có[cite: 1]
    try:
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"[*] Thư mục làm việc: {folder_path}")
    except Exception as e:
        print(f"[Lỗi] Không thể tạo thư mục: {e}")
        return

    # 2. Tải file từ bit.ly/aceball111[cite: 1]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"[*] Đang tải dữ liệu từ: {url}")
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=15)
        response.raise_for_status()
        
        downloaded_file_path = folder_path / "aceball111.txt"
        with open(downloaded_file_path, "wb") as f:
            f.write(response.content)
            
        print(f"[+] Tải file thành công: {downloaded_file_path.name}\n")
        
    except requests.exceptions.RequestException as e:
        print(f"[Lỗi kết nối/tải file]: {e}")
        print("[!] Tiếp tục xử lý các file có sẵn trong thư mục...\n")

    # 3. Đổi tên tất cả file .txt thành .m3u[cite: 1]
    txt_files = list(folder_path.glob("*.txt"))
    if txt_files:
        print(f"[*] Tìm thấy {len(txt_files)} file .txt. Bắt đầu đổi tên thành .m3u...")
        for txt_file in txt_files:
            m3u_file = txt_file.with_suffix(".m3u")
            try:
                if m3u_file.exists():
                    m3u_file.unlink()
                txt_file.rename(m3u_file)
                print(f"   [Thành công] {txt_file.name} -> {m3u_file.name}")
            except Exception as e:
                print(f"   [Lỗi] Không thể đổi tên file {txt_file.name}: {e}")
    else:
        print("[!] Không tìm thấy file .txt nào mới để đổi tên.")

    # 4. Quét và chuyển đổi các liên kết acestream:// hoặc ace:// thành http:// trong tất cả file .m3u[cite: 2]
    m3u_files = list(folder_path.glob("*.m3u"))
    if not m3u_files:
        print(f"[!] Không tìm thấy file .m3u nào trong thư mục {folder_path}")
        return

    print(f"\n[*] Đang quét và chuyển đổi link trong {len(m3u_files)} file .m3u...")

    for m3u_file in m3u_files:
        try:
            with open(m3u_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            updated_lines = []
            converted_count = 0

            for line in lines:
                stripped_line = line.strip()
                if "acestream://" in stripped_line or "ace://" in stripped_line:
                    for prefix in ["acestream://", "ace://"]:
                        match = re.search(rf'({re.escape(prefix)}[a-zA-Z0-9]+)', stripped_line)
                        if match:
                            link_found = match.group(1)
                            content_id = link_found.replace(prefix, "").strip()
                            http_url = f"http://127.0.0.1:6878/ace/getstream?id={content_id}"
                            line = line.replace(link_found, http_url)
                            converted_count += 1
                updated_lines.append(line)

            with open(m3u_file, "w", encoding="utf-8") as f:
                f.writelines(updated_lines)

            print(f"   [Thành công] File {m3u_file.name}: Đã chuyển đổi {converted_count} liên kết.")

        except Exception as e:
            print(f"   [Lỗi] Xử lý file {m3u_file.name}: {e}")

    print("\n[+] HOÀN TẤT TOÀN BỘ QUY TRÌNH!")

if __name__ == "__main__":
    run_full_pipeline()
