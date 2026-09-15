import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── CONFIG ───────────────────────────────────────────────────────────────────
API_KEY = "2ed48550993d420483c45028261808"
CITIES  = ["London", "New York", "Tokyo", "Sydney", "Mumbai"]
# ─────────────────────────────────────────────────────────────────────────────

BASE_URL = "https://api.weatherapi.com/v1/current.json"


def fetch_weather(city: str) -> dict | None:
    """Fetch current weather for a single city from weatherapi.com."""
    params = {"key": API_KEY, "q": city, "aqi": "no"}
    resp = requests.get(BASE_URL, params=params, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    print(f"  [!] Could not fetch {city} — {resp.status_code}: {resp.json().get('error', {}).get('message')}")
    return None


def parse_weather(data: dict) -> dict:
    """Extract the fields we care about from the weatherapi.com response."""
    loc = data["location"]
    cur = data["current"]
    return {
        "City":         loc["name"],
        "Country":      loc["country"],
        "Temperature":  cur["temp_c"],
        "Feels Like":   cur["feelslike_c"],
        "Humidity (%)": cur["humidity"],
        "Pressure":     cur["pressure_mb"],
        "Wind Speed":   cur["wind_kph"],
        "Visibility":   cur["vis_km"],
        "UV Index":     cur["uv"],
        "Condition":    cur["condition"]["text"],
        "Last Updated": cur["last_updated"],
    }


# ── FETCH ─────────────────────────────────────────────────────────────────────
print("Fetching weather data...\n")
records = []
for city in CITIES:
    raw = fetch_weather(city)
    if raw:
        records.append(parse_weather(raw))
        print(f"  ✓ {city}")

if not records:
    raise SystemExit("No data fetched — check your API key or city names.")

df = pd.DataFrame(records).set_index("City")

# ── DISPLAY ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("             CURRENT WEATHER SUMMARY")
print("=" * 65)
print(df[["Country", "Temperature", "Feels Like", "Humidity (%)",
          "Wind Speed", "Condition"]].to_string())

print("\n── Quick Stats ──────────────────────────────────────────────")
numeric = df[["Temperature", "Feels Like", "Humidity (%)", "Wind Speed", "Pressure"]]
print(numeric.describe().round(2))

print(f"\n  Hottest  : {df['Temperature'].idxmax()} ({df['Temperature'].max():.1f}°C)")
print(f"  Coldest  : {df['Temperature'].idxmin()} ({df['Temperature'].min():.1f}°C)")
print(f"  Windiest : {df['Wind Speed'].idxmax()} ({df['Wind Speed'].max():.1f} kph)")
print(f"  Humidest : {df['Humidity (%)'].idxmax()} ({df['Humidity (%)'].max():.0f}%)")
print(f"  Highest UV: {df['UV Index'].idxmax()} (UV {df['UV Index'].max()})")

# ── VISUALIZE ─────────────────────────────────────────────────────────────────
cities = df.index.tolist()
colors = plt.cm.tab10.colors[:len(cities)]

fig = plt.figure(figsize=(16, 10))
fig.suptitle("Current Weather Dashboard — weatherapi.com",
             fontsize=15, fontweight="bold")
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

# 1. Temperature vs Feels Like
ax1 = fig.add_subplot(gs[0, 0])
x = range(len(cities))
w = 0.35
ax1.bar([i - w/2 for i in x], df["Temperature"], w, label="Actual",     color=colors)
ax1.bar([i + w/2 for i in x], df["Feels Like"],  w, label="Feels Like", color=colors, alpha=0.5)
ax1.set_title("Temperature vs Feels Like (°C)")
ax1.set_xticks(list(x)); ax1.set_xticklabels(cities, rotation=20, ha="right")
ax1.set_ylabel("°C"); ax1.legend()

# 2. Humidity
ax2 = fig.add_subplot(gs[0, 1])
bars = ax2.bar(cities, df["Humidity (%)"], color=colors)
ax2.set_title("Humidity (%)"); ax2.set_ylabel("%"); ax2.set_ylim(0, 115)
ax2.set_xticklabels(cities, rotation=20, ha="right")
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f"{bar.get_height():.0f}%", ha="center", fontsize=9)

# 3. Wind Speed
ax3 = fig.add_subplot(gs[0, 2])
ax3.barh(cities, df["Wind Speed"], color=colors)
ax3.set_title("Wind Speed (kph)"); ax3.set_xlabel("kph")

# 4. Pressure
ax4 = fig.add_subplot(gs[1, 0])
ax4.plot(cities, df["Pressure"], marker="o", color="steelblue", linewidth=2, markersize=8)
ax4.fill_between(cities, df["Pressure"], alpha=0.15, color="steelblue")
ax4.set_title("Pressure (hPa)"); ax4.set_ylabel("hPa")
ax4.tick_params(axis="x", rotation=20)

# 5. Visibility
ax5 = fig.add_subplot(gs[1, 1])
ax5.bar(cities, df["Visibility"], color=colors)
ax5.set_title("Visibility (km)"); ax5.set_ylabel("km")
ax5.set_xticklabels(cities, rotation=20, ha="right")

# 6. Temperature ranking
ax6 = fig.add_subplot(gs[1, 2])
sorted_df = df["Temperature"].sort_values()
ax6.barh(sorted_df.index, sorted_df.values,
         color=[colors[cities.index(c)] for c in sorted_df.index])
ax6.set_title("Temperature Ranking (°C)"); ax6.set_xlabel("°C")
for i, v in enumerate(sorted_df.values):
    ax6.text(v + 0.2, i, f"{v:.1f}°", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("weather_dashboard.png", dpi=150, bbox_inches="tight")
print("\nChart saved → weather_dashboard.png")
plt.show()
