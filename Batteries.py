import tkinter as tk   #For Making the GUI popups
from tkinter import messagebox    #For startUp info popup
import psutil       #To get the information about the battery!
import threading    #To run the monitoring in the background and giving the asynchronous nature to these code!
import time         #for delays that are there between the popups
import sys          # For exiting on error or interrupt
import subprocess   # To play sound using afplay
import os           # To check if sound files exist
import platform     # To check the OS type

# --- Constants ---
LOW_BATTERY_THRESHOLD = 20
FULL_BATTERY_THRESHOLD = 98
CHECK_INTERVAL = 10  # Reduced frequency to save resources

# -- Sound Files ---
LOW_BATTERY_SOUND = 'ChargeMe.wav'
FULL_BATTERY_SOUND = 'Charge-Remove.wav'

class BatteryMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        
        # Performance & State
        self.running = True
        self.alert_low_shown = False     
        self.alert_full_shown = False    
        self.os_type = platform.system()

    def _get_resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def play_sound(self, sound_file):
        sound_path = self._get_resource_path(sound_file)
        if not os.path.exists(sound_path):
            print(f"[Warning] Sound file not found: {sound_path}")
            return

        try:
            if self.os_type == "Darwin":  # macOS
                subprocess.Popen(['afplay', sound_path])
            elif self.os_type == "Windows":
                import winsound
                winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif self.os_type == "Linux":
                subprocess.Popen(['aplay', sound_path])
        except Exception as e:
            print(f"[Sound Error] Failed to play {sound_file}: {e}")

    def show_popup(self, title, message, color="#FF3B30"):
        """ Display a premium-styled popup message """
        def popup():
            top = tk.Toplevel()
            top.title(title)
            top.geometry("400x200")
            top.resizable(False, False)
            top.configure(bg="#1C1C1E")  # Dark background (macOS style)
            
            # Center on screen
            window_width = 400
            window_height = 200
            screen_width = top.winfo_screenwidth()
            screen_height = top.winfo_screenheight()
            center_x = int(screen_width/2 - window_width / 2)
            center_y = int(screen_height/2 - window_height / 2)
            top.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

            top.attributes("-topmost", True)
            
            # Premium Styling
            main_frame = tk.Frame(top, bg="#1C1C1E", padx=20, pady=20)
            main_frame.pack(expand=True, fill="both")

            icon_label = tk.Label(main_frame, text="⚠️", font=("Arial", 40), bg="#1C1C1E", fg=color)
            icon_label.pack(pady=(0, 10))

            msg_label = tk.Label(
                main_frame, 
                text=message, 
                font=("SF Pro Display", 14, "bold"), 
                bg="#1C1C1E", 
                fg="white", 
                wraplength=350
            )
            msg_label.pack()

            close_btn = tk.Button(
                main_frame, 
                text="Dismiss", 
                command=top.destroy,
                bg=color,
                fg="white",
                font=("SF Pro Display", 12, "bold"),
                highlightthickness=0,
                bd=0,
                padx=20,
                pady=10,
                cursor="hand2"
            )
            close_btn.pack(pady=(20, 0))

            # Auto-close after 10 seconds
            top.after(10000, top.destroy)

        self.root.after(0, popup)

    def monitor_battery(self):
        print(f"[*] Battery monitoring started on {self.os_type}...")
        while self.running:
            try:
                battery = psutil.sensors_battery()
                if battery is None:
                    time.sleep(CHECK_INTERVAL)
                    continue

                percent = battery.percent
                plugged = battery.power_plugged

                # Logic for alerts
                if percent <= LOW_BATTERY_THRESHOLD and not plugged:
                    if not self.alert_low_shown:
                        self.show_popup("Low Battery", f"Battery is at {percent}%. Please connect your charger.", color="#FF9500")
                        self.play_sound(LOW_BATTERY_SOUND)
                        self.alert_low_shown = True
                        self.alert_full_shown = False # Reset full alert if we're now low
                
                elif percent >= FULL_BATTERY_THRESHOLD and plugged:
                    if not self.alert_full_shown:
                        self.show_popup("Battery Full", f"Battery is at {percent}%. Please remove the charger to protect battery health.", color="#34C759")
                        self.play_sound(FULL_BATTERY_SOUND)
                        self.alert_full_shown = True
                        self.alert_low_shown = False
                
                else:
                    # Reset flags when battery is in safe range
                    if percent > LOW_BATTERY_THRESHOLD + 5:
                        self.alert_low_shown = False
                    if percent < FULL_BATTERY_THRESHOLD - 5:
                        self.alert_full_shown = False

            except Exception as e:
                print(f"[Error] Monitoring loop encountered an issue: {e}")

            time.sleep(CHECK_INTERVAL)

    def start(self):
        # Initial greeting
        messagebox.showinfo("Battery Monitor", "🔋 Battery Guardian is now active in the background.\n\nWe'll alert you when it's time to plug or unplug.")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_battery, daemon=True)
        monitor_thread.start()
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print("[!] Stopping Battery Guardian...")
        self.running = False
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    monitor = BatteryMonitor()
    try:
        monitor.start()
    except Exception as e:
        print(f"[Fatal] {e}")
        sys.exit(1)