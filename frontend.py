# frontend.py
import customtkinter as ctk
from backend import fetch_air_data, fetch_state_heatmap_data
import matplotlib.pyplot as plt

# ------------------ ORANGE SUNSET THEME ------------------
BG = "#0f0f0f"
TEXT = "#ffffff"
ACCENT = "#ff8e3c"
ACCENT_LIGHT = "#ffb997"

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Air Pollution Exposure Tracker and Agriculture Effects")
app.geometry("1000x780")
app.configure(fg_color=BG)

# ---------------- HEADER ----------------
title = ctk.CTkLabel(
    app,
    text="🌇 Air Pollution Exposure Tracker and Agriculture Effects",
    font=("Poppins", 28, "bold"),
    text_color=ACCENT_LIGHT
)
title.pack(pady=12)

subtitle = ctk.CTkLabel(
    app,
    text="Enter a city to get AQI, dashboard, recommendations, agriculture advice & heatmaps.",
    font=("Poppins", 15),
    text_color=ACCENT,
)
subtitle.pack()

# ---------------- INPUT FRAME ----------------
inp = ctk.CTkFrame(app, fg_color="#1b1b1b")
inp.pack(pady=15)

location_entry = ctk.CTkEntry(
    inp, width=350, height=40,
    fg_color="#111111", text_color=TEXT,
    placeholder_text="Enter Indian City…"
)
location_entry.pack(pady=10)

status_label = ctk.CTkLabel(inp, text="", text_color=ACCENT_LIGHT)
status_label.pack(pady=5)

# Store selected state
last_state = None

# ---------------- MAIN FETCH FUNCTION ----------------
def get_aqi():
    global last_state

    city = location_entry.get().strip()
    if city == "":
        status_label.configure(text="❌ Enter a valid city", text_color="red")
        return

    status_label.configure(text="Fetching…", text_color=ACCENT_LIGHT)
    app.update()

    result = fetch_air_data(city)

    if not result["success"]:
        status_label.configure(text="❌ " + result["error"], text_color="red")
        return

    aqi = result["aqi"]
    comp = result["components"]
    last_state = result["state"]

    # Update dashboard
    pm25_label.configure(text=f"PM2.5:\n{comp['pm2_5']}")
    pm10_label.configure(text=f"PM10:\n{comp['pm10']}")
    no2_label.configure(text=f"NO₂:\n{comp['no2']}")
    so2_label.configure(text=f"SO₂:\n{comp['so2']}")
    o3_label.configure(text=f"O₃:\n{comp['o3']}")
    co_label.configure(text=f"CO:\n{comp['co']}")
    aqi_label.configure(text=f"AQI:\n{aqi}")

    status_label.configure(text=f"Updated for {city.title()}", text_color=ACCENT)

    # Agriculture + Pollution advice
    rec_text.configure(state="normal")
    rec_text.delete("0.0", "end")

    final = f"AQI: {aqi}\n\nAgriculture Advice:\n{result['agriculture']}"
    rec_text.insert("0.0", final)
    rec_text.configure(state="disabled")

# ---------------- HEATMAP ----------------
def show_heatmap():
    if not last_state:
        status_label.configure(text="❌ Fetch AQI first", text_color="red")
        return

    data = fetch_state_heatmap_data(last_state)
    if not data:
        status_label.configure(text="❌ No data for this state", text_color="red")
        return

    cities = list(data.keys())
    aqi_vals = list(data.values())

    plt.figure(figsize=(9, 5))
    plt.title(f"Most Polluted Cities in {last_state.title()}", fontsize=16)

    plt.bar(cities, aqi_vals)
    plt.xticks(rotation=25)
    plt.xlabel("Cities")
    plt.ylabel("AQI")

    plt.tight_layout()
    plt.show()

# ---------------- BUTTONS ----------------
btn = ctk.CTkButton(app, text="Get Air Quality",
                    fg_color=ACCENT, hover_color=ACCENT_LIGHT,
                    text_color=TEXT, command=get_aqi)
btn.pack(pady=10)

heatmap_btn = ctk.CTkButton(app, text="Show State Heatmap",
                            fg_color="#ff6d0a", hover_color="#ffa86a",
                            text_color=TEXT, command=show_heatmap)
heatmap_btn.pack(pady=5)

# ---------------- DASHBOARD ----------------
dash = ctk.CTkFrame(app, fg_color="#1b1b1b")
dash.pack(pady=20)

pm25_label = ctk.CTkLabel(dash, text="PM2.5:\n--", font=("Poppins", 18), text_color=TEXT)
pm10_label = ctk.CTkLabel(dash, text="PM10:\n--", font=("Poppins", 18), text_color=TEXT)
no2_label = ctk.CTkLabel(dash, text="NO₂:\n--", font=("Poppins", 18), text_color=TEXT)
so2_label = ctk.CTkLabel(dash, text="SO₂:\n--", font=("Poppins", 18), text_color=TEXT)
o3_label = ctk.CTkLabel(dash, text="O₃:\n--", font=("Poppins", 18), text_color=TEXT)
co_label = ctk.CTkLabel(dash, text="CO:\n--", font=("Poppins", 18), text_color=TEXT)
aqi_label = ctk.CTkLabel(dash, text="AQI:\n--", font=("Poppins", 18, "bold"), text_color=ACCENT)

pm25_label.grid(row=0, column=0, padx=40, pady=15)
pm10_label.grid(row=0, column=1, padx=40, pady=15)
no2_label.grid(row=0, column=2, padx=40, pady=15)
so2_label.grid(row=1, column=0, padx=40, pady=15)
o3_label.grid(row=1, column=1, padx=40, pady=15)
co_label.grid(row=1, column=2, padx=40, pady=15)
aqi_label.grid(row=0, column=3, rowspan=2, padx=60, pady=15)

# ---------------- RECOMMENDATIONS ----------------
rec = ctk.CTkFrame(app, fg_color="#1b1b1b")
rec.pack(pady=10)

rec_title = ctk.CTkLabel(rec, text="AI Recommendations", font=("Poppins", 20, "bold"), text_color=ACCENT_LIGHT)
rec_title.pack(pady=8)

rec_text = ctk.CTkTextbox(rec, width=700, height=140, fg_color="#111111", text_color=TEXT)
rec_text.insert("0.0", "Enter a city to begin…")
rec_text.configure(state="disabled")
rec_text.pack(pady=10)

app.mainloop()
