# ✋ Morse Hand Translator

Translator bahasa isyarat sederhana berbasis **Morse Code** menggunakan **kamera + Mediapipe + OpenCV**.  
Dengan mengangkat jari:  

- ☝️ **Telunjuk saja** = titik (`.`)  
- ✌️ **Telunjuk + Tengah** = garis (`-`)  

Kalau berhenti **2 detik** → otomatis decode ke huruf.  
Kalau idle **5 detik** → teks kalimat direset.  

---

## 🚀 Fitur
- Input morse pakai **gerakan jari**.  
- Real-time dengan **kamera**.  
- Translasi ke huruf A-Z dan angka 0-9.  
- Reset otomatis kalau idle.  
- Tampilan hasil di pojok kiri atas kamera.  

---

## 📦 Instalasi & Setup

### 1. Clone Repo
```bash
git clone https://github.com/anonymous-1-id/morse-translator.git
cd morse-hand-translator
```

---

### 2. Virtual Environment

---
### Windows
```bash
python -m venv venv
venv\Scripts\activate
```
### Linux/MacOs
```bash
python3 -m venv venv
source venv/bin/activate
```
---

### 3. Install Depencies
```bash
pip install --upgrade pip
pip install opencv-python mediapipe numpy
```

---

### 4. Running
```bash
python morse-translator.py
```
