# backend.py
import pandas as pd
import random

# ----------------- LOAD CITY DATABASE -----------------
try:
    df = pd.read_csv("Indian Cities Database.csv")
    df.columns = df.columns.str.strip().str.lower()   # normalize
except:
    raise FileNotFoundError(
        "❌ Could not load Indian Cities Database.csv. Place it in the same folder."
    )

# Required columns:
# city, state
if "city" not in df.columns or "state" not in df.columns:
    raise ValueError("❌ CSV must contain 'city' and 'state' columns.")


# ----------- RANDOM AIR QUALITY & POLLUTANT SIMULATION -----------
def generate_aqi():
    return random.randint(1, 5)  # AQI scale


def generate_components():
    return {
        "pm2_5": round(random.uniform(5, 180), 1),
        "pm10": round(random.uniform(10, 250), 1),
        "no2": round(random.uniform(5, 120), 1),
        "so2": round(random.uniform(2, 80), 1),
        "o3": round(random.uniform(10, 180), 1),
        "co": round(random.uniform(0.1, 2.5), 2),
    }


# ---------------------- MAIN FUNCTION USED BY FRONTEND ----------------------
def fetch_air_data(city_name: str):
    city_name = city_name.strip().lower()

    # match city from CSV
    match = df[df["city"].str.lower() == city_name]

    if match.empty:
        return {
            "success": False,
            "error": f"'{city_name.title()}' is not found in India."
        }

    state = match.iloc[0]["state"]

    aqi = generate_aqi()
    comp = generate_components()

    # ---------------- AGRICULTURE RECOMMENDATIONS ----------------
    if aqi >= 4:
        agriculture = (
            "⚠ Air quality is harmful for crops.\n"
            "- Avoid sowing leafy vegetables\n"
            "- Use shade nets & increase irrigation\n"
            "- Best crops now: mustard, millet, barley\n"
            "- Monitor plant stress daily"
        )

    elif aqi == 3:
        agriculture = (
            "🙂 Moderate conditions.\n"
            "- Suitable for wheat, beans, sugarcane\n"
            "- Check leaves for yellowing or spots\n"
            "- Maintain regular irrigation"
        )

    else:
        agriculture = (
            "🌱 Excellent air for crops.\n"
            "- Good for rice, wheat, vegetables\n"
            "- Ideal time for sowing & germination\n"
            "- High yield potential this week"
        )

    return {
        "success": True,
        "city": city_name,
        "state": state,
        "aqi": aqi,
        "components": comp,
        "agriculture": agriculture
    }


# ---------------------- HEATMAP DATA FUNCTION ----------------------
def fetch_state_heatmap_data(state_name: str):
    """Returns AQI for all cities of a state — for heatmap."""
    subset = df[df["state"].str.lower() == state_name.lower()]

    result = {}
    for _, row in subset.iterrows():
        result[row["city"]] = generate_aqi()

    return result
