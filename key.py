import tkinter as tk
import time
import pandas as pd

class KeystrokeLogger:
    def __init__(self, master):
        self.master = master
        self.master.title("Keystroke Logger - Parkinson's Detection")
        self.label = tk.Label(master, text="Type the sentence:\n\nThe quick brown fox jumps over the lazy dog", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(master, width=80, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.focus_set()

        self.start_time = None
        self.keystrokes = []
        self.press_times = {}

        self.entry.bind("<KeyPress>", self.on_key_press)
        self.entry.bind("<KeyRelease>", self.on_key_release)

        self.done_button = tk.Button(master, text="Done", command=self.save_data)
        self.done_button.pack(pady=10)

    def on_key_press(self, event):
        key = event.keysym
        self.press_times[key] = time.perf_counter()

        if self.start_time is None:
            self.start_time = self.press_times[key]

    def on_key_release(self, event):
        key = event.keysym
        release_time = time.perf_counter()
        press_time = self.press_times.get(key, release_time)
        dwell_time = release_time - press_time

        self.keystrokes.append({
            'key': key,
            'press_time': press_time,
            'release_time': release_time,
            'dwell_time': dwell_time
        })

    def save_data(self):
        df = pd.DataFrame(self.keystrokes)
        df.to_csv("keystroke_data.csv", index=False)

        
        dwell_times = df['dwell_time']
        total_time = df['release_time'].iloc[-1] - self.start_time
        num_chars = len(df)

        avg_dwell = dwell_times.mean()
        avg_flight = df['press_time'].iloc[1:].values - df['release_time'].iloc[:-1].values
        avg_flight_time = avg_flight.mean()
        typing_speed = num_chars / total_time
        key_variance = dwell_times.var()

        features = {
            "avg_dwell_time": round(avg_dwell * 1000, 2),
            "avg_flight_time": round(avg_flight_time * 1000, 2),
            "typing_speed": round(typing_speed, 2),
            "key_press_variance": round(key_variance * 1000, 2)
        }

        pd.DataFrame([features]).to_csv("keystroke_features.csv", index=False)
        print("Keystroke features saved to keystroke_features.csv")
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = KeystrokeLogger(root)
    root.mainloop()
