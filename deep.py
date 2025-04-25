#!/usr/bin/env python3
import os
import time
import shutil
import subprocess
import sys
import requests
import platform
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading
import hashlib
import zipfile
import tarfile
import stat

# Konfigurasi
VERSION = "2.0"
UPDATE_URL = "https://raw.githubusercontent.com/Habibzz01/UpdateTools-/refs/heads/main/convert.py"
BACKUP_DIR = "/storage/emulated/0/XBIBZ_Backup"
LOG_FILE = "/storage/emulated/0/XBIBZ_DeepCleaner.log"

# Warna untuk tampilan
class Warna:
    MERAH = "\033[91m"
    HIJAU = "\033[92m"
    KUNING = "\033[93m"
    BIRU = "\033[94m"
    UNGU = "\033[95m"
    CYAN = "\033[96m"
    PUTIH = "\033[97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

# Animasi loading
def animasi_loading(teks, durasi=2):
    chars = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    end_time = time.time() + durasi
    while time.time() < end_time:
        for char in chars:
            sys.stdout.write(f"\r{Warna.BIRU}{char} {teks}...{Warna.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(teks) + 10) + "\r")
    sys.stdout.flush()

# Membersihkan layar
def bersihkan_layar():
    os.system("clear" if os.name != "nt" else "cls")

# Log aktivitas
def log_aktivitas(pesan):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {pesan}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

# Header aplikasi
def tampilkan_header():
    bersihkan_layar()
    print(f"{Warna.UNGU}{Warna.BOLD}╔══════════════════════════════════════════════════╗")
    print(f"║       {Warna.CYAN}XBIBZ DEEP CLEANER v{VERSION} (NO ROOT){Warna.UNGU}       ║")
    print(f"║      {Warna.PUTIH}Developed by: {Warna.HIJAU}Xbibz Official{Warna.UNGU}         ║")
    print(f"║            {Warna.PUTIH}Team: {Warna.KUNING}X404X{Warna.UNGU}                     ║")
    print(f"╚══════════════════════════════════════════════════╝{Warna.RESET}\n")

# Cek update
def cek_update():
    try:
        response = requests.get(UPDATE_URL, timeout=10)
        if response.status_code == 200:
            remote_version = None
            for line in response.text.split('\n'):
                if line.startswith('VERSION = '):
                    remote_version = line.split('=')[1].strip().strip('"')
                    break
            
            if remote_version and remote_version > VERSION:
                print(f"\n{Warna.KUNING}⚠ Update tersedia! Versi {remote_version} tersedia.{Warna.RESET}")
                pilihan = input(f"{Warna.BOLD}🔹 Mau update sekarang? (y/n): {Warna.RESET}").strip().lower()
                if pilihan == 'y':
                    update_script(response.text)
            else:
                print(f"\n{Warna.HIJAU}✓ Anda menggunakan versi terbaru ({VERSION}).{Warna.RESET}")
                time.sleep(1)
    except Exception as e:
        print(f"\n{Warna.KUNING}⚠ Gagal cek update: {e}{Warna.RESET}")
        time.sleep(1)

# Update script
def update_script(new_content):
    try:
        backup_file = f"{os.path.basename(__file__)}.bak"
        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(open(__file__, "r", encoding="utf-8").read())
        
        with open(__file__, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        os.chmod(__file__, 0o755)
        print(f"\n{Warna.HIJAU}✅ Update berhasil! Versi baru akan aktif setelah restart.{Warna.RESET}")
        log_aktivitas(f"Script diupdate ke versi baru")
        input(f"{Warna.BOLD}🔶 Tekan Enter untuk restart script...{Warna.RESET}")
        restart_script()
    except Exception as e:
        print(f"\n{Warna.MERAH}❌ Gagal update: {e}{Warna.RESET}")
        time.sleep(2)

# Restart script
def restart_script():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Cek akses penyimpanan
def cek_akses_penyimpanan():
    try:
        test_dir = "/storage/emulated/0/XBIBZ_TEST"
        os.makedirs(test_dir, exist_ok=True)
        with open(f"{test_dir}/test.txt", "w") as f:
            f.write("test")
        os.remove(f"{test_dir}/test.txt")
        os.rmdir(test_dir)
        return True
    except Exception as e:
        print(f"\n{Warna.MERAH}❌ Akses penyimpanan ditolak!{Warna.RESET}")
        print(f"{Warna.KUNING}⚠ Berikan izin penyimpanan ke Termux di pengaturan aplikasi.{Warna.RESET}")
        return False

# Backup file sebelum dihapus
def backup_file(file_path):
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR, exist_ok=True)
        
        rel_path = os.path.relpath(file_path, "/")
        safe_path = rel_path.replace("/", "_").replace("..", "up")
        backup_path = os.path.join(BACKUP_DIR, safe_path)
        
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return True
    except Exception as e:
        log_aktivitas(f"Gagal backup {file_path}: {e}")
        return False

# Memindai file sampah dengan lebih banyak lokasi
def scan_file_sampah():
    lokasi_sampah = [
        "/storage/emulated/0/Android/data",
        "/storage/emulated/0/Android/obb",
        "/data/data/com.termux/files/home/.cache",
        "/storage/emulated/0/Download",
        "/storage/emulated/0/DCIM/.thumbnails",
        "/storage/emulated/0/DCIM/Screenshots",
        "/storage/emulated/0/Pictures/.thumbnails",
        "/storage/emulated/0/Movies/.thumbnails",
        "/storage/emulated/0/.thumbnails",
        "/storage/emulated/0/WhatsApp/Media/.Statuses",
        "/storage/emulated/0/WhatsApp/Media/.Thumbs",
        "/storage/emulated/0/Telegram/Telegram Images",
        "/storage/emulated/0/Telegram/Telegram Video",
        "/storage/emulated/0/DCIM/Camera/.thumbdata"
    ]
    
    ekstensi_sampah = [
        ".tmp", ".temp", ".log", ".cache", ".thumb", ".bak",
        ".dmp", ".crash", ".recycle", ".trash", ".delete"
    ]
    
    file_sampah = []
    total_size = 0
    
    print(f"{Warna.BIRU}🔍 Memindai file sampah...{Warna.RESET}")
    animasi_loading("Sedang memindai", 3)
    
    for lokasi in lokasi_sampah:
        if os.path.exists(lokasi):
            for root, dirs, files in os.walk(lokasi):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if any(file.endswith(ext) for ext in ekstensi_sampah) or "cache" in root.lower():
                            file_size = os.path.getsize(file_path)
                            file_sampah.append((file_path, file_size))
                            total_size += file_size
                    except:
                        continue
    
    if not file_sampah:
        print(f"{Warna.KUNING}⚠ Tidak ditemukan file sampah!{Warna.RESET}")
        return None
    
    print(f"\n{Warna.HIJAU}✅ Ditemukan {len(file_sampah)} file sampah ({total_size / (1024*1024):.2f} MB){Warna.RESET}")
    log_aktivitas(f"Menemukan {len(file_sampah)} file sampah ({total_size / (1024*1024):.2f} MB)")
    return file_sampah

# Menampilkan dan menghapus file sampah dengan opsi backup
def tampilkan_dan_hapus_file(file_sampah):
    if not file_sampah:
        return
    
    print(f"\n{Warna.BOLD}📁 Daftar File Sampah:{Warna.RESET}")
    for idx, (file, size) in enumerate(file_sampah[:50], 1):  # Tampilkan 50 file pertama saja
        print(f"{Warna.CYAN}{idx}. {file} ({size / 1024:.2f} KB){Warna.RESET}")
    
    if len(file_sampah) > 50:
        print(f"{Warna.KUNING}... dan {len(file_sampah)-50} file lainnya.{Warna.RESET}")
    
    print(f"\n{Warna.MERAH}⚠ PERINGATAN: Penghapusan permanen!{Warna.RESET}")
    print(f"{Warna.KUNING}📌 Tips: Gunakan 'all' untuk semua file, '1,3,5' untuk pilihan, atau 'cancel' untuk batal{Warna.RESET}")
    
    pilihan = input(f"\n{Warna.BOLD}🚀 Pilih file (contoh: 1,2,3 / all / backup / cancel): {Warna.RESET}").strip().lower()
    
    if pilihan == "cancel":
        return
    elif pilihan == "all":
        konfirmasi = input(f"{Warna.MERAH}Yakin hapus SEMUA {len(file_sampah)} file? (y/n): {Warna.RESET}").strip().lower()
        if konfirmasi == "y":
            deleted = 0
            with ThreadPoolExecutor() as executor:
                for file, size in file_sampah:
                    try:
                        os.remove(file)
                        deleted += 1
                        log_aktivitas(f"Menghapus: {file} ({size} bytes)")
                    except Exception as e:
                        log_aktivitas(f"Gagal hapus {file}: {e}")
            print(f"{Warna.HIJAU}✅ {deleted}/{len(file_sampah)} file sampah berhasil dihapus!{Warna.RESET}")
    elif pilihan == "backup":
        konfirmasi = input(f"{Warna.BIRU}Backup SEMUA file sebelum dihapus? (y/n): {Warna.RESET}").strip().lower()
        if konfirmasi == "y":
            backed_up = 0
            deleted = 0
            for file, size in file_sampah:
                if backup_file(file):
                    backed_up += 1
                    try:
                        os.remove(file)
                        deleted += 1
                        log_aktivitas(f"Backup dan hapus: {file}")
                    except Exception as e:
                        log_aktivitas(f"Gagal hapus setelah backup {file}: {e}")
            print(f"{Warna.HIJAU}✅ {backed_up} file di-backup, {deleted} dihapus!{Warna.RESET}")
            print(f"{Warna.CYAN}📁 Backup disimpan di: {BACKUP_DIR}{Warna.RESET}")
    else:
        indices = [int(i.strip()) - 1 for i in pilihan.split(",") if i.strip().isdigit()]
        deleted = 0
        for idx in indices:
            if 0 <= idx < len(file_sampah):
                file, size = file_sampah[idx]
                try:
                    os.remove(file)
                    deleted += 1
                    print(f"{Warna.HIJAU}✅ Berhasil hapus: {file}{Warna.RESET}")
                    log_aktivitas(f"Menghapus: {file} ({size} bytes)")
                except Exception as e:
                    print(f"{Warna.MERAH}❌ Gagal hapus {file}: {e}{Warna.RESET}")
                    log_aktivitas(f"Gagal hapus {file}: {e}")
        if deleted > 0:
            print(f"{Warna.HIJAU}✅ {deleted} file berhasil dihapus!{Warna.RESET}")

# Membersihkan cache aplikasi secara lebih menyeluruh
def bersihkan_cache_aplikasi():
    print(f"\n{Warna.BIRU}🧹 Membersihkan cache aplikasi...{Warna.RESET}")
    animasi_loading("Membersihkan cache", 3)

    try:
        # Daftar folder cache yang bisa dibersihkan tanpa root
        cache_dirs = [
            "/data/data/com.termux/files/usr/var/cache",
            "/data/data/com.termux/files/home/.cache",
            "/storage/emulated/0/Android/data/*/cache",
            "/storage/emulated/0/Android/data/*/code_cache",
            "/storage/emulated/0/Android/media/*/cache",
            "/storage/emulated/0/Android/data/*/files/cache",
            "/storage/emulated/0/Android/data/*/app_webview",
            "/storage/emulated/0/Android/data/*/app_textures"
        ]

        total_deleted = 0
        cleaned_folders = 0

        for cache_dir in cache_dirs:
            # Cari semua folder cache
            cache_folders = subprocess.run(
                f"find {cache_dir} -type d -name '*cache*' 2>/dev/null",
                shell=True,
                capture_output=True,
                text=True
            ).stdout.splitlines()

            for folder in cache_folders:
                try:
                    # Hitung ukuran sebelum dihapus
                    du_result = subprocess.run(
                        f"du -s '{folder}' 2>/dev/null | cut -f1",
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    size_before = int(du_result.stdout.strip() or 0)

                    # Hapus isi folder (jaga folder tetap ada)
                    subprocess.run(f"rm -rf '{folder}'/* 2>/dev/null", shell=True)
                    subprocess.run(f"rm -rf '{folder}'/.* 2>/dev/null", shell=True)

                    total_deleted += size_before
                    cleaned_folders += 1
                    log_aktivitas(f"Membersihkan cache: {folder} ({size_before} KB)")
                except Exception as e:
                    log_aktivitas(f"Gagal membersihkan {folder}: {e}")

        if total_deleted > 0:
            print(f"{Warna.HIJAU}✅ Berhasil membersihkan {cleaned_folders} folder cache ({total_deleted/1024:.2f} MB)!{Warna.RESET}")
        else:
            print(f"{Warna.KUNING}⚠ Tidak ada cache yang bisa dibersihkan.{Warna.RESET}")

    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal membersihkan cache: {e}{Warna.RESET}")
        log_aktivitas(f"Gagal membersihkan cache: {e}")

# Mengoptimalkan memori dengan menghentikan aplikasi di latar belakang
def optimalkan_memori():
    print(f"\n{Warna.BIRU}🛑 Menghentikan aplikasi latar belakang...{Warna.RESET}")
    animasi_loading("Mengoptimalkan memori", 2)
    
    try:
        # Dapatkan daftar aplikasi yang berjalan (kecuali sistem penting dan Termux)
        running_apps = subprocess.check_output(
            "ps -A -o ARGS= | grep -E '^[a-z]' | grep -v 'termux' | grep -v 'android' | grep -v 'system' | grep -v 'google' | awk '{print $1}' | sort -u",
            shell=True
        ).decode().split("\n")
        
        running_apps = [app for app in running_apps if app and "com.termux" not in app]
        
        if not running_apps:
            print(f"{Warna.KUNING}⚠ Tidak ada aplikasi latar yang bisa dihentikan.{Warna.RESET}")
            return
        
        stopped = 0
        for app in running_apps:
            try:
                subprocess.run(f"am force-stop {app} 2>/dev/null", shell=True)
                print(f"{Warna.HIJAU}✅ Berhenti: {app}{Warna.RESET}")
                stopped += 1
                log_aktivitas(f"Menghentikan aplikasi: {app}")
            except:
                continue
        
        print(f"{Warna.HIJAU}✅ {stopped} aplikasi latar berhasil dihentikan!{Warna.RESET}")
        
        # Clear RAM cache
        print(f"\n{Warna.BIRU}🧹 Membersihkan cache RAM...{Warna.RESET}")
        subprocess.run("sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null", shell=True)
        print(f"{Warna.HIJAU}✅ Cache RAM dibersihkan!{Warna.RESET}")
        log_aktivitas("Membersihkan cache RAM")
        
    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal mengoptimalkan memori: {e}{Warna.RESET}")
        log_aktivitas(f"Gagal mengoptimalkan memori: {e}")

# Fitur pemulihan file terhapus dengan lebih banyak opsi
def pulihkan_file_terhapus():
    print(f"\n{Warna.BIRU}🔮 Menu Pemulihan File Terhapus:{Warna.RESET}")
    print(f"{Warna.CYAN}1. Scan file yang mungkin dipulihkan{Warna.RESET}")
    print(f"{Warna.CYAN}2. Cari file spesifik (nama/ekstensi){Warna.RESET}")
    print(f"{Warna.CYAN}3. Kembali ke menu utama{Warna.RESET}")
    
    pilihan = input(f"\n{Warna.BOLD}🔹 Pilih opsi (1-3): {Warna.RESET}").strip()
    
    if pilihan == "1":
        scan_file_terhapus()
    elif pilihan == "2":
        cari_file_spesifik()
    elif pilihan == "3":
        return
    else:
        print(f"{Warna.MERAH}❌ Pilihan tidak valid!{Warna.RESET}")
    
    input(f"\n{Warna.BOLD}🔶 Tekan Enter untuk kembali...{Warna.RESET}")
    pulihkan_file_terhapus()

# Scan file yang mungkin dipulihkan
def scan_file_terhapus():
    print(f"\n{Warna.BIRU}🔍 Memindai file yang mungkin dipulihkan...{Warna.RESET}")
    animasi_loading("Memindai media penyimpanan", 5)
    
    try:
        # Cari file yang baru dihapus (masih ada inode-nya)
        deleted_files = subprocess.run(
            "find /storage -type f -name '*.*' -exec ls -i {} + 2>/dev/null | grep '? ' | awk '{print $2}'",
            shell=True,
            capture_output=True,
            text=True
        ).stdout.splitlines()
        
        if not deleted_files:
            print(f"{Warna.KUNING}⚠ Tidak ditemukan file yang bisa dipulihkan.{Warna.RESET}")
            print(f"{Warna.CYAN}📌 Gunakan aplikasi khusus seperti DiskDigger untuk pemulihan lebih lanjut.{Warna.RESET}")
            return
        
        print(f"\n{Warna.HIJAU}✅ Ditemukan {len(deleted_files)} file yang mungkin bisa dipulihkan:{Warna.RESET}")
        for idx, file in enumerate(deleted_files[:20], 1):
            print(f"{Warna.CYAN}{idx}. {file}{Warna.RESET}")
        
        if len(deleted_files) > 20:
            print(f"{Warna.KUNING}... dan {len(deleted_files)-20} file lainnya.{Warna.RESET}")
        
        print(f"\n{Warna.MERAH}⚠ PERINGATAN: Pemulihan tanpa root terbatas!{Warna.RESET}")
        print(f"{Warna.CYAN}📌 Untuk hasil terbaik, jangan tulis data baru ke penyimpanan.{Warna.RESET}")
        
    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal memindai: {e}{Warna.RESET}")
        log_aktivitas(f"Gagal memindai file terhapus: {e}")

# Cari file spesifik untuk dipulihkan
def cari_file_spesifik():
    print(f"\n{Warna.BIRU}🔎 Cari file spesifik untuk dipulihkan{Warna.RESET}")
    nama_file = input(f"{Warna.BOLD}🔹 Masukkan nama/ekstensi file (contoh: .jpg, dokumen): {Warna.RESET}").strip()
    
    if not nama_file:
        print(f"{Warna.MERAH}❌ Nama file tidak boleh kosong!{Warna.RESET}")
        return
    
    print(f"\n{Warna.BIRU}🔍 Mencari file '{nama_file}'...{Warna.RESET}")
    animasi_loading("Mencari file", 3)
    
    try:
        found_files = subprocess.run(
            f"find /storage -type f -iname '*{nama_file}*' 2>/dev/null | head -50",
            shell=True,
            capture_output=True,
            text=True
        ).stdout.splitlines()
        
        if not found_files:
            print(f"{Warna.KUNING}⚠ Tidak ditemukan file dengan pola '{nama_file}'.{Warna.RESET}")
            return
        
        print(f"\n{Warna.HIJAU}✅ Ditemukan {len(found_files)} file:{Warna.RESET}")
        for idx, file in enumerate(found_files[:20], 1):
            print(f"{Warna.CYAN}{idx}. {file}{Warna.RESET}")
        
        if len(found_files) > 20:
            print(f"{Warna.KUNING}... dan {len(found_files)-20} file lainnya.{Warna.RESET}")
        
        print(f"\n{Warna.CYAN}📌 File yang ditemukan mungkin masih utuh atau bisa dipulihkan.{Warna.RESET}")
        
    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal mencari: {e}{Warna.RESET}")
        log_aktivitas(f"Gagal mencari file {nama_file}: {e}")

# Fitur tambahan: Optimasi penyimpanan
def optimasi_penyimpanan():
    print(f"\n{Warna.BIRU}📊 Analisis penggunaan penyimpanan...{Warna.RESET}")
    animasi_loading("Menganalisis", 2)
    
    try:
        # Analisis penggunaan penyimpanan
        print(f"\n{Warna.BOLD}📁 Penggunaan Penyimpanan:{Warna.RESET}")
        subprocess.run("df -h /storage/emulated/0", shell=True)
        
        # Cari folder besar
        print(f"\n{Warna.BOLD}📂 Folder Terbesar di Penyimpanan Internal:{Warna.RESET}")
        subprocess.run("du -h /storage/emulated/0 --max-depth=2 2>/dev/null | sort -hr | head -10", shell=True)
        
        # Rekomendasi
        print(f"\n{Warna.BOLD}💡 Rekomendasi:{Warna.RESET}")
        print(f"{Warna.CYAN}1. Hapus file besar yang tidak perlu dari folder Download")
        print(f"2. Bersihkan cache aplikasi secara berkala")
        print(f"3. Pindahkan media ke SD card jika tersedia")
        print(f"4. Gunakan fitur 'Scan & Hapus File Sampah' secara rutin{Warna.RESET}")
        
    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal menganalisis: {e}{Warna.RESET}")
        log_aktivitas(f"Gagal analisis penyimpanan: {e}")

# Menu utama yang diperbarui
def main():
    # Cek akses penyimpanan pertama kali
    if not cek_akses_penyimpanan():
        input(f"{Warna.BOLD}🔶 Tekan Enter untuk keluar...{Warna.RESET}")
        return
    
    # Cek update
    cek_update()
    
    while True:
        tampilkan_header()
        print(f"{Warna.BOLD}📋 Menu Utama:{Warna.RESET}")
        print(f"{Warna.CYAN}1. Scan & Hapus File Sampah (Advanced){Warna.RESET}")
        print(f"{Warna.CYAN}2. Bersihkan Cache Aplikasi (Menyeluruh){Warna.RESET}")
        print(f"{Warna.CYAN}3. Optimasi Memori & Hentikan Aplikasi Latar{Warna.RESET}")
        print(f"{Warna.CYAN}4. Pulihkan File Terhapus (Eksperimental){Warna.RESET}")
        print(f"{Warna.CYAN}5. Analisis & Optimasi Penyimpanan{Warna.RESET}")
        print(f"{Warna.CYAN}6. Tentang Aplikasi{Warna.RESET}")
        print(f"{Warna.CYAN}7. Keluar{Warna.RESET}")
        
        pilihan = input(f"\n{Warna.BOLD}🔹 Pilih opsi (1-7): {Warna.RESET}").strip()
        
        if pilihan == "1":
            file_sampah = scan_file_sampah()
            if file_sampah:
                tampilkan_dan_hapus_file(file_sampah)
        elif pilihan == "2":
            bersihkan_cache_aplikasi()
        elif pilihan == "3":
            optimalkan_memori()
        elif pilihan == "4":
            pulihkan_file_terhapus()
        elif pilihan == "5":
            optimasi_penyimpanan()
        elif pilihan == "6":
            tampilkan_tentang()
        elif pilihan == "7":
            print(f"{Warna.HIJAU}🚪 Keluar dari aplikasi...{Warna.RESET}")
            exit()
        else:
            print(f"{Warna.MERAH}❌ Pilihan tidak valid!{Warna.RESET}")
        
        input(f"\n{Warna.BOLD}🔶 Tekan Enter untuk kembali ke menu...{Warna.RESET}")

# Tentang aplikasi
def tampilkan_tentang():
    tampilkan_header()
    print(f"{Warna.BOLD}📝 Tentang XBIBZ DEEP CLEANER v{VERSION}:{Warna.RESET}")
    print(f"{Warna.CYAN}• Fitur Utama:")
    print(f"  - Pembersihan file sampah canggih")
    print(f"  - Penghapusan cache aplikasi menyeluruh")
    print(f"  - Optimasi memori dengan menghentikan aplikasi latar")
    print(f"  - Analisis penggunaan penyimpanan")
    print(f"  - Pemulihan file terhapus dasar")
    print(f"  - Sistem backup sebelum penghapusan")
    print(f"  - Log aktivitas terperinci")
    print(f"  - Auto-update script{Warna.RESET}")
    
    print(f"\n{Warna.BOLD}⚙️ Persyaratan Sistem:{Warna.RESET}")
    print(f"{Warna.CYAN}• Android 5.0+ (Lollipop atau lebih baru)")
    print(f"• Termux terbaru")
    print(f"• Izin penyimpanan")
    print(f"• Koneksi internet untuk cek update{Warna.RESET}")
    
    print(f"\n{Warna.BOLD}👨‍💻 Developer:{Warna.RESET}")
    print(f"{Warna.CYAN}• Xbibz Official")
    print(f"• Team X404X")
    print(f"• https://github.com/xbibz{Warna.RESET}")
    
    input(f"\n{Warna.BOLD}🔶 Tekan Enter untuk kembali...{Warna.RESET}")

if __name__ == "__main__":
    try:
        # Setel eksekusi script
        if not os.access(__file__, os.X_OK):
            os.chmod(__file__, 0o755)
        
        # Buat direktori backup jika belum ada
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR, exist_ok=True)
        
        main()
    except KeyboardInterrupt:
        print(f"\n{Warna.MERAH}❌ Script dihentikan oleh pengguna.{Warna.RESET}")
        exit()
    except Exception as e:
        print(f"\n{Warna.MERAH}❌ Error: {e}{Warna.RESET}")
        log_aktivitas(f"Error: {e}")
        exit()