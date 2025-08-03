import os
import shutil
import subprocess
import datetime
import smtplib
from email.message import EmailMessage
import scapy.all as scapy
import socket
import platform
import json

# === Utility Functions ===
def pause():
    input("\nPress Enter to return to the menu...")

# === 1. Network Scanner ===
def network_scanner():
    ip_range = input("Enter IP base (e.g., 192.168.1): ")
    print("Scanning using ping...")
    for i in range(1, 255):
        ip = f"{ip_range}.{i}"
        os.system(f"ping -n 1 -w 100 {ip} >nul")
    print("\nDevices detected:")
    os.system("arp -a")
    try:
        print("\nScanning with scapy if available...")
        arp_req = scapy.ARP(pdst=f"{ip_range}.1/24")
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        request = broadcast / arp_req
        answered = scapy.srp(request, timeout=2, verbose=False)[0]
        for element in answered:
            print(f"IP: {element[1].psrc} | MAC: {element[1].hwsrc}")
    except Exception as e:
        print("Scapy not working or Npcap not installed.")
    pause()

# === 2. Ping Checker ===
def ping_checker():
    host = input("Enter IP or domain: ")
    response = os.system(f"ping -n 1 {host}")
    status = "Online" if response == 0 else "Offline"
    print(f"{host} -> {status}")
    pause()

# === 3. Check AD User Status ===
def ad_user_status():
    username = input("Enter username: ")
    result = subprocess.run(["net", "user", username, "/domain"], capture_output=True, text=True)
    if "Account active               Yes" in result.stdout:
        print(f"{username} is Active")
    else:
        print(f"{username} is Disabled or Not Found")
    pause()

# === 4. Backup Folder ===
def backup_folder():
    source = input("Enter source folder path: ")
    dest_base = input("Enter destination base folder path: ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    destination = os.path.join(dest_base, f"backup_{timestamp}")
    shutil.copytree(source, destination)
    print(f"Backup completed to: {destination}")
    pause()

# === 5. Extract Logs for Last X Days ===
def extract_logs():
    log_dir = os.path.expandvars(r"%SystemRoot%\\System32\\winevt\\Logs")
    log_file = os.path.join(log_dir, "System.evtx")
    print(f"Using log file: {log_file}")
    print("This feature requires external tools to parse EVTX. Not implemented here.")
    pause()

# === 6. Send Email with Attachment ===
def send_email():
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
    to = input("Enter recipient email: ")
    file_path = input("Enter attachment path (or press Enter to skip): ")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "your_email@gmail.com"
    msg['To'] = to
    msg.set_content(body)

    if file_path:
        with open(file_path, 'rb') as file:
            msg.add_attachment(file.read(), maintype='application', subtype='octet-stream', filename=os.path.basename(file_path))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login("your_email@gmail.com", "your_app_password")
            smtp.send_message(msg)
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Make sure to use App Password if you're using Gmail.")
    pause()

# === 7. Disk Usage Monitor ===
def disk_monitor():
    path = input("Enter drive path (default C:/): ") or "C:/"
    total, used, free = shutil.disk_usage(path)
    percent_used = used / total * 100
    print(f"Disk usage: {percent_used:.2f}%")
    if percent_used > 80:
        print("⚠️ Warning: Disk usage is over 80%")
    pause()

# === 8. Clean Temp Files ===
def clean_temp():
    paths = [os.environ['TEMP'], "C:\\Windows\\Temp", "C:\\Windows\\Prefetch"]
    for path in paths:
        try:
            for file in os.listdir(path):
                full_path = os.path.join(path, file)
                try:
                    if os.path.isfile(full_path):
                        os.remove(full_path)
                    elif os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                except Exception as e:
                    continue
            print(f"✅ Cleaned: {path}")
        except Exception as e:
            print(f"❌ Error cleaning {path}: {e}")
    pause()

# === 9. Network Interface Info ===
def network_info():
    print("\n=== Network Information ===")
    os.system("ipconfig /all")
    print("\n--- Connected Wi-Fi Profile ---")
    try:
        current = subprocess.check_output("netsh wlan show interfaces", shell=True).decode(errors='ignore')
        for line in current.splitlines():
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":")[1].strip()
                break
        profile_info = subprocess.check_output(f"netsh wlan show profile name=\"{ssid}\" key=clear", shell=True).decode(errors='ignore')
        print(f"\n[SSID] {ssid}")
        for line in profile_info.splitlines():
            if "Key Content" in line:
                print(f"[Password] {line.split(':')[1].strip()}")
    except Exception as e:
        print("Unable to retrieve connected Wi-Fi password.", e)
    pause()

# === Main Menu ===
def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
======== IT Automation Toolkit ========
1. Network Scanner
2. Ping Checker
3. Check AD User Status
4. Backup Folder
5. Extract Logs for Last X Days
6. Send Email with Attachment
7. Monitor Disk Usage
8. Clean Temp and Prefetch Files
9. View Network Interface Info
0. Exit
=======================================
        """)
        choice = input("Select an option: ")
        match choice:
            case "1": network_scanner()
            case "2": ping_checker()
            case "3": ad_user_status()
            case "4": backup_folder()
            case "5": extract_logs()
            case "6": send_email()
            case "7": disk_monitor()
            case "8": clean_temp()
            case "9": network_info()
            case "0": break
            case _: print("❌ Invalid choice."); pause()

if __name__ == "__main__":
    main()
