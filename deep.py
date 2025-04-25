#!/data/data/com.termux/files/usr/bin/python3

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
import json

# Konfigurasi
VERSION = "4.0"
UPDATE_URL = "https://raw.githubusercontent.com/Habibzz01/UpdateTools-/refs/heads/main/deep.py"
CONFIG_FILE = "/data/data/com.termux/files/home/.xdeepcleaner.conf"
LOG_FILE = "/data/data/com.termux/files/home/.xdeepcleaner.log"

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

# Fungsi untuk logging
def log_pesan(level, pesan):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {pesan}\n"
    
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
    except:
        pass

# Animasi loading yang lebih baik
def animasi_loading(teks, durasi=2):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + durasi
    
    sys.stdout.write(f"\r{Warna.BIRU}⏳ {teks}...{Warna.RESET}")
    sys.stdout.flush()
    
    while time.time() < end_time:
        for char in chars:
            if time.time() >= end_time:
                break
            sys.stdout.write(f"\r{Warna.BIRU}{char} {teks}...{Warna.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
    
    sys.stdout.write("\r" + " " * (len(teks) + 10) + "\r")
    sys.stdout.flush()

# Membersihkan layar (cross-platform)
def bersihkan_layar():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Header aplikasi yang lebih menarik
def tampilkan_header():
    bersihkan_layar()
    print(f"{Warna.UNGU}{Warna.BOLD}╔══════════════════════════════════════════════════╗")
    print(f"║    {Warna.CYAN}⚡ XBIBZ DEEP CLEANER v{VERSION} (NO ROOT) ⚡{Warna.UNGU}    ║")
    print(f"║   {Warna.PUTIH}Developed by: {Warna.HIJAU}Xbibz Official Team{Warna.UNGU}     ║")
    print(f"║       {Warna.PUTIH}Powered by: {Warna.KUNING}X404X Security{Warna.UNGU}        ║")
    print(f"╚═════��════════════════════════════════════════════╝{Warna.RESET}\n")

# Cek update dari GitHub
def cek_update():
    try:
        response = requests.get(UPDATE_URL, timeout=5)
        if response.status_code == 200:
            remote_content = response.text
            remote_version = None
            
            # Cari versi di remote content
            for line in remote_content.split('\n'):
                if line.startswith('VERSION = '):
                    remote_version = line.split('=')[1].strip().strip('"')
                    break
            
            if remote_version and remote_version != VERSION:
                print(f"{Warna.KUNING}⚠ Update tersedia! Versi {remote_version} sudah dirilis.{Warna.RESET}")
                print(f"{Warna.CYAN}🔗 Download di: {UPDATE_URL}{Warna.RESET}")
                return True
            else:
                print(f"{Warna.HIJAU}✅ Anda menggunakan versi terbaru ({VERSION}){Warna.RESET}")
                return False
    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal memeriksa update: {e}{Warna.RESET}")
        return False
    return False

# Memindai file sampah dengan lebih komprehensif
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
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/.Statuses",
        "/storage/emulated/0/Telegram/Telegram Documents",
        "/storage/emulated/0/tencent/MicroMsg/xlog",
        "/storage/emulated/0/tencent/MicroMsg/WeiXin",
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures/Screenshots",
        "/storage/emulated/0/Pictures/Instagram",
        "/storage/emulated/0/Pictures/Saved Pictures",
        "/storage/emulated/0/Android/media/com.facebook.orca/files/",
        "/storage/emulated/0/Android/media/com.facebook.katana/files/"
    ]
    
    ekstensi_sampah = [
        '.tmp', '.temp', '.log', '.cache', '.thumb', '.bak',
        '.dmp', '.old', '.recycle', '.trash', '.delete'
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
                        # Skip file penting
                        if any(skip in file_path.lower() for skip in ['important', 'essential', 'backup']):
                            continue
                            
                        # Cek ekstensi file
                        _, ext = os.path.splitext(file)
                        if ext.lower() in ekstensi_sampah or any(keyword in file.lower() for keyword in ['cache', 'temp', 'tmp']):
                            file_size = os.path.getsize(file_path)
                            file_sampah.append((file_path, file_size))
                            total_size += file_size
                    except:
                        continue
    
    if not file_sampah:
        print(f"{Warna.KUNING}⚠ Tidak ditemukan file sampah!{Warna.RESET}")
        return None
    
    # Urutkan berdasarkan ukuran (terbesar ke terkecil)
    file_sampah.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n{Warna.HIJAU}✅ Ditemukan {len(file_sampah)} file sampah ({total_size / (1024*1024):.2f} MB){Warna.RESET}")
    return file_sampah

# Menampilkan file sampah dengan pagination
def tampilkan_dan_hapus_file(file_sampah):
    if not file_sampah:
        return
    
    page_size = 10
    total_pages = (len(file_sampah) // page_size + 1)
    current_page = 1
    
    while True:
        start_idx = (current_page - 1) * page_size
        end_idx = start_idx + page_size
        
        print(f"\n{Warna.BOLD}📁 Daftar File Sampah (Halaman {current_page}/{total_pages}):{Warna.RESET}")
        for idx, (file, size) in enumerate(file_sampah[start_idx:end_idx], start_idx + 1):
            print(f"{Warna.CYAN}{idx}. {file} ({size / (1024*1024):.2f} MB){Warna.RESET}")
        
        print(f"\n{Warna.MERAH}⚠ PERINGATAN: Penghapusan permanen!{Warna.RESET}")
        print(f"{Warna.KUNING}📌 Petunjuk: all=hapus semua, cancel=batal, next=halaman berikut, prev=halaman sebelumnya{Warna.RESET}")
        
        pilihan = input(f"\n{Warna.BOLD}🚀 Pilih file (contoh: 1,2,3 / all / cancel / next / prev): {Warna.RESET}").strip().lower()
        
        if pilihan == "cancel":
            return
        elif pilihan == "all":
            konfirmasi = input(f"{Warna.MERAH}Yakin hapus SEMUA {len(file_sampah)} file? (y/n): {Warna.RESET}").strip().lower()
            if konfirmasi == "y":
                deleted_count = 0
                deleted_size = 0
                
                with ThreadPoolExecutor(max_workers=4) as executor:
                    futures = []
                    for file, size in file_sampah:
                        futures.append(executor.submit(delete_file, file, size))
                    
                    for future in futures:
                        success, file, size = future.result()
                        if success:
                            deleted_count += 1
                            deleted_size += size
                
                print(f"{Warna.HIJAU}✅ {deleted_count}/{len(file_sampah)} file berhasil dihapus ({deleted_size / (1024*1024):.2f} MB dibebaskan){Warna.RESET}")
                return
        elif pilihan == "next":
            if current_page < total_pages:
                current_page += 1
            else:
                print(f"{Warna.KUNING}⚠ Sudah di halaman terakhir!{Warna.RESET}")
        elif pilihan == "prev":
            if current_page > 1:
                current_page -= 1
            else:
                print(f"{Warna.KUNING}⚠ Sudah di halaman pertama!{Warna.RESET}")
        else:
            indices = []
            for i in pilihan.split(","):
                i = i.strip()
                if i.isdigit():
                    idx = int(i) - 1
                    if 0 <= idx < len(file_sampah):
                        indices.append(idx)
            
            if indices:
                deleted_count = 0
                deleted_size = 0
                
                for idx in indices:
                    file, size = file_sampah[idx]
                    success, _, _ = delete_file(file, size)
                    if success:
                        deleted_count += 1
                        deleted_size += size
                
                print(f"{Warna.HIJAU}✅ {deleted_count} file berhasil dihapus ({deleted_size / (1024*1024):.2f} MB dibebaskan){Warna.RESET}")
                return
            else:
                print(f"{Warna.MERAH}❌ Pilihan tidak valid!{Warna.RESET}")

# Fungsi untuk menghapus file dengan penanganan error yang lebih baik
def delete_file(file_path, file_size):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            log_pesan("INFO", f"Deleted: {file_path}")
            return (True, file_path, file_size)
    except PermissionError:
        try:
            # Coba dengan chmod jika permission denied
            os.chmod(file_path, 0o777)
            os.remove(file_path)
            log_pesan("INFO", f"Deleted (after chmod): {file_path}")
            return (True, file_path, file_size)
        except Exception as e:
            log_pesan("ERROR", f"Gagal menghapus {file_path}: {str(e)}")
            return (False, file_path, str(e))
    except Exception as e:
        log_pesan("ERROR", f"Gagal menghapus {file_path}: {str(e)}")
        return (False, file_path, str(e))
    
    return (False, file_path, "File not found")

# Membersihkan cache aplikasi dengan lebih efektif
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
            "/storage/emulated/0/Android/media/*/Cache",
            "/storage/emulated/0/Android/media/*/temp",
            "/storage/emulated/0/Android/media/*/Temp",
            "/storage/emulated/0/Android/media/*/logs",
            "/storage/emulated/0/Android/media/*/Logs"
        ]

        total_deleted = 0
        deleted_folders = 0

        for cache_dir in cache_dirs:
            try:
                # Gunakan find untuk mencari folder cache
                cache_folders = subprocess.run(
                    f"find {cache_dir} -type d -iname '*cache*' -o -iname '*temp*' -o -iname '*log*' 2>/dev/null",
                    shell=True,
                    capture_output=True,
                    text=True
                ).stdout.splitlines()

                for folder in cache_folders:
                    try:
                        # Hitung ukuran sebelum dihapus
                        du_output = subprocess.run(
                            f"du -s '{folder}'",
                            shell=True,
                            capture_output=True,
                            text=True
                        ).stdout
                        
                        if du_output:
                            size_before = int(du_output.split()[0])
                        else:
                            size_before = 0

                        # Hapus isi folder tapi jaga strukturnya
                        subprocess.run(f"rm -rf '{folder}'/* 2>/dev/null", shell=True)
                        subprocess.run(f"rm -rf '{folder}'/.* 2>/dev/null", shell=True)

                        total_deleted += size_before
                        deleted_folders += 1
                        print(f"{Warna.HIJAU}✅ Cache dibersihkan: {folder} ({size_before/1024:.2f} KB){Warna.RESET}")
                        log_pesan("INFO", f"Cleaned cache: {folder} ({size_before} KB)")
                    except Exception as e:
                        print(f"{Warna.KUNING}⚠ Gagal membersihkan {folder}: {e}{Warna.RESET}")
                        log_pesan("WARNING", f"Failed to clean {folder}: {e}")
            except Exception as e:
                print(f"{Warna.KUNING}⚠ Gagal memproses {cache_dir}: {e}{Warna.RESET}")
                log_pesan("WARNING", f"Failed to process {cache_dir}: {e}")

        if total_deleted > 0:
            print(f"{Warna.HIJAU}✅ Berhasil membersihkan {deleted_folders} folder cache ({total_deleted/1024:.2f} MB dibebaskan){Warna.RESET}")
        else:
            print(f"{Warna.KUNING}⚠ Tidak ada cache yang bisa dibersihkan.{Warna.RESET}")

    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal membersihkan cache: {e}{Warna.RESET}")
        log_pesan("ERROR", f"Cache cleaning failed: {e}")

# Menghentikan aplikasi di latar belakang dengan lebih aman
def hentikan_aplikasi_latar():
    print(f"\n{Warna.BIRU}🛑 Menghentikan aplikasi latar belakang...{Warna.RESET}")
    animasi_loading("Menghentikan aplikasi", 2)
    
    try:
        # Dapatkan daftar aplikasi yang berjalan (kecuali system dan termux)
        cmd = "ps -A -o PID,NAME | grep -vE 'termux|system_|android.' | awk '{print $2}' | sort | uniq"
        running_apps = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        ).stdout.splitlines()
        
        running_apps = [app for app in running_apps if app and len(app) < 50]
        
        if not running_apps:
            print(f"{Warna.KUNING}⚠ Tidak ada aplikasi latar belakang yang berjalan.{Warna.RESET}")
            return
        
        print(f"{Warna.CYAN}📌 Aplikasi yang akan dihentikan:{Warna.RESET}")
        for i, app in enumerate(running_apps, 1):
            print(f"{Warna.PUTIH}{i}. {app}{Warna.RESET}")
        
        konfirmasi = input(f"\n{Warna.MERAH}⚠ Yakin hentikan {len(running_apps)} aplikasi? (y/n): {Warna.RESET}").strip().lower()
        
        if konfirmasi == 'y':
            stopped_count = 0
            for app in running_apps:
                try:
                    subprocess.run(f"am force-stop {app}", shell=True, check=True)
                    print(f"{Warna.HIJAU}✅ Berhenti: {app}{Warna.RESET}")
                    stopped_count += 1
                    log_pesan("INFO", f"Stopped app: {app}")
                except subprocess.CalledProcessError:
                    print(f"{Warna.KUNING}⚠ Gagal menghentikan: {app} (mungkin sistem){Warna.RESET}")
                    log_pesan("WARNING", f"Failed to stop: {app}")
                except Exception as e:
                    print(f"{Warna.MERAH}❌ Error saat menghentikan {app}: {e}{Warna.RESET}")
                    log_pesan("ERROR", f"Error stopping {app}: {e}")
            
            print(f"{Warna.HIJAU}✅ {stopped_count}/{len(running_apps)} aplikasi berhasil dihentikan!{Warna.RESET}")
    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal menghentikan aplikasi: {e}{Warna.RESET}")
        log_pesan("ERROR", f"Failed to stop background apps: {e}")

