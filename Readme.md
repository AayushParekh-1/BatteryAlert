# 🔋 Battery Guardian

> **Your laptop's personal health guardian.** A premium, lightweight desktop application that protects your battery from overcharging and deep discharging.

---

## 💡 What is Battery Guardian?

Most laptop batteries degrade faster when they are pushed to extremes—staying at 100% while plugged in or dropping below 20%. **Battery Guardian** sits quietly in your background and alerts you exactly when it's time to act.

### ✨ Key Features
- **🌍 Cross-Platform:** Native support for macOS (`afplay`), Windows (`winsound`), and Linux (`aplay`).
- **🎨 Premium UI:** Beautiful, dark-themed macOS-style popups with SF Pro typography.
- **🧠 Smart Alert Logic:** No notification spam! The app only alerts you when a threshold is crossed and resets only when the battery return to a safe range.
- **🎵 Audio Alerts:** Distinctive sound cues for "Plug In" and "Unplug" notifications.
- **🧵 Performance First:** Multithreaded architecture ensures it never slows down your machine.

---

## �️ Tech Stack

- **Python 3.x**
- **Tkinter** (for the modern GUI)
- **psutil** (for precise battery monitoring)
- **Subprocess** (for low-latency audio playback)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/battery-monitor.git
cd battery-monitor
```

### 2. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip3 install -r requirements.txt
```

### 3. Launch the App
```bash
python3 Batteries.py
```

---

## ⚙️ Configuration

The app is pre-configured with industry-standard healthy thresholds:
- **Low Battery Alert:** 20% (Red/Orange Warning)
- **Full Battery Alert:** 98% (Green Notification)
- **Check Interval:** Every 10 seconds (optimized for battery life)

*To customize these, simply edit the constants at the top of `Batteries.py`.*

---

## � Project Structure

- `Batteries.py`: The unified core application logic.
- `requirements.txt`: Project dependencies.
- `ChargeMe.wav`: Alert sound for low battery.
- `Charge-Remove.wav`: Alert sound for full battery.

---

## 🤝 Contributing

Found a bug or have a design suggestion? We'd love to see it!
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License
Built with ❤️ to keep your laptop healthy.
