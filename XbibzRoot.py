import os
import sys
import time
import json
import socket
import platform
import subprocess
import threading
import queue
import re
import random
import urllib.request
from datetime import datetime
from getpass import getpass
from colorama import init, Fore, Back, Style, AnsiToWin32

# Inisialisasi colorama
init(autoreset=True)
init(wrap=True, convert=True)

# Konfigurasi warna tema terminal
THEME = {
    'success': Fore.GREEN + Style.BRIGHT,
    'error': Fore.RED + Style.BRIGHT,
    'warning': Fore.YELLOW + Style.BRIGHT,
    'info': Fore.CYAN + Style.BRIGHT,
    'debug': Fore.MAGENTA + Style.BRIGHT,
    'title': Fore.BLUE + Style.BRIGHT + Back.WHITE,
    'menu': Fore.WHITE + Style.BRIGHT + Back.BLUE,
    'input': Fore.YELLOW + Style.BRIGHT,
    'special': Fore.RED + Back.YELLOW + Style.BRIGHT
}

# Animasi loading
ANIMATIONS = [
    ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", 
     "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"],
    ["🌍", "🌎", "🌏"],
    ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    ["😊", "😄", "😃", "😀", "😆", "😅"],
    ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂"]
]

class AndroidOTGController:
    def __init__(self):
        self.check_platform()
        self.check_dependencies()
        self.setup_terminal()
        self.adb_path = self.detect_adb()
        self.fastboot_path = self.detect_fastboot()
        self.current_device = None
        self.server_port = 5555
        self.server_ip = self.get_local_ip()
        self.command_queue = queue.Queue()
        self.running = True
        self.animation_running = False
        self.animation_thread = None
        
    def check_platform(self):
        """Cek platform dan terminal yang digunakan"""
        self.platform = platform.system().lower()
        self.terminal = self.detect_terminal()
        
        print(THEME['title'] + "\n" + "="*70)
        print(f"{'Ultimate Android OTG ADB Controller':^70}")
        print(f"{'Versi: 3.7.1 VIP+++':^70}")
        print(f"{'Platform: ' + self.platform.upper():^70}")
        print(f"{'Terminal: ' + self.terminal.upper():^70}")
        print("="*70 + Style.RESET_ALL + "\n")
        
    def detect_terminal(self):
        """Deteksi terminal yang digunakan"""
        try:
            if 'TERMUX' in os.environ:
                return 'termux'
            elif 'WT_SESSION' in os.environ:
                return 'windows terminal'
            elif 'GNOME_TERMINAL_SCREEN' in os.environ:
                return 'gnome terminal'
            elif 'KONSOLE_VERSION' in os.environ:
                return 'konsole'
            elif 'XTERM_VERSION' in os.environ:
                return 'xterm'
            elif 'ALACRITTY_LOG' in os.environ:
                return 'alacritty'
            elif 'TMUX' in os.environ:
                return 'tmux'
            elif 'STY' in os.environ:
                return 'screen'
            elif 'SSH_CONNECTION' in os.environ:
                return 'ssh'
            else:
                return 'unknown terminal'
        except:
            return 'unknown terminal'
    
    def setup_terminal(self):
        """Setup terminal dengan tema yang menarik"""
        try:
            # Set judul terminal
            if self.platform == 'windows':
                os.system('title Ultimate Android OTG ADB Controller - VIP+++')
            else:
                sys.stdout.write("\x1b]2;Ultimate Android OTG ADB Controller - VIP+++\x07")
            
            # Set warna terminal jika memungkinkan
            if self.platform != 'windows':
                os.system('setterm -background white -foreground blue -store')
        except:
            pass
    
    def check_dependencies(self):
        """Cek dan install dependencies yang diperlukan"""
        required_packages = ['colorama']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(THEME['warning'] + f"Package berikut tidak ditemukan: {', '.join(missing_packages)}")
            if self.confirm_action("Install package yang diperlukan?"):
                self.install_packages(missing_packages)
    
    def install_packages(self, packages):
        """Install package menggunakan pip"""
        try:
            import pip
            for package in packages:
                self.start_animation(f"Sedang menginstall {package}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                self.stop_animation()
                print(THEME['success'] + f"Berhasil menginstall {package}")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal menginstall package: {str(e)}")
            sys.exit(1)
    
    def detect_adb(self):
        """Deteksi lokasi ADB"""
        paths = {
            'windows': ['adb.exe', 'platform-tools\\adb.exe', os.path.join(os.environ.get('ProgramFiles', ''), 'Android\\android-sdk\\platform-tools\\adb.exe')],
            'linux': ['adb', '/usr/bin/adb', '/usr/local/bin/adb', os.path.expanduser('~/Android/Sdk/platform-tools/adb')],
            'android': ['adb', '/data/data/com.termux/files/usr/bin/adb']
        }
        
        for path in paths.get(self.platform, []):
            if os.path.exists(path):
                return path
        
        # Jika tidak ditemukan, coba cari di PATH
        try:
            subprocess.run(['adb', 'version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return 'adb'
        except:
            pass
        
        print(THEME['error'] + "ADB tidak ditemukan!")
        if self.confirm_action("Apakah Anda ingin menginstall ADB sekarang?"):
            self.install_adb()
            return self.detect_adb()  # Cek lagi setelah install
        else:
            print(THEME['error'] + "ADB diperlukan untuk menjalankan tool ini!")
            sys.exit(1)
    
    def detect_fastboot(self):
        """Deteksi lokasi Fastboot"""
        paths = {
            'windows': ['fastboot.exe', 'platform-tools\\fastboot.exe', os.path.join(os.environ.get('ProgramFiles', ''), 'Android\\android-sdk\\platform-tools\\fastboot.exe')],
            'linux': ['fastboot', '/usr/bin/fastboot', '/usr/local/bin/fastboot', os.path.expanduser('~/Android/Sdk/platform-tools/fastboot')],
            'android': ['fastboot', '/data/data/com.termux/files/usr/bin/fastboot']
        }
        
        for path in paths.get(self.platform, []):
            if os.path.exists(path):
                return path
        
        # Jika tidak ditemukan, coba cari di PATH
        try:
            subprocess.run(['fastboot', 'version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return 'fastboot'
        except:
            pass
        
        print(THEME['warning'] + "Fastboot tidak ditemukan. Beberapa fitur mungkin tidak tersedia.")
        return None
    
    def install_adb(self):
        """Install ADB secara otomatis"""
        print(THEME['info'] + "Menginstall ADB...")
        
        try:
            if self.platform == 'android':
                self.start_animation("Menginstall ADB di Termux...")
                subprocess.run(['pkg', 'install', 'android-tools', '-y'], check=True)
                self.stop_animation()
                print(THEME['success'] + "ADB berhasil diinstall di Termux!")
            elif self.platform == 'linux':
                self.start_animation("Menginstall ADB di Linux...")
                if os.path.exists('/etc/debian_version'):
                    subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                    subprocess.run(['sudo', 'apt-get', 'install', 'adb', 'fastboot', '-y'], check=True)
                elif os.path.exists('/etc/arch-release'):
                    subprocess.run(['sudo', 'pacman', '-S', 'android-tools', '--noconfirm'], check=True)
                elif os.path.exists('/etc/redhat-release'):
                    subprocess.run(['sudo', 'dnf', 'install', 'android-tools', '-y'], check=True)
                self.stop_animation()
                print(THEME['success'] + "ADB berhasil diinstall di Linux!")
            elif self.platform == 'windows':
                print(THEME['info'] + "Silakan download ADB secara manual dari:")
                print(THEME['info'] + "https://developer.android.com/studio/releases/platform-tools")
                print(THEME['info'] + "Ekstrak ke C:\\platform-tools dan tambahkan ke PATH")
                input(THEME['input'] + "Tekan Enter setelah selesai...")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal menginstall ADB: {str(e)}")
            sys.exit(1)
    
    def get_local_ip(self):
        """Dapatkan alamat IP lokal"""
        try:
            if self.platform == 'linux' or self.platform == 'android':
                # Untuk Linux/Android
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                return ip
            elif self.platform == 'windows':
                # Untuk Windows
                hostname = socket.gethostname()
                return socket.gethostbyname(hostname)
            else:
                return '127.0.0.1'
        except:
            return '127.0.0.1'
    
    def run_command(self, command, adb=False, fastboot=False, root=False, background=False):
        """Jalankan perintah ADB/Fastboot"""
        try:
            if adb and self.adb_path:
                full_command = [self.adb_path]
                if root:
                    full_command.append('root')
                full_command.extend(command.split())
            elif fastboot and self.fastboot_path:
                full_command = [self.fastboot_path]
                full_command.extend(command.split())
            else:
                full_command = command.split()
            
            if background:
                # Jalankan di background
                if self.platform == 'windows':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    process = subprocess.Popen(full_command, 
                                             stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE,
                                             stdin=subprocess.PIPE,
                                             startupinfo=startupinfo)
                else:
                    process = subprocess.Popen(full_command, 
                                             stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE,
                                             stdin=subprocess.PIPE,
                                             preexec_fn=os.setsid)
                return process
            else:
                # Jalankan dan tunggu hasilnya
                result = subprocess.run(full_command, 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE,
                                      text=True)
                return result
        except Exception as e:
            print(THEME['error'] + f"Error menjalankan perintah: {str(e)}")
            return None
    
    def start_animation(self, message):
        """Tampilkan animasi loading"""
        if self.animation_running:
            return
            
        self.animation_running = True
        anim = random.choice(ANIMATIONS)
        self.animation_thread = threading.Thread(target=self._animate, args=(anim, message), daemon=True)
        self.animation_thread.start()
    
    def _animate(self, anim, message):
        """Thread untuk animasi"""
        frame = 0
        while self.animation_running:
            sys.stdout.write(f"\r{THEME['special']}{anim[frame % len(anim)]} {THEME['info']}{message}")
            sys.stdout.flush()
            frame += 1
            time.sleep(0.1)
        sys.stdout.write("\r" + " "*(len(anim[0]) + len(message) + 2) + "\r")
        sys.stdout.flush()
    
    def stop_animation(self):
        """Hentikan animasi loading"""
        self.animation_running = False
        if self.animation_thread:
            self.animation_thread.join()
            self.animation_thread = None
    
    def confirm_action(self, message):
        """Konfirmasi aksi dengan user"""
        while True:
            response = input(THEME['input'] + f"{message} (y/n): ").lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print(THEME['warning'] + "Masukkan y atau n!")
    
    def connect_device(self):
        """Hubungkan ke perangkat Android"""
        print(THEME['title'] + "\n" + "="*70)
        print(f"{'MENU KONEKSI PERANGKAT':^70}")
        print("="*70 + Style.RESET_ALL)
        
        print("\n1. Koneksi via USB")
        print("2. Koneksi via WiFi")
        print("3. Koneksi via OTG")
        print("4. Kembali ke menu utama")
        
        choice = input(THEME['input'] + "\nPilih opsi [1-4]: ")
        
        if choice == '1':
            self.connect_usb()
        elif choice == '2':
            self.connect_wifi()
        elif choice == '3':
            self.connect_otg()
        elif choice == '4':
            return
        else:
            print(THEME['error'] + "Pilihan tidak valid!")
            time.sleep(1)
    
    def connect_usb(self):
        """Koneksi via USB"""
        print(THEME['info'] + "\nPastikan perangkat Android terhubung via USB dan USB debugging diaktifkan!")
        input(THEME['input'] + "Tekan Enter setelah siap...")
        
        self.start_animation("Mencari perangkat USB...")
        result = self.run_command('devices', adb=True)
        self.stop_animation()
        
        if result and result.stdout:
            devices = [line.split('\t')[0] for line in result.stdout.splitlines() if '\tdevice' in line]
            if devices:
                print(THEME['success'] + f"Perangkat terdeteksi: {', '.join(devices)}")
                self.current_device = devices[0]
                self.device_menu()
            else:
                print(THEME['error'] + "Tidak ada perangkat yang terdeteksi!")
                print(THEME['info'] + "Pastikan:")
                print("- USB debugging diaktifkan di pengembang")
                print("- Izin USB debugging diberikan")
                print("- Kabel USB dalam kondisi baik")
        else:
            print(THEME['error'] + "Gagal mendeteksi perangkat!")
    
    def connect_wifi(self):
        """Koneksi via WiFi"""
        print(THEME['info'] + "\nPastikan perangkat Android dan komputer dalam jaringan yang sama!")
        
        # Cek apakah sudah terkoneksi via USB terlebih dahulu
        self.start_animation("Memeriksa koneksi USB...")
        usb_result = self.run_command('devices', adb=True)
        self.stop_animation()
        
        usb_devices = [line.split('\t')[0] for line in usb_result.stdout.splitlines() if '\tdevice' in line] if usb_result else []
        
        if not usb_devices:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung via USB!")
            print(THEME['info'] + "Anda harus terhubung via USB terlebih dahulu untuk inisialisasi koneksi WiFi.")
            return
        
        print(THEME['success'] + f"Perangkat USB terdeteksi: {usb_devices[0]}")
        
        # Set perangkat ke mode TCPIP
        self.start_animation("Mengaktifkan koneksi WiFi...")
        tcpip_result = self.run_command(f'tcpip {self.server_port}', adb=True)
        self.stop_animation()
        
        if tcpip_result and tcpip_result.returncode == 0:
            print(THEME['success'] + f"Perangkat siap untuk koneksi WiFi di port {self.server_port}")
            
            # Dapatkan IP perangkat
            self.start_animation("Mendapatkan IP perangkat...")
            ip_result = self.run_command('shell ip route', adb=True)
            self.stop_animation()
            
            device_ip = None
            if ip_result and ip_result.stdout:
                # Parse output untuk mendapatkan IP
                match = re.search(r'src (\d+\.\d+\.\d+\.\d+)', ip_result.stdout)
                if match:
                    device_ip = match.group(1)
            
            if device_ip:
                print(THEME['success'] + f"IP perangkat: {device_ip}")
                
                # Hubungkan via WiFi
                self.start_animation(f"Menghubungkan ke {device_ip}...")
                connect_result = self.run_command(f'connect {device_ip}:{self.server_port}', adb=True)
                self.stop_animation()
                
                if connect_result and connect_result.returncode == 0:
                    print(THEME['success'] + f"Berhasil terhubung via WiFi ke {device_ip}")
                    self.current_device = f"{device_ip}:{self.server_port}"
                    self.device_menu()
                else:
                    print(THEME['error'] + "Gagal terhubung via WiFi!")
                    print(THEME['info'] + "Pastikan:")
                    print("- Perangkat dan komputer dalam jaringan yang sama")
                    print("- Port tidak diblokir firewall")
            else:
                print(THEME['error'] + "Gagal mendapatkan IP perangkat!")
        else:
            print(THEME['error'] + "Gagal mengaktifkan mode TCPIP!")
    
    def connect_otg(self):
        """Koneksi via OTG"""
        print(THEME['info'] + "\nFitur OTG memerlukan akses khusus dan konfigurasi perangkat!")
        
        if self.platform != 'android':
            print(THEME['warning'] + "Fitur OTG hanya tersedia di Termux (Android)!")
            return
        
        print(THEME['info'] + "Pastikan:")
        print("- Mode developer diaktifkan")
        print("- USB OTG diaktifkan")
        print("- Kabel OTG terhubung dengan baik")
        
        if not self.confirm_action("Lanjutkan koneksi OTG?"):
            return
        
        self.start_animation("Mengkonfigurasi OTG...")
        
        try:
            # Coba mengaktifkan OTG (mungkin memerlukan root)
            subprocess.run(['su', '-c', 'setprop persist.sys.usb.config otg'], check=True)
            time.sleep(2)
            
            # Cek perangkat yang terhubung
            result = subprocess.run(['lsusb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.stop_animation()
            
            if result.returncode == 0:
                print(THEME['success'] + "Perangkat OTG terdeteksi:")
                print(result.stdout)
                
                # Coba koneksi ADB via OTG
                self.start_animation("Mencoba koneksi ADB via OTG...")
                adb_result = self.run_command('devices', adb=True)
                self.stop_animation()
                
                if adb_result and adb_result.stdout:
                    devices = [line.split('\t')[0] for line in adb_result.stdout.splitlines() if '\tdevice' in line]
                    if devices:
                        print(THEME['success'] + f"Perangkat OTG terhubung: {devices[0]}")
                        self.current_device = devices[0]
                        self.device_menu()
                    else:
                        print(THEME['error'] + "Tidak ada perangkat ADB yang terdeteksi via OTG!")
                else:
                    print(THEME['error'] + "Gagal mendeteksi perangkat ADB via OTG!")
            else:
                print(THEME['error'] + "Gagal mendeteksi perangkat OTG!")
                print(THEME['info'] + "Pastikan kabel OTG terhubung dengan baik dan didukung.")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal mengkonfigurasi OTG: {str(e)}")
            print(THEME['info'] + "Mungkin diperlukan akses root untuk fitur ini.")
    
    def device_menu(self):
        """Menu utama setelah perangkat terhubung"""
        while True:
            print(THEME['title'] + "\n" + "="*70)
            print(f"{'MENU PERANGKAT':^70}")
            print(f"{'Perangkat: ' + (self.current_device if self.current_device else 'Tidak terhubung'):^70}")
            print("="*70 + Style.RESET_ALL)
            
            print("\n1. Informasi Perangkat")
            print("2. File Manager")
            print("3. Aplikasi Manager")
            print("4. Root Device")
            print("5. Unlock Bootloader")
            print("6. Custom Recovery")
            print("7. Backup & Restore")
            print("8. Eksekusi Perintah ADB")
            print("9. Putuskan Koneksi")
            print("0. Kembali ke Menu Utama")
            
            choice = input(THEME['input'] + "\nPilih opsi [0-9]: ")
            
            if choice == '1':
                self.device_info()
            elif choice == '2':
                self.file_manager()
            elif choice == '3':
                self.app_manager()
            elif choice == '4':
                self.root_device()
            elif choice == '5':
                self.unlock_bootloader()
            elif choice == '6':
                self.custom_recovery()
            elif choice == '7':
                self.backup_restore()
            elif choice == '8':
                self.adb_shell()
            elif choice == '9':
                self.disconnect_device()
                break
            elif choice == '0':
                self.disconnect_device()
                return
            else:
                print(THEME['error'] + "Pilihan tidak valid!")
                time.sleep(1)
    
    def device_info(self):
        """Tampilkan informasi perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        self.start_animation("Mengambil informasi perangkat...")
        
        try:
            # Informasi dasar
            model = self.run_command('shell getprop ro.product.model', adb=True).stdout.strip()
            brand = self.run_command('shell getprop ro.product.brand', adb=True).stdout.strip()
            device = self.run_command('shell getprop ro.product.device', adb=True).stdout.strip()
            android_version = self.run_command('shell getprop ro.build.version.release', adb=True).stdout.strip()
            sdk_version = self.run_command('shell getprop ro.build.version.sdk', adb=True).stdout.strip()
            build_id = self.run_command('shell getprop ro.build.id', adb=True).stdout.strip()
            security_patch = self.run_command('shell getprop ro.build.version.security_patch', adb=True).stdout.strip()
            serialno = self.run_command('shell getprop ro.serialno', adb=True).stdout.strip()
            cpu = self.run_command('shell getprop ro.product.cpu.abi', adb=True).stdout.strip()
            ram = self.run_command('shell cat /proc/meminfo | grep MemTotal', adb=True).stdout.strip()
            storage = self.run_command('shell df -h /data', adb=True).stdout.splitlines()[1] if self.platform != 'windows' else "N/A"
            battery = self.run_command('shell dumpsys battery', adb=True).stdout.strip()
            
            self.stop_animation()
            
            # Tampilkan informasi
            print(THEME['title'] + "\n" + "="*70)
            print(f"{'INFORMASI PERANGKAT':^70}")
            print("="*70 + Style.RESET_ALL)
            
            print(f"\n{THEME['menu']}Model:{Style.RESET_ALL} {model}")
            print(f"{THEME['menu']}Merek:{Style.RESET_ALL} {brand}")
            print(f"{THEME['menu']}Device:{Style.RESET_ALL} {device}")
            print(f"{THEME['menu']}Android:{Style.RESET_ALL} {android_version} (SDK {sdk_version})")
            print(f"{THEME['menu']}Build ID:{Style.RESET_ALL} {build_id}")
            print(f"{THEME['menu']}Patch Keamanan:{Style.RESET_ALL} {security_patch}")
            print(f"{THEME['menu']}Serial Number:{Style.RESET_ALL} {serialno}")
            print(f"{THEME['menu']}CPU:{Style.RESET_ALL} {cpu}")
            print(f"{THEME['menu']}RAM:{Style.RESET_ALL} {ram.split()[1]} {ram.split()[2]}")
            print(f"{THEME['menu']}Penyimpanan:{Style.RESET_ALL} {storage}")
            
            # Informasi baterai
            if 'level' in battery:
                level = re.search(r'level: (\d+)', battery).group(1)
                status = re.search(r'status: (\d+)', battery).group(1)
                status_text = "Charging" if status == '2' else "Discharging" if status == '3' else "Full" if status == '5' else "Unknown"
                print(f"{THEME['menu']}Baterai:{Style.RESET_ALL} {level}% ({status_text})")
            
            # Informasi tambahan
            print(f"\n{THEME['menu']}Kernel:{Style.RESET_ALL}")
            kernel = self.run_command('shell uname -a', adb=True).stdout.strip()
            print(kernel)
            
            print(f"\n{THEME['menu']}CPU Info:{Style.RESET_ALL}")
            cpuinfo = self.run_command('shell cat /proc/cpuinfo', adb=True).stdout.strip()[:500] + "..."
            print(cpuinfo)
            
            input(THEME['input'] + "\nTekan Enter untuk kembali...")
            
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal mendapatkan informasi perangkat: {str(e)}")
    
    def file_manager(self):
        """Manajemen file di perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        current_path = "/sdcard/"
        
        while True:
            self.start_animation(f"Mengambil daftar file di {current_path}...")
            ls_result = self.run_command(f'shell ls -la "{current_path}"', adb=True)
            self.stop_animation()
            
            if ls_result and ls_result.returncode == 0:
                files = ls_result.stdout.splitlines()
                
                print(THEME['title'] + "\n" + "="*70)
                print(f"{'FILE MANAGER':^70}")
                print(f"{'Path: ' + current_path:^70}")
                print("="*70 + Style.RESET_ALL)
                
                # Tampilkan daftar file
                for i, file in enumerate(files[:20], 1):
                    print(f"{i}. {file}")
                
                if len(files) > 20:
                    print(THEME['info'] + f"\nMenampilkan 20 dari {len(files)} item...")
                
                print("\nOpsi:")
                print("n. Masuk ke direktori")
                print("p. Kembali ke direktori sebelumnya")
                print("u. Upload file")
                print("d. Download file")
                print("r. Hapus file")
                print("m. Buat direktori")
                print("0. Kembali")
                
                choice = input(THEME['input'] + "\nPilih opsi: ")
                
                if choice == '0':
                    break
                elif choice == 'n':
                    dir_name = input(THEME['input'] + "Masukkan nama direktori: ")
                    if dir_name:
                        new_path = os.path.join(current_path, dir_name)
                        test_result = self.run_command(f'shell ls "{new_path}"', adb=True)
                        if test_result and test_result.returncode == 0:
                            current_path = new_path + ("/" if not new_path.endswith("/") else "")
                        else:
                            print(THEME['error'] + "Direktori tidak valid atau tidak dapat diakses!")
                elif choice == 'p':
                    if current_path != "/":
                        current_path = os.path.dirname(current_path[:-1]) + "/"
                elif choice == 'u':
                    self.upload_file(current_path)
                elif choice == 'd':
                    self.download_file(current_path)
                elif choice == 'r':
                    self.delete_file(current_path)
                elif choice == 'm':
                    self.create_directory(current_path)
                else:
                    try:
                        selected = int(choice) - 1
                        if 0 <= selected < len(files):
                            selected_file = files[selected].split()[-1]
                            if files[selected].startswith('d'):
                                current_path = os.path.join(current_path, selected_file) + "/"
                    except ValueError:
                        print(THEME['error'] + "Pilihan tidak valid!")
            else:
                print(THEME['error'] + "Gagal mendapatkan daftar file!")
                break
    
    def upload_file(self, remote_path):
        """Upload file ke perangkat"""
        if self.platform == 'android':
            print(THEME['warning'] + "Upload file dari Termux mungkin terbatas.")
        
        local_file = input(THEME['input'] + "Masukkan path file lokal: ")
        remote_file = input(THEME['input'] + f"Masukkan nama file tujuan [{remote_path}]: ") or os.path.join(remote_path, os.path.basename(local_file))
        
        if not os.path.exists(local_file):
            print(THEME['error'] + "File lokal tidak ditemukan!")
            return
        
        self.start_animation(f"Mengupload {local_file} ke {remote_file}...")
        push_result = self.run_command(f'push "{local_file}" "{remote_file}"', adb=True)
        self.stop_animation()
        
        if push_result and push_result.returncode == 0:
            print(THEME['success'] + "File berhasil diupload!")
        else:
            print(THEME['error'] + "Gagal mengupload file!")
    
    def download_file(self, remote_path):
        """Download file dari perangkat"""
        remote_file = input(THEME['input'] + f"Masukkan nama file di perangkat [{remote_path}]: ")
        local_file = input(THEME['input'] + "Masukkan path tujuan lokal: ") or os.path.basename(remote_file)
        
        self.start_animation(f"Mendownload {remote_file} ke {local_file}...")
        pull_result = self.run_command(f'pull "{remote_file}" "{local_file}"', adb=True)
        self.stop_animation()
        
        if pull_result and pull_result.returncode == 0:
            print(THEME['success'] + "File berhasil didownload!")
        else:
            print(THEME['error'] + "Gagal mendownload file!")
    
    def delete_file(self, remote_path):
        """Hapus file di perangkat"""
        remote_file = input(THEME['input'] + f"Masukkan nama file yang akan dihapus [{remote_path}]: ")
        
        if not self.confirm_action(f"Yakin ingin menghapus {remote_file}?"):
            return
        
        self.start_animation(f"Menghapus {remote_file}...")
        rm_result = self.run_command(f'shell rm -rf "{remote_file}"', adb=True)
        self.stop_animation()
        
        if rm_result and rm_result.returncode == 0:
            print(THEME['success'] + "File berhasil dihapus!")
        else:
            print(THEME['error'] + "Gagal menghapus file!")
    
    def create_directory(self, remote_path):
        """Buat direktori di perangkat"""
        dir_name = input(THEME['input'] + "Masukkan nama direktori: ")
        
        self.start_animation(f"Membuat direktori {dir_name}...")
        mkdir_result = self.run_command(f'shell mkdir "{os.path.join(remote_path, dir_name)}"', adb=True)
        self.stop_animation()
        
        if mkdir_result and mkdir_result.returncode == 0:
            print(THEME['success'] + "Direktori berhasil dibuat!")
        else:
            print(THEME['error'] + "Gagal membuat direktori!")
    
    def app_manager(self):
        """Manajemen aplikasi di perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        while True:
            print(THEME['title'] + "\n" + "="*70)
            print(f"{'APLIKASI MANAGER':^70}")
            print("="*70 + Style.RESET_ALL)
            
            print("\n1. Daftar Aplikasi Terinstall")
            print("2. Install Aplikasi (APK)")
            print("3. Uninstall Aplikasi")
            print("4. Backup Aplikasi")
            print("5. Restore Aplikasi")
            print("6. Matikan Aplikasi")
            print("7. Hidupkan Aplikasi")
            print("8. Hapus Cache Aplikasi")
            print("9. Hapus Data Aplikasi")
            print("0. Kembali")
            
            choice = input(THEME['input'] + "\nPilih opsi [0-9]: ")
            
            if choice == '1':
                self.list_apps()
            elif choice == '2':
                self.install_app()
            elif choice == '3':
                self.uninstall_app()
            elif choice == '4':
                self.backup_app()
            elif choice == '5':
                self.restore_app()
            elif choice == '6':
                self.disable_app()
            elif choice == '7':
                self.enable_app()
            elif choice == '8':
                self.clear_app_cache()
            elif choice == '9':
                self.clear_app_data()
            elif choice == '0':
                break
            else:
                print(THEME['error'] + "Pilihan tidak valid!")
                time.sleep(1)
    
    def list_apps(self):
        """Daftar aplikasi yang terinstall"""
        self.start_animation("Mendapatkan daftar aplikasi...")
        result = self.run_command('shell pm list packages -f', adb=True)
        self.stop_animation()
        
        if result and result.returncode == 0:
            apps = result.stdout.splitlines()
            
            print(THEME['title'] + "\n" + "="*70)
            print(f"{'DAFTAR APLIKASI':^70}")
            print("="*70 + Style.RESET_ALL)
            
            # Tampilkan aplikasi dengan format yang lebih baik
            for i, app in enumerate(apps[:50], 1):
                # Format: package:/path/to/apk=com.example.app
                parts = app.split('=')
                if len(parts) == 2:
                    apk_path = parts[0].replace('package:', '')
                    package_name = parts[1]
                    print(f"{i}. {package_name}")
                    print(f"   {apk_path}")
            
            if len(apps) > 50:
                print(THEME['info'] + f"\nMenampilkan 50 dari {len(apps)} aplikasi...")
            
            input(THEME['input'] + "\nTekan Enter untuk kembali...")
        else:
            print(THEME['error'] + "Gagal mendapatkan daftar aplikasi!")
    
    def install_app(self):
        """Install aplikasi dari APK"""
        if self.platform == 'android':
            print(THEME['warning'] + "Install APK dari Termux mungkin terbatas.")
        
        apk_file = input(THEME['input'] + "Masukkan path file APK: ")
        
        if not os.path.exists(apk_file):
            print(THEME['error'] + "File APK tidak ditemukan!")
            return
        
        self.start_animation(f"Menginstall {apk_file}...")
        install_result = self.run_command(f'install "{apk_file}"', adb=True)
        self.stop_animation()
        
        if install_result and install_result.returncode == 0:
            print(THEME['success'] + "Aplikasi berhasil diinstall!")
        else:
            print(THEME['error'] + "Gagal menginstall aplikasi!")
            if install_result and install_result.stderr:
                print(THEME['error'] + install_result.stderr)
    
    def uninstall_app(self):
        """Uninstall aplikasi"""
        package_name = input(THEME['input'] + "Masukkan nama package aplikasi: ")
        
        if not self.confirm_action(f"Yakin ingin uninstall {package_name}?"):
            return
        
        keep_data = self.confirm_action("Simpan data aplikasi?") if self.confirm_action("Pertahankan data?") else ""
        
        self.start_animation(f"Menghapus {package_name}...")
        if keep_data:
            uninstall_result = self.run_command(f'uninstall -k {package_name}', adb=True)
        else:
            uninstall_result = self.run_command(f'uninstall {package_name}', adb=True)
        self.stop_animation()
        
        if uninstall_result and uninstall_result.returncode == 0:
            print(THEME['success'] + "Aplikasi berhasil diuninstall!")
        else:
            print(THEME['error'] + "Gagal menguninstall aplikasi!")
            if uninstall_result and uninstall_result.stderr:
                print(THEME['error'] + uninstall_result.stderr)
    
    def backup_app(self):
        """Backup aplikasi ke file APK"""
        package_name = input(THEME['input'] + "Masukkan nama package aplikasi: ")
        output_file = input(THEME['input'] + "Masukkan nama file output [backup.apk]: ") or "backup.apk"
        
        self.start_animation(f"Membackup {package_name} ke {output_file}...")
        
        # Dapatkan path APK
        path_result = self.run_command(f'shell pm path {package_name}', adb=True)
        if path_result and path_result.returncode == 0:
            apk_path = path_result.stdout.strip().replace('package:', '')
            
            # Download APK
            pull_result = self.run_command(f'pull "{apk_path}" "{output_file}"', adb=True)
            self.stop_animation()
            
            if pull_result and pull_result.returncode == 0:
                print(THEME['success'] + f"Aplikasi berhasil dibackup ke {output_file}!")
            else:
                print(THEME['error'] + "Gagal mendownload APK!")
        else:
            self.stop_animation()
            print(THEME['error'] + "Gagal mendapatkan path APK!")
    
    def restore_app(self):
        """Restore aplikasi dari backup"""
        apk_file = input(THEME['input'] + "Masukkan path file APK backup: ")
        
        if not os.path.exists(apk_file):
            print(THEME['error'] + "File APK tidak ditemukan!")
            return
        
        self.install_app(apk_file)
    
    def disable_app(self):
        """Nonaktifkan aplikasi sistem"""
        package_name = input(THEME['input'] + "Masukkan nama package aplikasi: ")
        
        if not self.confirm_action(f"Yakin ingin menonaktifkan {package_name}?"):
            return
        
        self.start_animation(f"Menonaktifkan {package_name}...")
        disable_result = self.run_command(f'shell pm disable-user {package_name}', adb=True)
        self.stop_animation()
        
        if disable_result and disable_result.returncode == 0:
            print(THEME['success'] + "Aplikasi berhasil dinonaktifkan!")
        else:
            print(THEME['error'] + "Gagal menonaktifkan aplikasi!")
            if disable_result and disable_result.stderr:
                print(THEME['error'] + disable_result.stderr)
    
    def enable_app(self):
        """Aktifkan aplikasi sistem"""
        package_name = input(THEME['input'] + "Masukkan nama package aplikasi: ")
        
        self.start_animation(f"Mengaktifkan {package_name}...")
        enable_result = self.run_command(f'shell pm enable {package_name}', adb=True)
        self.stop_animation()
        
        if enable_result and enable_result.returncode == 0:
            print(THEME['success'] + "Aplikasi berhasil diaktifkan!")
        else:
            print(THEME['error'] + "Gagal mengaktifkan aplikasi!")
            if enable_result and enable_result.stderr:
                print(THEME['error'] + enable_result.stderr)
    
    def clear_app_cache(self):
        """Hapus cache aplikasi"""
        package_name = input(THEME['input'] + "Masukkan nama package aplikasi: ")
        
        self.start_animation(f"Menghapus cache {package_name}...")
        clear_result = self.run_command(f'shell pm clear {package_name}', adb=True)
        self.stop_animation()
        
        if clear_result and clear_result.returncode == 0:
            print(THEME['success'] + "Cache aplikasi berhasil dihapus!")
        else:
            print(THEME['error'] + "Gagal menghapus cache aplikasi!")
            if clear_result and clear_result.stderr:
                print(THEME['error'] + clear_result.stderr)
    
    def clear_app_data(self):
        """Hapus data aplikasi"""
        package_name = input(THEME['input'] + "Masukkan nama package aplikasi: ")
        
        if not self.confirm_action(f"Yakin ingin menghapus semua data {package_name}?"):
            return
        
        self.start_animation(f"Menghapus data {package_name}...")
        clear_result = self.run_command(f'shell pm clear {package_name}', adb=True)
        self.stop_animation()
        
        if clear_result and clear_result.returncode == 0:
            print(THEME['success'] + "Data aplikasi berhasil dihapus!")
        else:
            print(THEME['error'] + "Gagal menghapus data aplikasi!")
            if clear_result and clear_result.stderr:
                print(THEME['error'] + clear_result.stderr)
    
    def root_device(self):
        """Root perangkat Android"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['warning'] + "\nPERINGATAN: Proses rooting dapat:")
        print("- Membatalkan garansi perangkat")
        print("- Menyebabkan kehilangan data")
        print("- Membuat perangkat tidak stabil")
        print("- Bahkan merusak perangkat jika tidak dilakukan dengan benar!")
        
        if not self.confirm_action("Apakah Anda yakin ingin melanjutkan proses rooting?"):
            return
        
        # Cek apakah perangkat sudah di-root
        self.start_animation("Memeriksa status root...")
        root_check = self.run_command('shell su -c id', adb=True)
        self.stop_animation()
        
        if root_check and 'uid=0' in root_check.stdout:
            print(THEME['success'] + "Perangkat sudah di-root!")
            return
        
        # Dapatkan informasi perangkat untuk menentukan metode rooting
        self.start_animation("Menganalisis perangkat...")
        brand = self.run_command('shell getprop ro.product.brand', adb=True).stdout.strip().lower()
        model = self.run_command('shell getprop ro.product.model', adb=True).stdout.strip().lower()
        android_version = self.run_command('shell getprop ro.build.version.release', adb=True).stdout.strip()
        self.stop_animation()
        
        print(THEME['info'] + f"\nInformasi Perangkat:")
        print(f"- Merek: {brand}")
        print(f"- Model: {model}")
        print(f"- Android: {android_version}")
        
        # Tentukan metode rooting berdasarkan perangkat
        method = None
        if 'samsung' in brand:
            method = "Odin + CF-Auto-Root atau TWRP + Magisk"
        elif 'xiaomi' in brand or 'redmi' in brand or 'poco' in brand:
            method = "Unlock bootloader + TWRP + Magisk"
        elif 'oneplus' in brand:
            method = "Unlock bootloader + TWRP + Magisk"
        elif 'huawei' in brand or 'honor' in brand:
            method = "Unlock bootloader (mungkin sulit) + TWRP + Magisk"
        else:
            method = "TWRP + Magisk atau Patch boot image dengan Magisk"
        
        print(THEME['info'] + f"\nMetode rooting yang disarankan: {method}")
        
        # Proses rooting
        if self.confirm_action("Apakah Anda ingin mencoba rooting otomatis?"):
            self.start_animation("Mempersiapkan proses rooting...")
            
            try:
                # Langkah 1: Unlock bootloader jika diperlukan
                if self.confirm_action("Apakah Anda ingin mencoba unlock bootloader terlebih dahulu?"):
                    self.unlock_bootloader()
                
                # Langkah 2: Download tools yang diperlukan
                print(THEME['info'] + "\nMendownload tools rooting...")
                self.download_root_tools()
                
                # Langkah 3: Reboot ke fastboot/bootloader
                print(THEME['info'] + "\nReboot ke fastboot...")
                self.run_command('reboot bootloader', adb=True)
                time.sleep(10)
                
                # Langkah 4: Flash custom recovery (TWRP)
                if self.fastboot_path:
                    print(THEME['info'] + "\nMencoba flash TWRP...")
                    twrp_img = "twrp.img"  # Ini harus disesuaikan dengan file TWRP yang benar untuk perangkat
                    flash_result = self.run_command(f'flash recovery {twrp_img}', fastboot=True)
                    
                    if flash_result and flash_result.returncode == 0:
                        print(THEME['success'] + "TWRP berhasil di-flash!")
                        
                        # Langkah 5: Boot ke recovery
                        print(THEME['info'] + "\nBooting ke TWRP...")
                        self.run_command('boot recovery', fastboot=True)
                        time.sleep(20)
                        
                        # Langkah 6: Install Magisk
                        print(THEME['info'] + "\nMenginstall Magisk...")
                        magisk_zip = "Magisk-v25.2.zip"  # Versi terbaru Magisk
                        push_result = self.run_command(f'push {magisk_zip} /sdcard/', adb=True)
                        
                        if push_result and push_result.returncode == 0:
                            print(THEME['success'] + "Magisk berhasil di-copy ke perangkat!")
                            print(THEME['info'] + "Silakan install Magisk secara manual dari TWRP:")
                            print(THEME['info'] + "1. Pilih Install")
                            print(THEME['info'] + "2. Pilih file Magisk.zip")
                            print(THEME['info'] + "3. Swipe untuk menginstall")
                            print(THEME['info'] + "4. Reboot sistem")
                            
                            input(THEME['input'] + "\nSetelah selesai, tekan Enter untuk melanjutkan...")
                            
                            # Verifikasi root
                            root_check = self.run_command('shell su -c id', adb=True)
                            if root_check and 'uid=0' in root_check.stdout:
                                print(THEME['success'] + "Perangkat berhasil di-root!")
                            else:
                                print(THEME['warning'] + "Root tidak terdeteksi. Mungkin perlu konfigurasi manual.")
                        else:
                            print(THEME['error'] + "Gagal meng-copy Magisk ke perangkat!")
                    else:
                        print(THEME['error'] + "Gagal flash TWRP!")
                else:
                    print(THEME['error'] + "Fastboot tidak tersedia untuk proses ini!")
            except Exception as e:
                print(THEME['error'] + f"Error selama proses rooting: {str(e)}")
            finally:
                self.stop_animation()
        else:
            print(THEME['info'] + "\nAnda dapat mencoba rooting manual dengan panduan online.")
    
    def download_root_tools(self):
        """Download tools rooting (TWRP, Magisk)"""
        try:
            # Buat direktori tools jika belum ada
            if not os.path.exists('root_tools'):
                os.makedirs('root_tools')
            
            # Download Magisk
            magisk_url = "https://github.com/topjohnwu/Magisk/releases/download/v25.2/Magisk-v25.2.apk"
            print(THEME['info'] + f"Mendownload Magisk dari {magisk_url}...")
            urllib.request.urlretrieve(magisk_url, 'root_tools/Magisk-v25.2.apk')
            
            print(THEME['success'] + "Magisk berhasil didownload!")
            
            # Catatan: Tidak bisa otomatis download TWRP karena spesifik perangkat
            print(THEME['warning'] + "\nSilakan download TWRP yang sesuai untuk perangkat Anda secara manual:")
            print(THEME['warning'] + "Kunjungi https://twrp.me dan cari untuk model perangkat Anda")
            print(THEME['warning'] + "Simpan file img-nya di folder root_tools dengan nama twrp.img")
            
            input(THEME['input'] + "\nTekan Enter setelah selesai download TWRP...")
            
            if os.path.exists('root_tools/twrp.img'):
                print(THEME['success'] + "TWRP berhasil ditemukan!")
            else:
                print(THEME['error'] + "TWRP tidak ditemukan! Proses rooting mungkin gagal.")
        except Exception as e:
            print(THEME['error'] + f"Gagal mendownload tools rooting: {str(e)}")
    
    def unlock_bootloader(self):
        """Unlock bootloader perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['warning'] + "\nPERINGATAN: Unlock bootloader dapat:")
        print("- Membatalkan garansi perangkat")
        print("- Menghapus semua data di perangkat (factory reset)")
        print("- Membuat perangkat tidak stabil")
        
        if not self.confirm_action("Apakah Anda yakin ingin melanjutkan unlock bootloader?"):
            return
        
        # Cek apakah bootloader sudah di-unlock
        self.start_animation("Memeriksa status bootloader...")
        if self.fastboot_path:
            oem_result = self.run_command('oem device-info', fastboot=True)
            self.stop_animation()
            
            if oem_result and 'Device unlocked: true' in oem_result.stdout:
                print(THEME['success'] + "Bootloader sudah di-unlock!")
                return
            elif oem_result and 'Device unlocked: false' in oem_result.stdout:
                print(THEME['info'] + "Bootloader terkunci. Mencoba unlock...")
            else:
                print(THEME['warning'] + "Tidak dapat menentukan status bootloader. Mencoba lanjut...")
        else:
            self.stop_animation()
            print(THEME['error'] + "Fastboot tidak tersedia!")
            return
        
        # Reboot ke fastboot
        print(THEME['info'] + "\nReboot ke fastboot...")
        self.run_command('reboot bootloader', adb=True)
        time.sleep(10)
        
        # Coba unlock bootloader
        print(THEME['info'] + "\nMencoba unlock bootloader...")
        unlock_result = self.run_command('flashing unlock', fastboot=True)
        
        if unlock_result and unlock_result.returncode == 0:
            print(THEME['success'] + "Perintah unlock berhasil dikirim!")
            print(THEME['info'] + "Silakan konfirmasi di layar perangkat Anda (jika ada)")
            print(THEME['info'] + "Setelah selesai, perangkat akan melakukan factory reset")
            
            input(THEME['input'] + "\nTekan Enter setelah proses selesai...")
            
            # Verifikasi unlock
            print(THEME['info'] + "\nMemverifikasi status bootloader...")
            oem_result = self.run_command('oem device-info', fastboot=True)
            
            if oem_result and 'Device unlocked: true' in oem_result.stdout:
                print(THEME['success'] + "Bootloader berhasil di-unlock!")
            else:
                print(THEME['warning'] + "Bootloader mungkin masih terkunci. Coba manual jika diperlukan.")
        else:
            print(THEME['error'] + "Gagal mengirim perintah unlock!")
            if unlock_result and unlock_result.stderr:
                print(THEME['error'] + unlock_result.stderr)
        
        # Reboot kembali ke sistem
        print(THEME['info'] + "\nReboot ke sistem...")
        self.run_command('reboot', fastboot=True)
        time.sleep(20)
    
    def custom_recovery(self):
        """Install custom recovery (TWRP)"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['warning'] + "\nPERINGATAN: Install custom recovery dapat:")
        print("- Membatalkan garansi perangkat")
        print("- Menyebabkan masalah boot jika tidak kompatibel")
        print("- Membutuhkan bootloader yang sudah di-unlock")
        
        if not self.confirm_action("Apakah Anda yakin ingin melanjutkan install custom recovery?"):
            return
        
        # Cek bootloader status
        self.start_animation("Memeriksa status bootloader...")
        if self.fastboot_path:
            oem_result = self.run_command('oem device-info', fastboot=True)
            self.stop_animation()
            
            if oem_result and 'Device unlocked: false' in oem_result.stdout:
                print(THEME['error'] + "Bootloader masih terkunci! Unlock terlebih dahulu.")
                if self.confirm_action("Apakah Anda ingin mencoba unlock bootloader sekarang?"):
                    self.unlock_bootloader()
                else:
                    return
            elif not oem_result:
                print(THEME['warning'] + "Tidak dapat memeriksa status bootloader. Lanjut dengan hati-hati!")
        else:
            self.stop_animation()
            print(THEME['error'] + "Fastboot tidak tersedia!")
            return
        
        # Download TWRP jika belum ada
        if not os.path.exists('root_tools/twrp.img'):
            print(THEME['info'] + "\nSilakan download TWRP yang sesuai untuk perangkat Anda:")
            print(THEME['info'] + "Kunjungi https://twrp.me dan cari untuk model perangkat Anda")
            print(THEME['info'] + "Simpan file img-nya di folder root_tools dengan nama twrp.img")
            
            input(THEME['input'] + "\nTekan Enter setelah selesai download TWRP...")
            
            if not os.path.exists('root_tools/twrp.img'):
                print(THEME['error'] + "File TWRP tidak ditemukan!")
                return
        
        # Reboot ke fastboot
        print(THEME['info'] + "\nReboot ke fastboot...")
        self.run_command('reboot bootloader', adb=True)
        time.sleep(10)
        
        # Flash recovery
        print(THEME['info'] + "\nFlashing TWRP...")
        flash_result = self.run_command(f'flash recovery root_tools/twrp.img', fastboot=True)
        
        if flash_result and flash_result.returncode == 0:
            print(THEME['success'] + "TWRP berhasil di-flash!")
            
            # Reboot ke recovery untuk verifikasi
            if self.confirm_action("Apakah Anda ingin langsung boot ke TWRP sekarang?"):
                print(THEME['info'] + "\nBooting ke TWRP...")
                self.run_command('boot recovery', fastboot=True)
                print(THEME['info'] + "Perangkat akan boot ke TWRP. Verifikasi instalasi.")
        else:
            print(THEME['error'] + "Gagal flash TWRP!")
            if flash_result and flash_result.stderr:
                print(THEME['error'] + flash_result.stderr)
        
        # Reboot kembali ke sistem jika tidak boot ke recovery
        if not self.confirm_action("Apakah Anda ingin tetap di fastboot?"):
            print(THEME['info'] + "\nReboot ke sistem...")
            self.run_command('reboot', fastboot=True)
            time.sleep(10)
    
    def backup_restore(self):
        """Backup dan restore perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        while True:
            print(THEME['title'] + "\n" + "="*70)
            print(f"{'BACKUP & RESTORE':^70}")
            print("="*70 + Style.RESET_ALL)
            
            print("\n1. Backup Partisi Sistem")
            print("2. Backup Data Pengguna")
            print("3. Backup Lengkap (Sistem + Data)")
            print("4. Restore Backup")
            print("5. Buat Flashable ZIP")
            print("0. Kembali")
            
            choice = input(THEME['input'] + "\nPilih opsi [0-5]: ")
            
            if choice == '1':
                self.backup_partition('system')
            elif choice == '2':
                self.backup_partition('data')
            elif choice == '3':
                self.full_backup()
            elif choice == '4':
                self.restore_backup()
            elif choice == '5':
                self.create_flashable_zip()
            elif choice == '0':
                break
            else:
                print(THEME['error'] + "Pilihan tidak valid!")
                time.sleep(1)
    
    def backup_partition(self, partition):
        """Backup partisi tertentu"""
        backup_name = input(THEME['input'] + f"Masukkan nama backup [{partition}_backup]: ") or f"{partition}_backup"
        
        print(THEME['warning'] + f"\nPERINGATAN: Backup partisi {partition} dapat:")
        print("- Membutuhkan ruang penyimpanan yang besar")
        print("- Membutuhkan waktu yang lama")
        print("- Membutuhkan akses root untuk beberapa partisi")
        
        if not self.confirm_action(f"Apakah Anda yakin ingin membackup partisi {partition}?"):
            return
        
        self.start_animation(f"Membackup partisi {partition}...")
        
        try:
            # Buat direktori backup jika belum ada
            if not os.path.exists('backups'):
                os.makedirs('backups')
            
            # Dapatkan blok partisi
            blk_result = self.run_command(f'shell ls -l /dev/block/by-name/{partition}', adb=True, root=True)
            if blk_result and '->' in blk_result.stdout:
                blk_path = blk_result.stdout.split('->')[-1].strip()
                
                # Backup menggunakan dd
                backup_cmd = f'shell su -c "dd if={blk_path} bs=4M | gzip -c" > backups/{backup_name}.img.gz'
                backup_process = self.run_command(backup_cmd, adb=True, background=True)
                
                # Tampilkan progress
                while backup_process.poll() is None:
                    size = os.path.getsize(f'backups/{backup_name}.img.gz') / (1024*1024)
                    sys.stdout.write(f"\r{THEME['info']}Progress: {size:.2f} MB")
                    sys.stdout.flush()
                    time.sleep(1)
                
                self.stop_animation()
                print(THEME['success'] + f"\nBackup partisi {partition} berhasil disimpan di backups/{backup_name}.img.gz!")
            else:
                self.stop_animation()
                print(THEME['error'] + f"Tidak dapat menemukan partisi {partition}!")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal membackup partisi {partition}: {str(e)}")
    
    def full_backup(self):
        """Backup lengkap sistem dan data"""
        backup_name = input(THEME['input'] + "Masukkan nama backup [full_backup]: ") or "full_backup"
        
        print(THEME['warning'] + "\nPERINGATAN: Backup lengkap dapat:")
        print("- Membutuhkan ruang penyimpanan yang sangat besar")
        print("- Membutuhkan waktu yang sangat lama")
        print("- Membutuhkan akses root")
        
        if not self.confirm_action("Apakah Anda yakin ingin membackup lengkap?"):
            return
        
        self.start_animation("Membackup sistem dan data...")
        
        try:
            # Buat direktori backup jika belum ada
            if not os.path.exists('backups'):
                os.makedirs('backups')
            
            # Backup sistem
            sys_blk = self.run_command('shell ls -l /dev/block/by-name/system', adb=True, root=True)
            if sys_blk and '->' in sys_blk.stdout:
                sys_path = sys_blk.stdout.split('->')[-1].strip()
                sys_cmd = f'shell su -c "dd if={sys_path} bs=4M | gzip -c" > backups/{backup_name}_system.img.gz'
                sys_process = self.run_command(sys_cmd, adb=True, background=True)
            
            # Backup data
            data_blk = self.run_command('shell ls -l /dev/block/by-name/userdata', adb=True, root=True)
            if data_blk and '->' in data_blk.stdout:
                data_path = data_blk.stdout.split('->')[-1].strip()
                data_cmd = f'shell su -c "dd if={data_path} bs=4M | gzip -c" > backups/{backup_name}_data.img.gz'
                data_process = self.run_command(data_cmd, adb=True, background=True)
            
            # Tampilkan progress
            while (sys_process.poll() is None if 'sys_process' in locals() else False) or \
                  (data_process.poll() is None if 'data_process' in locals() else False):
                sys_size = os.path.getsize(f'backups/{backup_name}_system.img.gz') / (1024*1024) if 'sys_process' in locals() else 0
                data_size = os.path.getsize(f'backups/{backup_name}_data.img.gz') / (1024*1024) if 'data_process' in locals() else 0
                sys.stdout.write(f"\r{THEME['info']}Progress: System {sys_size:.2f} MB | Data {data_size:.2f} MB")
                sys.stdout.flush()
                time.sleep(1)
            
            self.stop_animation()
            print(THEME['success'] + f"\nBackup lengkap berhasil disimpan di backups/{backup_name}_[system|data].img.gz!")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal membackup lengkap: {str(e)}")
    
    def restore_backup(self):
        """Restore backup partisi"""
        backup_file = input(THEME['input'] + "Masukkan path file backup: ")
        partition = input(THEME['input'] + "Masukkan nama partisi yang akan direstore (system/data): ").lower()
        
        if not os.path.exists(backup_file):
            print(THEME['error'] + "File backup tidak ditemukan!")
            return
        
        if partition not in ['system', 'data']:
            print(THEME['error'] + "Partisi harus system atau data!")
            return
        
        print(THEME['warning'] + f"\nPERINGATAN: Restore partisi {partition} dapat:")
        print("- Menyebabkan kehilangan data")
        print("- Membuat perangkat tidak bisa boot jika gagal")
        print("- Membutuhkan akses root")
        
        if not self.confirm_action(f"Apakah Anda yakin ingin merestore {partition} dari backup?"):
            return
        
        self.start_animation(f"Merestore partisi {partition}...")
        
        try:
            # Dapatkan blok partisi
            blk_result = self.run_command(f'shell ls -l /dev/block/by-name/{partition}', adb=True, root=True)
            if blk_result and '->' in blk_result.stdout:
                blk_path = blk_result.stdout.split('->')[-1].strip()
                
                # Restore menggunakan dd
                restore_cmd = f'gunzip -c {backup_file} | adb shell su -c "dd of={blk_path} bs=4M"'
                restore_process = subprocess.Popen(restore_cmd, shell=True)
                
                # Tampilkan progress
                total_size = os.path.getsize(backup_file) / (1024*1024)
                while restore_process.poll() is None:
                    time.sleep(1)
                    # Progress sulit diukur, cukup tampilkan sedang berjalan
                    sys.stdout.write(f"\r{THEME['info']}Sedang merestore... Total size: {total_size:.2f} MB")
                    sys.stdout.flush()
                
                self.stop_animation()
                print(THEME['success'] + f"\nPartisi {partition} berhasil direstore!")
                
                if self.confirm_action("Apakah Anda ingin me-reboot perangkat sekarang?"):
                    self.run_command('reboot', adb=True)
            else:
                self.stop_animation()
                print(THEME['error'] + f"Tidak dapat menemukan partisi {partition}!")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal merestore partisi {partition}: {str(e)}")
    
    def create_flashable_zip(self):
        """Buat flashable zip dari backup"""
        print(THEME['info'] + "\nFitur ini akan membuat file zip yang bisa di-flash via recovery")
        print(THEME['info'] + "File zip akan berisi:")
        print("- Script update-binary")
        print("- File system.img atau data.img")
        print("- Script updater-script untuk flash")
        
        backup_file = input(THEME['input'] + "Masukkan path file backup: ")
        partition = input(THEME['input'] + "Masukkan nama partisi (system/data): ").lower()
        zip_name = input(THEME['input'] + "Masukkan nama file zip output [flashable.zip]: ") or "flashable.zip"
        
        if not os.path.exists(backup_file):
            print(THEME['error'] + "File backup tidak ditemukan!")
            return
        
        if partition not in ['system', 'data']:
            print(THEME['error'] + "Partisi harus system atau data!")
            return
        
        self.start_animation("Membuat flashable zip...")
        
        try:
            # Buat direktori kerja
            if not os.path.exists('flashable_temp'):
                os.makedirs('flashable_temp/META-INF/com/google/android')
            
            # Salin file backup
            os.rename(backup_file, f'flashable_temp/{partition}.img')
            
            # Buat updater-script
            with open('flashable_temp/META-INF/com/google/android/updater-script', 'w') as f:
                f.write(f"""
ui_print("Flashing {partition} image...");
show_progress(0.500000, 0);
package_extract_file("{partition}.img", "/dev/block/bootdevice/by-name/{partition}");
show_progress(0.100000, 0);
ui_print("Flash selesai!");
""")
            
            # Buat update-binary (sederhana)
            with open('flashable_temp/META-INF/com/google/android/update-binary', 'w') as f:
                f.write("""#!/sbin/sh
# Dummy update-binary
echo "Starting flash..."
. /tmp/updater-script
""")
            os.chmod('flashable_temp/META-INF/com/google/android/update-binary', 0o755)
            
            # Buat zip
            import zipfile
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk('flashable_temp'):
                    for file in files:
                        zipf.write(os.path.join(root, file), 
                                  os.path.relpath(os.path.join(root, file), 
                                  'flashable_temp'))
            
            # Bersihkan
            import shutil
            shutil.rmtree('flashable_temp')
            
            self.stop_animation()
            print(THEME['success'] + f"Flashable zip berhasil dibuat: {zip_name}")
            print(THEME['info'] + "Anda bisa flash zip ini via custom recovery seperti TWRP")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal membuat flashable zip: {str(e)}")
    
    def adb_shell(self):
        """Akses shell ADB"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['title'] + "\n" + "="*70)
        print(f"{'ADB SHELL':^70}")
        print("="*70 + Style.RESET_ALL)
        
        print(THEME['info'] + "\nAnda sekarang masuk ke ADB shell. Ketik 'exit' untuk keluar.")
        print(THEME['info'] + "Perintah akan dijalankan di perangkat Android Anda.")
        
        while True:
            try:
                command = input(THEME['input'] + f"\n{self.current_device} $ ")
                
                if command.lower() in ['exit', 'quit']:
                    break
                
                if command.strip():
                    self.start_animation("Menjalankan perintah...")
                    result = self.run_command(f'shell {command}', adb=True)
                    self.stop_animation()
                    
                    if result:
                        print(result.stdout)
                        if result.stderr:
                            print(THEME['error'] + result.stderr)
            except KeyboardInterrupt:
                print(THEME['warning'] + "\nGunakan 'exit' untuk keluar dari shell")
            except Exception as e:
                print(THEME['error'] + f"Error: {str(e)}")
    
    def disconnect_device(self):
        """Putuskan koneksi perangkat"""
        if self.current_device:
            if ':' in self.current_device:  # Koneksi WiFi
                self.run_command(f'disconnect {self.current_device}', adb=True)
            print(THEME['info'] + f"Koneksi ke {self.current_device} diputus")
            self.current_device = None
        else:
            print(THEME['warning'] + "Tidak ada perangkat yang terhubung")
    
    def network_features(self):
        """Fitur jaringan tambahan"""
        while True:
            print(THEME['title'] + "\n" + "="*70)
            print(f"{'FITUR JARINGAN':^70}")
            print("="*70 + Style.RESET_ALL)
            
            print("\n1. Port Forwarding")
            print("2. Reverse Port Forwarding")
            print("3. ADB over Network")
            print("4. ADB over Internet (Ngrok)")
            print("5. Scan Port Perangkat")
            print("0. Kembali")
            
            choice = input(THEME['input'] + "\nPilih opsi [0-5]: ")
            
            if choice == '1':
                self.port_forwarding()
            elif choice == '2':
                self.reverse_port_forwarding()
            elif choice == '3':
                self.adb_over_network()
            elif choice == '4':
                self.adb_over_internet()
            elif choice == '5':
                self.scan_device_ports()
            elif choice == '0':
                break
            else:
                print(THEME['error'] + "Pilihan tidak valid!")
                time.sleep(1)
    
    def port_forwarding(self):
        """Port forwarding dari host ke device"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        local_port = input(THEME['input'] + "Masukkan port lokal: ")
        remote_port = input(THEME['input'] + "Masukkan port remote: ")
        
        if not local_port.isdigit() or not remote_port.isdigit():
            print(THEME['error'] + "Port harus angka!")
            return
        
        self.start_animation(f"Mengaktifkan port forwarding {local_port} -> {remote_port}...")
        result = self.run_command(f'forward tcp:{local_port} tcp:{remote_port}', adb=True)
        self.stop_animation()
        
        if result and result.returncode == 0:
            print(THEME['success'] + f"Port forwarding berhasil: localhost:{local_port} -> device:{remote_port}")
        else:
            print(THEME['error'] + "Gagal mengaktifkan port forwarding!")
    
    def reverse_port_forwarding(self):
        """Reverse port forwarding dari device ke host"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        remote_port = input(THEME['input'] + "Masukkan port remote: ")
        local_port = input(THEME['input'] + "Masukkan port lokal: ")
        
        if not local_port.isdigit() or not remote_port.isdigit():
            print(THEME['error'] + "Port harus angka!")
            return
        
        self.start_animation(f"Mengaktifkan reverse port forwarding {remote_port} -> {local_port}...")
        result = self.run_command(f'reverse tcp:{remote_port} tcp:{local_port}', adb=True)
        self.stop_animation()
        
        if result and result.returncode == 0:
            print(THEME['success'] + f"Reverse port forwarding berhasil: device:{remote_port} -> localhost:{local_port}")
        else:
            print(THEME['error'] + "Gagal mengaktifkan reverse port forwarding!")
    
    def adb_over_network(self):
        """Aktifkan ADB over jaringan lokal"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung via USB!")
            return
        
        port = input(THEME['input'] + f"Masukkan port ADB [{self.server_port}]: ") or self.server_port
        
        if not port.isdigit():
            print(THEME['error'] + "Port harus angka!")
            return
        
        self.start_animation(f"Mengaktifkan ADB over network di port {port}...")
        
        # Set perangkat ke mode TCPIP
        tcpip_result = self.run_command(f'tcpip {port}', adb=True)
        
        if tcpip_result and tcpip_result.returncode == 0:
            # Dapatkan IP perangkat
            ip_result = self.run_command('shell ip route', adb=True)
            
            if ip_result and ip_result.stdout:
                # Parse output untuk mendapatkan IP
                match = re.search(r'src (\d+\.\d+\.\d+\.\d+)', ip_result.stdout)
                if match:
                    device_ip = match.group(1)
                    self.stop_animation()
                    print(THEME['success'] + f"ADB over network diaktifkan!")
                    print(THEME['info'] + f"Gunakan perintah berikut untuk terhubung:")
                    print(THEME['info'] + f"adb connect {device_ip}:{port}")
                    self.server_port = port
                    return
        
        self.stop_animation()
        print(THEME['error'] + "Gagal mengaktifkan ADB over network!")
    
    def adb_over_internet(self):
        """Aktifkan ADB over internet menggunakan Ngrok"""
        print(THEME['info'] + "\nFitur ini akan menggunakan Ngrok untuk membuat tunnel ADB ke internet")
        print(THEME['warning'] + "PERINGATAN: Ini akan membuat perangkat Anda bisa diakses dari internet!")
        
        if not self.confirm_action("Apakah Anda yakin ingin melanjutkan?"):
            return
        
        # Cek apakah ngrok sudah diinstall
        self.start_animation("Memeriksa Ngrok...")
        try:
            ngrok_result = subprocess.run(['ngrok', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ngrok_installed = ngrok_result.returncode == 0
        except:
            ngrok_installed = False
        
        if not ngrok_installed:
            self.stop_animation()
            print(THEME['error'] + "Ngrok tidak ditemukan!")
            
            if self.platform == 'android':
                print(THEME['info'] + "Untuk Termux, Anda bisa install Ngrok dengan:")
                print(THEME['info'] + "1. Download dari https://ngrok.com/download")
                print(THEME['info'] + "2. Ekstrak dan simpan di ~/../usr/bin/")
                print(THEME['info'] + "3. chmod +x ~/../usr/bin/ngrok")
            else:
                print(THEME['info'] + "Silakan download Ngrok dari https://ngrok.com/download")
            
            input(THEME['input'] + "\nTekan Enter setelah Ngrok terinstall...")
            return
        
        self.stop_animation()
        
        # Jalankan Ngrok
        print(THEME['info'] + "\nMenjalankan Ngrok untuk ADB port 5555...")
        ngrok_process = subprocess.Popen(['ngrok', 'tcp', '5555'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # Beri waktu Ngrok untuk start
        
        # Dapatkan URL Ngrok
        try:
            import requests
            ngrok_api = requests.get('http://localhost:4040/api/tunnels').json()
            public_url = ngrok_api['tunnels'][0]['public_url']
            print(THEME['success'] + f"\nADB tersedia via internet di:")
            print(THEME['success'] + public_url)
            
            # Parse host dan port
            ngrok_host = public_url.split('//')[1].split(':')[0]
            ngrok_port = public_url.split(':')[2]
            
            print(THEME['info'] + "\nGunakan perintah berikut untuk terhubung dari jarak jauh:")
            print(THEME['info'] + f"adb connect {ngrok_host}:{ngrok_port}")
            
            input(THEME['input'] + "\nTekan Enter untuk menghentikan Ngrok...")
            ngrok_process.terminate()
        except Exception as e:
            print(THEME['error'] + f"Gagal mendapatkan URL Ngrok: {str(e)}")
            ngrok_process.terminate()
    
    def scan_device_ports(self):
        """Scan port yang terbuka di perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['info'] + "\nMemindai port yang terbuka di perangkat...")
        
        self.start_animation("Menjalankan scan port...")
        
        try:
            # Gunakan netstat di perangkat
            netstat_result = self.run_command('shell netstat -tuln', adb=True)
            self.stop_animation()
            
            if netstat_result and netstat_result.stdout:
                print(THEME['title'] + "\nPORT TERBUKA DI PERANGKAT:")
                print(netstat_result.stdout)
            else:
                print(THEME['error'] + "Tidak bisa mendapatkan info port. Mungkin membutuhkan root.")
                
                if self.confirm_action("Coba dengan akses root?"):
                    self.start_animation("Menjalankan scan port dengan root...")
                    netstat_root = self.run_command('shell su -c netstat -tuln', adb=True)
                    self.stop_animation()
                    
                    if netstat_root and netstat_root.stdout:
                        print(THEME['title'] + "\nPORT TERBUKA DI PERANGKAT (ROOT):")
                        print(netstat_root.stdout)
                    else:
                        print(THEME['error'] + "Gagal mendapatkan info port bahkan dengan root.")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal memindai port: {str(e)}")
    
    def advanced_features(self):
        """Fitur-fitur advanced"""
        while True:
            print(THEME['title'] + "\n" + "="*70)
            print(f"{'FITUR ADVANCED':^70}")
            print("="*70 + Style.RESET_ALL)
            
            print("\n1. Screen Mirroring")
            print("2. Rekam Layar")
            print("3. Screenshot")
            print("4. Buka Deep Link")
            print("5. Monitor Logcat")
            print("6. Monitor CPU/RAM")
            print("7. Monitor Baterai")
            print("8. Monitor Jaringan")
            print("9. Ekstrak APK dari Aplikasi")
            print("0. Kembali")
            
            choice = input(THEME['input'] + "\nPilih opsi [0-9]: ")
            
            if choice == '1':
                self.screen_mirroring()
            elif choice == '2':
                self.record_screen()
            elif choice == '3':
                self.take_screenshot()
            elif choice == '4':
                self.open_deep_link()
            elif choice == '5':
                self.monitor_logcat()
            elif choice == '6':
                self.monitor_cpu_ram()
            elif choice == '7':
                self.monitor_battery()
            elif choice == '8':
                self.monitor_network()
            elif choice == '9':
                self.extract_apk()
            elif choice == '0':
                break
            else:
                print(THEME['error'] + "Pilihan tidak valid!")
                time.sleep(1)
    
    def screen_mirroring(self):
        """Mirror layar perangkat ke komputer"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['info'] + "\nScreen mirroring akan menampilkan layar perangkat di komputer Anda")
        print(THEME['warning'] + "PERINGATAN: Fitur ini membutuhkan scrcpy yang terinstall!")
        
        # Cek scrcpy
        try:
            scrcpy_check = subprocess.run(['scrcpy', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            scrcpy_installed = scrcpy_check.returncode == 0
        except:
            scrcpy_installed = False
        
        if not scrcpy_installed:
            print(THEME['error'] + "scrcpy tidak ditemukan!")
            
            if self.platform == 'android':
                print(THEME['info'] + "Untuk Termux, Anda bisa install dengan:")
                print(THEME['info'] + "1. pkg install scrcpy")
                print(THEME['info'] + "2. pkg install android-tools")
            else:
                print(THEME['info'] + "Silakan install scrcpy dari https://github.com/Genymobile/scrcpy")
            
            input(THEME['input'] + "\nTekan Enter setelah scrcpy terinstall...")
            return
        
        # Jalankan scrcpy
        print(THEME['info'] + "\nMenjalankan scrcpy...")
        try:
            subprocess.run(['scrcpy'], check=True)
            print(THEME['success'] + "Screen mirroring selesai!")
        except Exception as e:
            print(THEME['error'] + f"Gagal menjalankan scrcpy: {str(e)}")
    
    def record_screen(self):
        """Rekam layar perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        output_file = input(THEME['input'] + "Masukkan nama file output [screenrecord.mp4]: ") or "screenrecord.mp4"
        duration = input(THEME['input'] + "Masukkan durasi rekaman (detik) [180]: ") or "180"
        
        if not duration.isdigit():
            print(THEME['error'] + "Durasi harus angka!")
            return
        
        print(THEME['info'] + f"\nRekaman akan disimpan sebagai {output_file} selama {duration} detik")
        print(THEME['info'] + "Tekan Ctrl+C untuk menghentikan rekaman lebih awal")
        
        self.start_animation("Memulai rekaman layar...")
        try:
            record_process = self.run_command(f'shell screenrecord --time-limit {duration} /sdcard/{output_file}', adb=True, background=True)
            
            # Tampilkan timer
            for i in range(int(duration)):
                sys.stdout.write(f"\r{THEME['info']}Rekaman berlangsung... {i+1}/{duration} detik")
                sys.stdout.flush()
                time.sleep(1)
                if record_process.poll() is not None:
                    break
            
            # Download rekaman
            print(THEME['info'] + "\nMengunduh rekaman...")
            self.run_command(f'pull /sdcard/{output_file}', adb=True)
            self.run_command(f'shell rm /sdcard/{output_file}', adb=True)
            
            self.stop_animation()
            print(THEME['success'] + f"\nRekaman berhasil disimpan sebagai {output_file}")
        except KeyboardInterrupt:
            self.stop_animation()
            print(THEME['warning'] + "\nRekaman dihentikan lebih awal!")
            
            # Tetap coba download rekaman yang sudah ada
            if self.confirm_action("Download rekaman yang sudah terekam?"):
                self.run_command(f'pull /sdcard/{output_file}', adb=True)
                self.run_command(f'shell rm /sdcard/{output_file}', adb=True)
                print(THEME['info'] + f"Rekaman parsial disimpan sebagai {output_file}")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal merekam layar: {str(e)}")
    
    def take_screenshot(self):
        """Ambil screenshot dari perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        output_file = input(THEME['input'] + "Masukkan nama file output [screenshot.png]: ") or "screenshot.png"
        
        self.start_animation("Mengambil screenshot...")
        try:
            # Ambil screenshot
            self.run_command(f'shell screencap -p /sdcard/{output_file}', adb=True)
            
            # Download screenshot
            self.run_command(f'pull /sdcard/{output_file}', adb=True)
            self.run_command(f'shell rm /sdcard/{output_file}', adb=True)
            
            self.stop_animation()
            print(THEME['success'] + f"Screenshot berhasil disimpan sebagai {output_file}")
            
            # Coba tampilkan screenshot jika memungkinkan
            if self.confirm_action("Tampilkan screenshot?"):
                try:
                    if self.platform == 'windows':
                        os.startfile(output_file)
                    elif self.platform == 'linux':
                        subprocess.run(['xdg-open', output_file])
                    elif self.platform == 'android':
                        subprocess.run(['termux-open', output_file])
                except:
                    print(THEME['warning'] + "Tidak bisa menampilkan screenshot. Buka manual.")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal mengambil screenshot: {str(e)}")
    
    def open_deep_link(self):
        """Buka deep link di perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        deep_link = input(THEME['input'] + "Masukkan deep link (contoh: https://example.com): ")
        
        if not deep_link:
            print(THEME['error'] + "Deep link tidak boleh kosong!")
            return
        
        self.start_animation(f"Membuka {deep_link}...")
        result = self.run_command(f'shell am start -a android.intent.action.VIEW -d "{deep_link}"', adb=True)
        self.stop_animation()
        
        if result and result.returncode == 0:
            print(THEME['success'] + f"Deep link {deep_link} berhasil dibuka!")
        else:
            print(THEME['error'] + f"Gagal membuka deep link {deep_link}!")
    
    def monitor_logcat(self):
        """Monitor logcat perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['info'] + "\nMemantau logcat perangkat. Tekan Ctrl+C untuk berhenti.")
        print(THEME['info'] + "Filter opsional (contoh: *:E untuk error saja):")
        log_filter = input(THEME['input'] + "Masukkan filter logcat (kosongkan untuk semua): ") or ""
        
        try:
            logcat_cmd = ['adb', 'logcat']
            if log_filter:
                logcat_cmd.append(log_filter)
            
            logcat_process = subprocess.Popen(logcat_cmd)
            logcat_process.wait()
        except KeyboardInterrupt:
            print(THEME['warning'] + "\nMenghentikan logcat...")
            logcat_process.terminate()
        except Exception as e:
            print(THEME['error'] + f"Gagal memantau logcat: {str(e)}")
    
    def monitor_cpu_ram(self):
        """Monitor penggunaan CPU dan RAM perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['info'] + "\nMemantau CPU dan RAM perangkat. Tekan Ctrl+C untuk berhenti.")
        
        try:
            while True:
                # Dapatkan info CPU
                cpu_cmd = 'shell top -n 1 | grep -A 1 "PID USER" | tail -n 1'
                cpu_result = self.run_command(cpu_cmd, adb=True)
                
                # Dapatkan info RAM
                ram_cmd = 'shell cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable"'
                ram_result = self.run_command(ram_cmd, adb=True)
                
                # Bersihkan layar
                os.system('cls' if self.platform == 'windows' else 'clear')
                
                # Tampilkan header
                print(THEME['title'] + "\n" + "="*70)
                print(f"{'MONITOR CPU & RAM':^70}")
                print("="*70 + Style.RESET_ALL)
                
                # Tampilkan CPU
                if cpu_result and cpu_result.stdout:
                    cpu_parts = cpu_result.stdout.strip().split()
                    if len(cpu_parts) >= 9:
                        print(f"\n{THEME['menu']}CPU Usage:{Style.RESET_ALL}")
                        print(f"PID: {cpu_parts[0]}")
                        print(f"User: {cpu_parts[1]}")
                        print(f"CPU%: {cpu_parts[8]}%")
                        print(f"Command: {' '.join(cpu_parts[10:])}")
                
                # Tampilkan RAM
                if ram_result and ram_result.stdout:
                    ram_lines = ram_result.stdout.strip().splitlines()
                    ram_info = {}
                    for line in ram_lines:
                        parts = line.split(':')
                        if len(parts) == 2:
                            ram_info[parts[0].strip()] = parts[1].strip()
                    
                    print(f"\n{THEME['menu']}RAM Usage:{Style.RESET_ALL}")
                    if 'MemTotal' in ram_info:
                        total = int(ram_info['MemTotal'].split()[0])
                        print(f"Total: {total / 1024:.2f} MB")
                    if 'MemFree' in ram_info:
                        free = int(ram_info['MemFree'].split()[0])
                        print(f"Free: {free / 1024:.2f} MB")
                    if 'MemAvailable' in ram_info:
                        avail = int(ram_info['MemAvailable'].split()[0])
                        print(f"Available: {avail / 1024:.2f} MB")
                        if 'MemTotal' in ram_info:
                            used = total - avail
                            print(f"Used: {used / 1024:.2f} MB ({used/total*100:.1f}%)")
                
                print(THEME['info'] + "\nTekan Ctrl+C untuk berhenti...")
                time.sleep(2)
        except KeyboardInterrupt:
            print(THEME['warning'] + "\nMenghentikan monitor...")
        except Exception as e:
            print(THEME['error'] + f"Gagal memantau: {str(e)}")
    
    def monitor_battery(self):
        """Monitor status baterai perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['info'] + "\nMemantau status baterai perangkat. Tekan Ctrl+C untuk berhenti.")
        
        try:
            while True:
                # Dapatkan info baterai
                bat_cmd = 'shell dumpsys battery'
                bat_result = self.run_command(bat_cmd, adb=True)
                
                # Bersihkan layar
                os.system('cls' if self.platform == 'windows' else 'clear')
                
                # Tampilkan header
                print(THEME['title'] + "\n" + "="*70)
                print(f"{'MONITOR BATERAI':^70}")
                print("="*70 + Style.RESET_ALL)
                
                # Tampilkan info baterai
                if bat_result and bat_result.stdout:
                    bat_lines = bat_result.stdout.strip().splitlines()
                    bat_info = {}
                    for line in bat_lines:
                        if ':' in line:
                            parts = line.split(':')
                            key = parts[0].strip()
                            value = ':'.join(parts[1:]).strip()
                            bat_info[key] = value
                    
                    print(f"\n{THEME['menu']}Status Baterai:{Style.RESET_ALL}")
                    if 'level' in bat_info:
                        print(f"Level: {bat_info['level']}%")
                    if 'status' in bat_info:
                        status_map = {
                            '2': 'Charging',
                            '3': 'Discharging',
                            '4': 'Not charging',
                            '5': 'Full'
                        }
                        status = bat_info['status']
                        print(f"Status: {status_map.get(status, 'Unknown')} ({status})")
                    if 'health' in bat_info:
                        health_map = {
                            '2': 'Good',
                            '3': 'Overheat',
                            '4': 'Dead',
                            '5': 'Over voltage',
                            '6': 'Unspecified failure',
                            '7': 'Cold'
                        }
                        health = bat_info['health']
                        print(f"Health: {health_map.get(health, 'Unknown')} ({health})")
                    if 'temperature' in bat_info:
                        temp = int(bat_info['temperature']) / 10
                        print(f"Temperature: {temp}°C")
                    if 'voltage' in bat_info:
                        volt = int(bat_info['voltage'])
                        print(f"Voltage: {volt} mV")
                    if 'technology' in bat_info:
                        print(f"Technology: {bat_info['technology']}")
                
                print(THEME['info'] + "\nTekan Ctrl+C untuk berhenti...")
                time.sleep(2)
        except KeyboardInterrupt:
            print(THEME['warning'] + "\nMenghentikan monitor...")
        except Exception as e:
            print(THEME['error'] + f"Gagal memantau: {str(e)}")
    
    def monitor_network(self):
        """Monitor aktivitas jaringan perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['info'] + "\nMemantau aktivitas jaringan perangkat. Tekan Ctrl+C untuk berhenti.")
        
        try:
            prev_rx = 0
            prev_tx = 0
            
            while True:
                # Dapatkan statistik jaringan
                net_cmd = 'shell cat /proc/net/dev'
                net_result = self.run_command(net_cmd, adb=True)
                
                # Bersihkan layar
                os.system('cls' if self.platform == 'windows' else 'clear')
                
                # Tampilkan header
                print(THEME['title'] + "\n" + "="*70)
                print(f"{'MONITOR JARINGAN':^70}")
                print("="*70 + Style.RESET_ALL)
                
                # Proses statistik jaringan
                if net_result and net_result.stdout:
                    net_lines = net_result.stdout.strip().splitlines()
                    interfaces = {}
                    
                    for line in net_lines[2:]:  # Lewati 2 baris header
                        parts = line.split()
                        if len(parts) >= 17:
                            iface = parts[0].replace(':', '')
                            rx_bytes = int(parts[1])
                            tx_bytes = int(parts[9])
                            interfaces[iface] = (rx_bytes, tx_bytes)
                    
                    # Hitung perbedaan dengan sebelumnya
                    current_rx = sum(rx for rx, tx in interfaces.values())
                    current_tx = sum(tx for rx, tx in interfaces.values())
                    
                    diff_rx = current_rx - prev_rx
                    diff_tx = current_tx - prev_tx
                    
                    # Konversi ke KB/s (asumsi interval 1 detik)
                    rx_rate = diff_rx / 1024
                    tx_rate = diff_tx / 1024
                    
                    # Tampilkan info
                    print(f"\n{THEME['menu']}Aktivitas Jaringan:{Style.RESET_ALL}")
                    print(f"Download: {rx_rate:.2f} KB/s")
                    print(f"Upload: {tx_rate:.2f} KB/s")
                    print(f"\n{THEME['menu']}Total:{Style.RESET_ALL}")
                    print(f"Received: {current_rx / (1024*1024):.2f} MB")
                    print(f"Transmitted: {current_tx / (1024*1024):.2f} MB")
                    
                    # Simpan nilai saat ini untuk perhitungan berikutnya
                    prev_rx = current_rx
                    prev_tx = current_tx
                
                print(THEME['info'] + "\nTekan Ctrl+C untuk berhenti...")
                time.sleep(1)
        except KeyboardInterrupt:
            print(THEME['warning'] + "\nMenghentikan monitor...")
        except Exception as e:
            print(THEME['error'] + f"Gagal memantau: {str(e)}")
    
    def extract_apk(self):
        """Ekstrak APK dari aplikasi yang terinstall"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        package_name = input(THEME['input'] + "Masukkan nama package aplikasi: ")
        output_file = input(THEME['input'] + "Masukkan nama file output [app.apk]: ") or "app.apk"
        
        self.start_animation(f"Mengekstrak APK {package_name}...")
        
        try:
            # Dapatkan path APK
            path_result = self.run_command(f'shell pm path {package_name}', adb=True)
            if path_result and path_result.returncode == 0:
                apk_path = path_result.stdout.strip().replace('package:', '')
                
                # Download APK
                pull_result = self.run_command(f'pull "{apk_path}" "{output_file}"', adb=True)
                self.stop_animation()
                
                if pull_result and pull_result.returncode == 0:
                    print(THEME['success'] + f"APK berhasil diekstrak ke {output_file}!")
                else:
                    print(THEME['error'] + "Gagal mendownload APK!")
            else:
                self.stop_animation()
                print(THEME['error'] + "Gagal mendapatkan path APK!")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal mengekstrak APK: {str(e)}")
    
    def main_menu(self):
        """Menu utama aplikasi"""
        while self.running:
            print(THEME['title'] + "\n" + "="*70)
            print(f"{'ULTIMATE ANDROID OTG ADB CONTROLLER':^70}")
            print(f"{'VIP+++ EDITION':^70}")
            print("="*70 + Style.RESET_ALL)
            
            print("\n1. Hubungkan Perangkat")
            print("2. Fitur Jaringan")
            print("3. Fitur Advanced")
            print("4. Tools Tambahan")
            print("5. Pengaturan")
            print("0. Keluar")
            
            choice = input(THEME['input'] + "\nPilih opsi [0-5]: ")
            
            if choice == '1':
                self.connect_device()
            elif choice == '2':
                self.network_features()
            elif choice == '3':
                self.advanced_features()
            elif choice == '4':
                self.additional_tools()
            elif choice == '5':
                self.settings_menu()
            elif choice == '0':
                if self.current_device:
                    self.disconnect_device()
                print(THEME['success'] + "\nTerima kasih telah menggunakan Ultimate Android OTG ADB Controller!")
                self.running = False
            else:
                print(THEME['error'] + "Pilihan tidak valid!")
                time.sleep(1)
    
    def additional_tools(self):
        """Tools tambahan"""
        while True:
            print(THEME['title'] + "\n" + "="*70)
            print(f"{'TOOLS TAMBAHAN':^70}")
            print("="*70 + Style.RESET_ALL)
            
            print("\n1. Reboot Perangkat")
            print("2. Reboot Recovery")
            print("3. Reboot Bootloader")
            print("4. Reboot Fastboot")
            print("5. Reboot Sideload")
            print("6. Hapus Cache Partisi")
            print("7. Factory Reset")
            print("8. Flash ZIP dari Recovery")
            print("9. Flash Image ke Partisi")
            print("0. Kembali")
            
            choice = input(THEME['input'] + "\nPilih opsi [0-9]: ")
            
            if choice == '1':
                self.reboot_device()
            elif choice == '2':
                self.reboot_recovery()
            elif choice == '3':
                self.reboot_bootloader()
            elif choice == '4':
                self.reboot_fastboot()
            elif choice == '5':
                self.reboot_sideload()
            elif choice == '6':
                self.wipe_cache()
            elif choice == '7':
                self.factory_reset()
            elif choice == '8':
                self.flash_zip()
            elif choice == '9':
                self.flash_image()
            elif choice == '0':
                break
            else:
                print(THEME['error'] + "Pilihan tidak valid!")
                time.sleep(1)
    
    def reboot_device(self, mode=None):
        """Reboot perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        modes = {
            None: 'reboot',
            'recovery': 'reboot recovery',
            'bootloader': 'reboot bootloader',
            'fastboot': 'reboot fastboot',
            'sideload': 'reboot sideload'
        }
        
        mode_name = {
            None: 'normal',
            'recovery': 'recovery',
            'bootloader': 'bootloader',
            'fastboot': 'fastboot',
            'sideload': 'sideload'
        }
        
        if not self.confirm_action(f"Apakah Anda yakin ingin reboot ke mode {mode_name[mode]}?"):
            return
        
        self.start_animation(f"Reboot ke mode {mode_name[mode]}...")
        result = self.run_command(modes[mode], adb=True)
        self.stop_animation()
        
        if result and result.returncode == 0:
            print(THEME['success'] + f"Perintah reboot {mode_name[mode]} berhasil dikirim!")
        else:
            print(THEME['error'] + f"Gagal mengirim perintah reboot {mode_name[mode]}!")
    
    def reboot_recovery(self):
        """Reboot ke recovery"""
        self.reboot_device('recovery')
    
    def reboot_bootloader(self):
        """Reboot ke bootloader"""
        self.reboot_device('bootloader')
    
    def reboot_fastboot(self):
        """Reboot ke fastboot"""
        self.reboot_device('fastboot')
    
    def reboot_sideload(self):
        """Reboot ke sideload"""
        self.reboot_device('sideload')
    
    def wipe_cache(self):
        """Hapus cache partisi"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['warning'] + "\nPERINGATAN: Menghapus cache partisi akan:")
        print("- Menghapus semua cache sistem dan aplikasi")
        print("- Tidak menghapus data pribadi")
        print("- Mungkin memperbaiki beberapa masalah sistem")
        
        if not self.confirm_action("Apakah Anda yakin ingin menghapus cache partisi?"):
            return
        
        self.start_animation("Menghapus cache partisi...")
        
        try:
            # Reboot ke recovery
            self.run_command('reboot recovery', adb=True)
            time.sleep(10)
            
            # Jika menggunakan fastboot
            if self.fastboot_path:
                # Jalankan perintah wipe cache
                wipe_result = self.run_command('erase cache', fastboot=True)
                
                if wipe_result and wipe_result.returncode == 0:
                    print(THEME['success'] + "Cache partisi berhasil dihapus!")
                else:
                    print(THEME['error'] + "Gagal menghapus cache partisi!")
            
            # Reboot kembali ke sistem
            self.run_command('reboot', fastboot=True)
            self.stop_animation()
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal menghapus cache partisi: {str(e)}")
    
    def factory_reset(self):
        """Factory reset perangkat"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        print(THEME['warning'] + "\nPERINGATAN: Factory reset akan:")
        print("- Menghapus SEMUA DATA di perangkat")
        print("- Mengembalikan ke pengaturan pabrik")
        print("- Membutuhkan setup ulang perangkat")
        
        if not self.confirm_action("Apakah Anda BENAR-BENAR yakin ingin factory reset?"):
            return
        
        self.start_animation("Melakukan factory reset...")
        
        try:
            # Jalankan factory reset via fastboot
            if self.fastboot_path:
                reset_result = self.run_command('-w', fastboot=True)
                
                if reset_result and reset_result.returncode == 0:
                    print(THEME['success'] + "Factory reset berhasil!")
                else:
                    print(THEME['error'] + "Gagal melakukan factory reset!")
            
            # Reboot
            self.run_command('reboot', fastboot=True)
            self.stop_animation()
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal melakukan factory reset: {str(e)}")
    
    def flash_zip(self):
        """Flash zip dari recovery"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        zip_file = input(THEME['input'] + "Masukkan path file zip: ")
        
        if not os.path.exists(zip_file):
            print(THEME['error'] + "File zip tidak ditemukan!")
            return
        
        print(THEME['warning'] + "\nPERINGATAN: Flash zip dapat:")
        print("- Mengubah sistem perangkat")
        print("- Menyebabkan masalah jika zip tidak kompatibel")
        print("- Membutuhkan custom recovery seperti TWRP")
        
        if not self.confirm_action("Apakah Anda yakin ingin flash zip ini?"):
            return
        
        self.start_animation(f"Flashing {zip_file}...")
        
        try:
            # Reboot ke recovery
            self.run_command('reboot recovery', adb=True)
            time.sleep(15)
            
            # Sideload zip
            print(THEME['info'] + "\nHarap pilih 'Install' atau 'ADB Sideload' di recovery")
            input(THEME['input'] + "Tekan Enter setelah siap...")
            
            # Jalankan sideload
            sideload_result = self.run_command(f'sideload "{zip_file}"', adb=True)
            
            if sideload_result and sideload_result.returncode == 0:
                print(THEME['success'] + "Flash zip berhasil!")
            else:
                print(THEME['error'] + "Gagal flash zip!")
            
            # Reboot
            self.run_command('reboot', adb=True)
            self.stop_animation()
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal flash zip: {str(e)}")
    
    def flash_image(self):
        """Flash image ke partisi"""
        if not self.current_device:
            print(THEME['error'] + "Tidak ada perangkat yang terhubung!")
            return
        
        if not self.fastboot_path:
            print(THEME['error'] + "Fastboot tidak tersedia!")
            return
        
        image_file = input(THEME['input'] + "Masukkan path file image: ")
        partition = input(THEME['input'] + "Masukkan nama partisi (system, boot, recovery, dll): ")
        
        if not os.path.exists(image_file):
            print(THEME['error'] + "File image tidak ditemukan!")
            return
        
        if not partition:
            print(THEME['error'] + "Nama partisi tidak boleh kosong!")
            return
        
        print(THEME['warning'] + "\nPERINGATAN: Flash image dapat:")
        print("- Merusak perangkat jika partisi salah")
        print("- Membuat perangkat tidak bisa boot")
        print("- Membutuhkan bootloader yang sudah di-unlock")
        
        if not self.confirm_action(f"Apakah Anda yakin ingin flash {partition} dengan {image_file}?"):
            return
        
        self.start_animation(f"Flashing {image_file} ke {partition}...")
        
        try:
            # Reboot ke bootloader
            self.run_command('reboot bootloader', adb=True)
            time.sleep(10)
            
            # Flash image
            flash_result = self.run_command(f'flash {partition} {image_file}', fastboot=True)
            
            if flash_result and flash_result.returncode == 0:
                print(THEME['success'] + f"Image berhasil di-flash ke {partition}!")
            else:
                print(THEME['error'] + f"Gagal flash image ke {partition}!")
            
            # Reboot
            self.run_command('reboot', fastboot=True)
            self.stop_animation()
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal flash image: {str(e)}")
    
    def settings_menu(self):
        """Menu pengaturan"""
        while True:
            print(THEME['title'] + "\n" + "="*70)
            print(f"{'PENGATURAN':^70}")
            print("="*70 + Style.RESET_ALL)
            
            print("\n1. Ganti Port ADB")
            print("2. Ganti Tema Terminal")
            print("3. Update Tool")
            print("4. Reset Pengaturan")
            print("0. Kembali")
            
            choice = input(THEME['input'] + "\nPilih opsi [0-4]: ")
            
            if choice == '1':
                self.change_adb_port()
            elif choice == '2':
                self.change_terminal_theme()
            elif choice == '3':
                self.update_tool()
            elif choice == '4':
                self.reset_settings()
            elif choice == '0':
                break
            else:
                print(THEME['error'] + "Pilihan tidak valid!")
                time.sleep(1)
    
    def change_adb_port(self):
        """Ganti port ADB default"""
        new_port = input(THEME['input'] + f"Masukkan port ADB baru [{self.server_port}]: ") or self.server_port
        
        if not new_port.isdigit() or int(new_port) < 1024 or int(new_port) > 65535:
            print(THEME['error'] + "Port harus antara 1024 dan 65535!")
            return
        
        self.server_port = int(new_port)
        print(THEME['success'] + f"Port ADB diubah ke {self.server_port}")
    
    def change_terminal_theme(self):
        """Ganti tema terminal"""
        print(self.THEME['title'] + "\n" + "="*70)
        print(f"{'PILIH TEMA TERMINAL':^70}")
        print("="*70 + Style.RESET_ALL)

        themes = [
            ("Biru Standar", {
                'success': Fore.GREEN + Style.BRIGHT,
                'error': Fore.RED + Style.BRIGHT,
                'warning': Fore.YELLOW + Style.BRIGHT,
                'info': Fore.CYAN + Style.BRIGHT,
                'debug': Fore.MAGENTA + Style.BRIGHT,
                'title': Fore.BLUE + Style.BRIGHT + Back.WHITE,
                'menu': Fore.WHITE + Style.BRIGHT + Back.BLUE,
                'input': Fore.YELLOW + Style.BRIGHT,
                'special': Fore.RED + Back.YELLOW + Style.BRIGHT
            }),
            ("Hijau Gelap", {
                'success': Fore.GREEN + Style.BRIGHT,
                'error': Fore.RED + Style.BRIGHT,
                'warning': Fore.YELLOW + Style.BRIGHT,
                'info': Fore.CYAN + Style.BRIGHT,
                'debug': Fore.MAGENTA + Style.BRIGHT,
                'title': Fore.GREEN + Style.BRIGHT + Back.BLACK,
                'menu': Fore.WHITE + Style.BRIGHT + Back.GREEN,
                'input': Fore.YELLOW + Style.BRIGHT,
                'special': Fore.WHITE + Back.GREEN + Style.BRIGHT
            }),
            ("Merah Dramatis", {
                'success': Fore.GREEN + Style.BRIGHT,
                'error': Fore.RED + Style.BRIGHT,
                'warning': Fore.YELLOW + Style.BRIGHT,
                'info': Fore.CYAN + Style.BRIGHT,
                'debug': Fore.MAGENTA + Style.BRIGHT,
                'title': Fore.RED + Style.BRIGHT + Back.WHITE,
                'menu': Fore.WHITE + Style.BRIGHT + Back.RED,
                'input': Fore.YELLOW + Style.BRIGHT,
                'special': Fore.WHITE + Back.RED + Style.BRIGHT
            }),
            ("Ungu Futuristik", {
                'success': Fore.GREEN + Style.BRIGHT,
                'error': Fore.RED + Style.BRIGHT,
                'warning': Fore.YELLOW + Style.BRIGHT,
                'info': Fore.CYAN + Style.BRIGHT,
                'debug': Fore.MAGENTA + Style.BRIGHT,
                'title': Fore.MAGENTA + Style.BRIGHT + Back.WHITE,
                'menu': Fore.WHITE + Style.BRIGHT + Back.MAGENTA,
                'input': Fore.YELLOW + Style.BRIGHT,
                'special': Fore.WHITE + Back.MAGENTA + Style.BRIGHT
            })
        ]

        for i, (name, _) in enumerate(themes, 1):
            print(f"{i}. {name}")

        choice = input(self.THEME['input'] + "\nPilih tema [1-4]: ")

        try:
            choice = int(choice) - 1
            if 0 <= choice < len(themes):
                self.THEME = themes[choice][1]
                print(self.THEME['success'] + f"Tema diubah ke {themes[choice][0]}")
            else:
                print(self.THEME['error'] + "Pilihan tidak valid!")
        except ValueError:
            print(self.THEME['error'] + "Masukkan angka!")

    
    def update_tool(self):
        """Update tool ke versi terbaru"""
        print(THEME['info'] + "\nMemeriksa update...")
        
        try:
            # URL raw ke file script di GitHub
            updatesceh = "https://raw.githubusercontent.com/Habibzz01/UpdateTools-/refs/heads/main/XbibzRoot.py"
            
            # Dapatkan versi saat ini
            current_version = "2.0"
            
            # Dapatkan versi terbaru dari GitHub
            self.start_animation("Menghubungi server...")
            response = urllib.request.urlopen(updatesceh)
            content = response.read().decode('utf-8')
            
            # Cari versi di file
            version_match = re.search(r'Versi: (\d+\.\d+\.\d+)', content)
            if version_match:
                latest_version = version_match.group(1)
                
                if latest_version == current_version:
                    self.stop_animation()
                    print(THEME['success'] + "Anda sudah menggunakan versi terbaru!")
                else:
                    self.stop_animation()
                    print(THEME['info'] + f"Versi terbaru tersedia: {latest_version}")
                    print(THEME['info'] + f"Versi Anda saat ini: {current_version}")
                    
                    if self.confirm_action("Apakah Anda ingin update sekarang?"):
                        # Backup file saat ini
                        backup_name = f"XbibzRoot{current_version}.py"
                        with open(__file__, 'r') as f:
                            current_content = f.read()
                        
                        with open(backup_name, 'w') as f:
                            f.write(current_content)
                        
                        # Download versi baru
                        self.start_animation("Mengupdate tool...")
                        with open(__file__, 'w') as f:
                            f.write(content)
                        
                        self.stop_animation()
                        print(THEME['success'] + "Update berhasil!")
                        print(THEME['info'] + f"Backup versi lama disimpan sebagai {backup_name}")
                        print(THEME['info'] + "Silakan jalankan ulang tool untuk perubahan berlaku")
                        sys.exit(0)
            else:
                self.stop_animation()
                print(THEME['error'] + "Tidak bisa memeriksa versi terbaru!")
        except Exception as e:
            self.stop_animation()
            print(THEME['error'] + f"Gagal memeriksa update: {str(e)}")
    
    def reset_settings(self):
        """Reset semua pengaturan ke default"""
        if not self.confirm_action("Apakah Anda yakin ingin reset semua pengaturan?"):
            return
        
        self.server_port = 5555
        global THEME
        THEME = {
            'success': Fore.GREEN + Style.BRIGHT,
            'error': Fore.RED + Style.BRIGHT,
            'warning': Fore.YELLOW + Style.BRIGHT,
            'info': Fore.CYAN + Style.BRIGHT,
            'debug': Fore.MAGENTA + Style.BRIGHT,
            'title': Fore.BLUE + Style.BRIGHT + Back.WHITE,
            'menu': Fore.WHITE + Style.BRIGHT + Back.BLUE,
            'input': Fore.YELLOW + Style.BRIGHT,
            'special': Fore.RED + Back.YELLOW + Style.BRIGHT
        }
        
        print(THEME['success'] + "Semua pengaturan telah direset ke default!")

if __name__ == "__main__":
    try:
        controller = AndroidOTGController()
        controller.main_menu()
    except KeyboardInterrupt:
        print(THEME['error'] + "\nProgram dihentikan oleh pengguna")
        sys.exit(0)
    except Exception as e:
        print(THEME['error'] + f"\nError tidak terduga: {str(e)}")
        sys.exit(1)