# Fitur pemulihan file terhapus yang lebih informatif
def pulihkan_file_terhapus():
    print(f"\n{Warna.BIRU}🔮 Memindai file yang terhapus...{Warna.RESET}")
    animasi_loading("Memulihkan file", 3)
    
    try:
        print(f"{Warna.CYAN}📌 Rekomendasi Tools Pemulihan File:{Warna.RESET}")
        print(f"{Warna.PUTIH}1. DiskDigger (Play Store){Warna.RESET}")
        print(f"{Warna.PUTIH}2. Undeleter (Play Store){Warna.RESET}")
        print(f"{Warna.PUTIH}3. PhotoRec (Linux/Android dengan root){Warna.RESET}")
        
        print(f"\n{Warna.KUNING}⚠ Tips Pemulihan File:{Warna.RESET}")
        print(f"{Warna.PUTIH}- Segera hentikan penggunaan storage setelah file terhapus{Warna.RESET}")
        print(f"{Warna.PUTIH}- Gunakan mode pesawat untuk mencegah overwrite data{Warna.RESET}")
        print(f"{Warna.PUTIH}- Untuk hasil terbaik, gunakan perangkat dengan akses root{Warna.RESET}")
        
        print(f"\n{Warna.MERAH}❌ Tanpa akses root, pemulihan file sangat terbatas.{Warna.RESET}")
        
        # Coba cari file yang baru dihapus di recycle bin
        recycle_bins = [
            "/storage/emulated/0/RecycleBin",
            "/storage/emulated/0/.RecycleBin",
            "/storage/emulated/0/Trash",
            "/storage/emulated/0/.Trash"
        ]
        
        found_files = []
        for rb in recycle_bins:
            if os.path.exists(rb):
                for root, _, files in os.walk(rb):
                    for file in files:
                        file_path = os.path.join(root, file)
                        found_files.append(file_path)
        
        if found_files:
            print(f"\n{Warna.HIJAU}✅ Ditemukan {len(found_files)} file di Recycle Bin:{Warna.RESET}")
            for i, file in enumerate(found_files[:5], 1):
                print(f"{Warna.CYAN}{i}. {file}{Warna.RESET}")
            if len(found_files) > 5:
                print(f"{Warna.CYAN}... dan {len(found_files)-5} file lainnya{Warna.RESET}")
        else:
            print(f"\n{Warna.KUNING}⚠ Tidak ditemukan file di Recycle Bin.{Warna.RESET}")
        
    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal memulihkan file: {e}{Warna.RESET}")
        log_pesan("ERROR", f"File recovery failed: {e}")

