# 🚀 DCbypass
DCbypass adalah sebuah alat yang dirancang untuk menguji kerentanannya dalam aplikasi web dengan cara bypass login admin menggunakan teknik-teknik yang umum digunakan oleh penyerang. Alat ini membantu dalam mengidentifikasi dan mengatasi celah keamanan yang memungkinkan bypass pada halaman login.

## 🎯 Tujuan Penggunaan
Alat ini digunakan untuk menguji aplikasi web dengan mengeksploitasi kelemahan dalam proses autentikasi login admin. Alat ini berguna dalam fase **pengetesan penetrasi (pentest)**, khususnya untuk menemukan potensi celah pada aplikasi yang dapat digunakan untuk mendapatkan akses tidak sah ke sistem.

## ⚙️ Fitur Unggulan
- 🔐 **Bypass login**: Mengakses area admin dengan mengeksploitasi kelemahan autentikasi.
- 🧩 **Payload beragam**: Dukungan untuk berbagai teknik payload untuk bypass login.
- 🛡️ **Metode autentikasi berbeda**: Memanfaatkan teknik-teknik seperti SQL Injection, bypass CSRF, dan lainnya.
- 🚀 **Kecepatan & efisiensi**: Eksekusi cepat untuk mengidentifikasi dan mengatasi kerentanannya.
- 📊 **Laporan hasil**: Menghasilkan laporan dan log yang mudah dibaca untuk analisis lebih lanjut.

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
1. **intercept login page di burpsuite copy dan buatkan file 1.txt
   - USE **dummyuser** and **dummypass** To check endpoint (example: uname=dummyuser&pass=dummypass)
   
   ![image](https://github.com/nantzzsec/nantzzsec/blob/f7485a63220a2cda81923cc0838b6d1584d416f0/assets/DCbypass4.png)

3. **Masukkan payload yang digunakan untuk bypass login**:
   Sesuaikan parameter username dan password pada bagian -U dan -P
   ```
   python3 DCbypass.py -r 1.txt -w wordlist.txt -U uname -P pass
   ```
   ![image](https://github.com/nantzzsec/nantzzsec/blob/f7485a63220a2cda81923cc0838b6d1584d416f0/assets/DCbypass1.png)

5. **Lakukan uji bypass pada form login** dengan mengirimkan payload yang sesuai dan memeriksa respons server.
   ![image](https://github.com/nantzzsec/nantzzsec/blob/f7485a63220a2cda81923cc0838b6d1584d416f0/assets/DCbypass2.png)
   

7. **Hasil Akhir**: Alat ini akan menampilkan hasil uji bypass login dan memberikan informasi terkait potensi celah yang ditemukan.
   ![image](https://github.com/nantzzsec/nantzzsec/blob/f7485a63220a2cda81923cc0838b6d1584d416f0/assets/DCbypass3.png)

## 📄 Lisensi
Proyek ini dilisensikan di bawah **MIT License**, yang berarti Anda dapat mendistribusikan dan memodifikasi proyek ini dengan mencantumkan kredit kepada saya.

## Connect with me:

<p align="left">

<a href = "[https://id.linkedin.com/in/gede-ananda-960699309]"><img src="https://img.icons8.com/fluent/48/000000/linkedin.png"/></a>
<a href = "[https://www.instagram.com/darkclownsec.id/]"><img src="https://img.icons8.com/fluent/48/000000/instagram-new.png"/></a>
<a href = "[https://www.gedeananda.com/]"><img src="https://img.icons8.com/color/48/itranslate.png"/></a>
<a href = "[https://www.tiktok.com/@accessdenied_error]"><img src="https://img.icons8.com/color/48/tiktok--v1.png"/></a>
</p>
