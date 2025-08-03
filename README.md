 🛠️ IT Automation Toolkit – CMD Version

A fully interactive Batch (.bat) script for IT professionals to automate daily tasks using a clean CLI interface in Windows CMD. No installation or dependencies required.

🚀 Features

| Feature                      | Description |
|-----------------------------|-------------|
| ✅ Network Scanner           | Ping-based scan with ARP output |
| ✅ Ping Checker              | Check connectivity to domain/IP |
| ✅ AD User Status Checker    | View if a domain user is active |
| ✅ Backup Folder             | Copy folder to new timestamped backup |
| ✅ Log Extractor             | View System, Application, or Security logs from the last X days |
| ✅ Disk Usage Monitor        | Show disk space used in GB and percentage |
| ✅ Temp File Cleaner         | Clean `%TEMP%`, `C:\Windows\Temp`, and `Prefetch` |
| ✅ Network Info Viewer       | Shows IP, MAC, Gateway + Wi-Fi SSID and password |

 🧰 Requirements
- Windows 10/11
- Admin privileges for full functionality (especially logs & Wi-Fi keys)
- PowerShell enabled (included by default in Windows)


 🛠️ How to Use
1. Download `IT_Tools.bat`
2. Right-click > Run as Administrator
3. Use the menu to navigate the toolkit

 🔒 Notes
- Wi-Fi password feature only shows currently connected network
- Log reader uses PowerShell (`Get-WinEvent`)
- For sending email or advanced tasks, check [Python Version](https://github.com/...)

 📄 License
MIT

---

Created with ❤️ by [Hossam Yosri](https://www.linkedin.com/in/hossamyosri)