# Fitur baru: Optimasi memori
def optimasi_memori():
    print(f"\n{Warna.BIRU}⚡ Mengoptimalkan penggunaan memori...{Warna.RESET}")
    animasi_loading("Optimasi memori", 2)
    
    try:
        # Dapatkan info memori sebelum optimasi
        mem_info = subprocess.run(
            "free -m",
            shell=True,
            capture_output=True,
            text=True
        ).stdout
        
        print(f"{Warna.CYAN}📊 Penggunaan Memori Sebelum:{Warna.RESET}")
        print(mem_info)
        
        # Bersihkan cache memori
        subprocess.run("sync; echo 3 > /proc/sys/vm/drop_caches", shell=True)
        
        # Hentikan aplikasi yang boros memori
        top_mem = subprocess.run(
            "ps -A -o %mem,pid,comm | sort -nr | head -n 5",
            shell=True,
            capture_output=True,
            text=True
        ).stdout
        
        print(f"\n{Warna.CYAN}📊 Aplikasi Paling Boros Memori:{Warna.RESET}")
        print(top_mem)
        
        # Dapatkan info memori setelah optimasi
        mem_info_after = subprocess.run(
            "free -m",
            shell=True,
            capture_output=True,
            text=True
        ).stdout
        
        print(f"\n{Warna.CYAN}📊 Penggunaan Memori Sesudah:{Warna.RESET}")
        print(mem_info_after)
        
        print(f"\n{Warna.HIJAU}✅ Optimasi memori selesai!{Warna.RESET}")
        log_pesan("INFO", "Memory optimization completed")
    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal mengoptimalkan memori: {e}{Warna.RESET}")
        log_pesan("ERROR", f"Memory optimization failed: {e}")

