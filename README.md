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
pip install -r requirements.txt
```

## 💡 Cara Penggunaan
1. **intercept login page di burpsuite copy dan buatkan file 1.txt**
   
   ![image](https://github.com/nantzzsec/nantzzsec/blob/f7485a63220a2cda81923cc0838b6d1584d416f0/assets/DCbypass4.png)

3. **Masukkan payload yang digunakan untuk bypass login**:
   Sesuaikan parameter username dan password pada bagian -U dan -P
   ```
   python3 DCbypass.py -r 1.txt -w word.txt -U uname -P pass
   ```
   ![image](https://github.com/nantzzsec/nantzzsec/blob/f7485a63220a2cda81923cc0838b6d1584d416f0/assets/DCbypass1.png)

5. **Lakukan uji bypass pada form login** dengan mengirimkan payload yang sesuai dan memeriksa respons server.
   ![image](https://github.com/nantzzsec/nantzzsec/blob/f7485a63220a2cda81923cc0838b6d1584d416f0/assets/DCbypass2.png)
   

7. **Hasil Akhir**: Alat ini akan menampilkan hasil uji bypass login dan memberikan informasi terkait potensi celah yang ditemukan.
   ![image](https://github.com/nantzzsec/nantzzsec/blob/f7485a63220a2cda81923cc0838b6d1584d416f0/assets/DCbypass3.png)

## 📄 Lisensi
Proyek ini dilisensikan di bawah **MIT License**, yang berarti Anda dapat mendistribusikan dan memodifikasi proyek ini dengan mencantumkan kredit kepada saya.
