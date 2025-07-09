# 🚀 DCbypass
DCbypass is a tool designed to test vulnerabilities in web applications by bypassing admin login using techniques commonly used by attackers. This tool helps in identifying and addressing security holes that allow bypassing the login page.

## 🎯 Purpose of Use
This tool is used to test web applications by exploiting weaknesses in the admin login authentication process. This tool is useful in the **penetration testing (pentest)** phase, specifically to find potential gaps in the application that can be used to gain unauthorized access to the system.

## ⚙️ Fitur Unggulan
- 🔐 **Bypass login**: Access the admin area by exploiting authentication weaknesses.
- 🧩 **Diverse payloads**: Support for various payload techniques to bypass login.
- 🛡️ **Different authentication methods**: Utilize techniques such as SQL Injection, CSRF bypass, and more.
- 🚀 **Speed & efficiency**: Fast execution to identify and resolve vulnerabilities.
- 📊 **Reporting of results**: Generates easy-to-read reports and logs for further analysis.

## 💡 Instalasi
**Download Tools**
```
git clone https://github.com/nantzzsec/DCbypass.git
```
**Install dependencies**
```
pip install -r requirements.txt --break-system-package
```
**Runing**
USE **dummyuser** and **dummypass** To check endpoint
```
python3 DCbypass.py -r 1.txt
```
**OR**
```
python3 DCbypass.py -u hackerone.com/login.php
```
## 💡 Cara Penggunaan
1. **intercept login page in burpsuite copy and create file 1.txt**
   
   ![image](https://github.com/nantzzsec/nantzzsec/blob/f7485a63220a2cda81923cc0838b6d1584d416f0/assets/DCbypass4.png)


## 📄 Lisensi
Proyek ini dilisensikan di bawah **MIT License**, yang berarti Anda dapat mendistribusikan dan memodifikasi proyek ini dengan mencantumkan kredit kepada saya.

## Connect with me:

<p align="left">

<a href = "[https://id.linkedin.com/in/gede-ananda-960699309]"><img src="https://img.icons8.com/fluent/48/000000/linkedin.png"/></a>
<a href = "[https://www.instagram.com/darkclownsec.id/]"><img src="https://img.icons8.com/fluent/48/000000/instagram-new.png"/></a>
<a href = "[https://www.gedeananda.com/]"><img src="https://img.icons8.com/color/48/itranslate.png"/></a>
<a href = "[https://www.tiktok.com/@accessdenied_error]"><img src="https://img.icons8.com/color/48/tiktok--v1.png"/></a>
</p>