# Fitur baru: Analisis penyimpanan
def analisis_penyimpanan():
    print(f"\n{Warna.BIRU}📊 Menganalisis penggunaan penyimpanan...{Warna.RESET}")
    animasi_loading("Analisis penyimpanan", 3)
    
    try:
        # Analisis partisi utama
        print(f"{Warna.CYAN}📌 Partisi Utama:{Warna.RESET}")
        df_output = subprocess.run(
            "df -h /data /storage/emulated/0",
            shell=True,
            capture_output=True,
            text=True
        ).stdout
        print(df_output)
        
        # Folder terbesar di internal storage
        print(f"\n{Warna.CYAN}📌 Folder Terbesar di Internal Storage:{Warna.RESET}")
        du_output = subprocess.run(
            "du -h --max-depth=1 /storage/emulated/0 2>/dev/null | sort -hr | head -n 10",
            shell=True,
            capture_output=True,
            text=True
        ).stdout
        print(du_output)
        
        # Folder terbesar di home termux
        print(f"\n{Warna.CYAN}📌 Folder Terbesar di Termux Home:{Warna.RESET}")
        du_termux = subprocess.run(
            "du -h --max-depth=1 /data/data/com.termux/files/home 2>/dev/null | sort -hr | head -n 10",
            shell=True,
            capture_output=True,
            text=True
        ).stdout
        print(du_termux)
        
        print(f"\n{Warna.HIJAU}✅ Analisis penyimpanan selesai!{Warna.RESET}")
        log_pesan("INFO", "Storage analysis completed")
    except Exception as e:
        print(f"{Warna.MERAH}❌ Gagal menganalisis penyimpanan: {e}{Warna.RESET}")
        log_pesan("ERROR", f"Storage analysis failed: {e}")

