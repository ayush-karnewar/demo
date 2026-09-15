import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── LOAD CREDENTIALS ─────────────────────────────────────────────────────────
with open("credentials.json") as f:
    creds = json.load(f)

CLIENT_ID     = creds["clientId"]
CLIENT_SECRET = creds["clientSecret"]

# ── FETCH TOKEN ───────────────────────────────────────────────────────────────
print("Authenticating with OpenSky Network...")

token_resp = requests.post(
    "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token",
    data={
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type":    "client_credentials",
    },
    timeout=15,
)

if token_resp.status_code != 200:
    raise SystemExit(f"Auth failed ({token_resp.status_code}): {token_resp.text}")

access_token = token_resp.json()["access_token"]
print("  ✓ Token obtained\n")

# ── FETCH LIVE FLIGHT DATA ────────────────────────────────────────────────────
print("Fetching live flight states...")

headers = {"Authorization": f"Bearer {access_token}"}
resp = requests.get(
    "https://opensky-network.org/api/states/all",
    headers=headers,
    timeout=20,
)

if resp.status_code != 200:
    raise SystemExit(f"API error ({resp.status_code}): {resp.text}")

data = resp.json()
states = data.get("states", [])

if not states:
    raise SystemExit("No flight data returned.")

print(f"  ✓ {len(states)} flights received\n")

# ── BUILD DATAFRAME ───────────────────────────────────────────────────────────
columns = [
    "icao24", "callsign", "origin_country", "time_position", "last_contact",
    "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
    "true_track", "vertical_rate", "sensors", "geo_altitude",
    "squawk", "spi", "position_source"
]

df = pd.DataFrame(states, columns=columns)

# Clean up
df["callsign"]      = df["callsign"].str.strip()
df["baro_altitude"] = pd.to_numeric(df["baro_altitude"], errors="coerce")
df["velocity"]      = pd.to_numeric(df["velocity"],      errors="coerce")
df["latitude"]      = pd.to_numeric(df["latitude"],      errors="coerce")
df["longitude"]     = pd.to_numeric(df["longitude"],     errors="coerce")
df["vertical_rate"] = pd.to_numeric(df["vertical_rate"], errors="coerce")

# Drop rows without position
df = df.dropna(subset=["latitude", "longitude"])

# Airborne vs on-ground
airborne = df[df["on_ground"] == False]
on_ground = df[df["on_ground"] == True]

# ── DISPLAY ───────────────────────────────────────────────────────────────────
print("=" * 60)
print("         LIVE FLIGHT DATA — OpenSky Network")
print("=" * 60)
print(f"  Total flights tracked : {len(df)}")
print(f"  Airborne              : {len(airborne)}")
print(f"  On ground             : {len(on_ground)}")

print("\n── Top 10 Flights (by altitude) ─────────────────────────────")
top10 = (
    airborne[["callsign", "origin_country", "baro_altitude", "velocity", "vertical_rate"]]
    .dropna(subset=["baro_altitude"])
    .sort_values("baro_altitude", ascending=False)
    .head(10)
)
print(top10.to_string(index=False))

print("\n── Top 10 Countries by Active Flights ───────────────────────")
country_counts = airborne["origin_country"].value_counts().head(10)
print(country_counts.to_string())

print("\n── Altitude Stats (airborne, metres) ────────────────────────")
print(airborne["baro_altitude"].describe().round(1).to_string())

print("\n── Speed Stats (airborne, m/s) ──────────────────────────────")
print(airborne["velocity"].describe().round(1).to_string())

# ── VISUALIZE ─────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 12))
fig.suptitle("Live Flight Dashboard — OpenSky Network", fontsize=15, fontweight="bold", color="black")

# ── 1. WORLD MAP ──────────────────────────────────────────────────────────────
ax_map = fig.add_subplot(2, 2, (1, 2))  # spans top row

# simple world outline via scatter colours
ax_map.set_facecolor("white")
fig.patch.set_facecolor("white")

# colour by altitude
alt_norm = airborne["baro_altitude"].fillna(0)
sc = ax_map.scatter(
    airborne["longitude"], airborne["latitude"],
    c=alt_norm, cmap="plasma",
    s=1.5, alpha=0.7, linewidths=0,
)

# on-ground dots
ax_map.scatter(
    on_ground["longitude"], on_ground["latitude"],
    color="green", s=1, alpha=0.6, label="On ground"
)

cbar = plt.colorbar(sc, ax=ax_map, fraction=0.02, pad=0.01)
cbar.set_label("Altitude (m)", color="black", fontsize=9)
cbar.ax.yaxis.set_tick_params(color="black")
plt.setp(cbar.ax.yaxis.get_ticklabels(), color="black")

ax_map.set_xlim(-180, 180)
ax_map.set_ylim(-90, 90)
ax_map.set_title("Real-time Flight Map", color="black", fontsize=12)
ax_map.set_xlabel("Longitude", color="black")
ax_map.set_ylabel("Latitude",  color="black")
ax_map.tick_params(colors="black")
for spine in ax_map.spines.values():
    spine.set_edgecolor("black")

legend_patch = mpatches.Patch(color="green", label="On ground")
ax_map.legend(handles=[legend_patch], loc="lower left",
              facecolor="white", labelcolor="black", fontsize=8)

# ── 2. TOP COUNTRIES BAR ──────────────────────────────────────────────────────
ax_country = fig.add_subplot(2, 2, 3)
colors = plt.cm.tab10.colors[:len(country_counts)]
bars = ax_country.barh(country_counts.index[::-1], country_counts.values[::-1], color=colors[::-1])
ax_country.set_title("Top 10 Countries — Airborne Flights")
ax_country.set_xlabel("Number of Flights")
for bar in bars:
    ax_country.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                    str(int(bar.get_width())), va="center", fontsize=8)

# ── 3. ALTITUDE HISTOGRAM ─────────────────────────────────────────────────────
ax_alt = fig.add_subplot(2, 2, 4)
airborne["baro_altitude"].dropna().plot.hist(
    bins=40, color="steelblue", edgecolor="black", alpha=0.85, ax=ax_alt
)
ax_alt.set_title("Altitude Distribution (Airborne)", color="black")
ax_alt.set_xlabel("Altitude (m)", color="black")
ax_alt.set_ylabel("Number of Flights", color="black")
ax_alt.tick_params(colors="black")

ax_country.set_title("Top 10 Countries — Airborne Flights", color="black")
ax_country.set_xlabel("Number of Flights", color="black")
ax_country.tick_params(colors="black")

plt.tight_layout()
plt.savefig("flights_dashboard.png", dpi=150, bbox_inches="tight")
print("\nChart saved → flights_dashboard.png")
plt.show()