# Menu utama yang diperbarui
def main():
    # Cek dependensi
    try:
        subprocess.run("command -v du", shell=True, check=True)
        subprocess.run("command -v find", shell=True, check=True)
    except:
        print(f"{Warna.MERAH}❌ Error: Dependensi 'du' atau 'find' tidak ditemukan!{Warna.RESET}")
        print(f"{Warna.KUNING}📌 Jalankan 'pkg install coreutils findutils' di Termux{Warna.RESET}")
        return
    
    while True:
        tampilkan_header()
        print(f"{Warna.BOLD}📋 Menu Utama v{VERSION}:{Warna.RESET}")
        print(f"{Warna.CYAN}1. Scan & Hapus File Sampah{Warna.RESET}")
        print(f"{Warna.CYAN}2. Bersihkan Cache Aplikasi{Warna.RESET}")
        print(f"{Warna.CYAN}3. Hentikan Aplikasi Latar Belakang{Warna.RESET}")
        print(f"{Warna.CYAN}4. Pulihkan File Terhapus{Warna.RESET}")
        print(f"{Warna.CYAN}5. Optimasi Memori{Warna.RESET}")
        print(f"{Warna.CYAN}6. Analisis Penyimpanan{Warna.RESET}")
        print(f"{Warna.CYAN}7. Cek Update{Warna.RESET}")
        print(f"{Warna.CYAN}8. Keluar{Warna.RESET}")
        
        pilihan = input(f"\n{Warna.BOLD}🔹 Pilih opsi (1-8): {Warna.RESET}").strip()
        
        if pilihan == "1":
            file_sampah = scan_file_sampah()
            if file_sampah:
                tampilkan_dan_hapus_file(file_sampah)
        elif pilihan == "2":
            bersihkan_cache_aplikasi()
        elif pilihan == "3":
            hentikan_aplikasi_latar()
        elif pilihan == "4":
            pulihkan_file_terhapus()
        elif pilihan == "5":
            optimasi_memori()
        elif pilihan == "6":
            analisis_penyimpanan()
        elif pilihan == "7":
            cek_update()
        elif pilihan == "8":
            print(f"{Warna.HIJAU}🚪 Keluar dari aplikasi...{Warna.RESET}")
            exit()
        else:
            print(f"{Warna.MERAH}❌ Pilihan tidak valid!{Warna.RESET}")
        
        input(f"\n{Warna.BOLD}🔶 Tekan Enter untuk kembali ke menu...{Warna.RESET}")

if __name__ == "__main__":
    try:
        # Cek jika script dijalankan di Termux
        if not os.path.exists("/data/data/com.termux/files/usr/bin"):
            print(f"{Warna.MERAH}❌ Script ini didesain untuk dijalankan di Termux!{Warna.RESET}")
            exit(1)
        
        main()
    except KeyboardInterrupt:
        print(f"\n{Warna.MERAH}❌ Script dihentikan oleh pengguna.{Warna.RESET}")
        log_pesan("WARNING", "Script stopped by user")
        exit()
    except Exception as e:
        print(f"\n{Warna.MERAH}❌ Error: {e}{Warna.RESET}")
        log_pesan("ERROR", f"Unexpected error: {e}")
        exit(1)