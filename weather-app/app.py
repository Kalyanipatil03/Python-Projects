import datetime
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Weather Code Mapping to Icons and Conditions
WEATHER_CODES = {
    0: ("Clear Sky", "fa-sun", "text-amber-400"),
    1: ("Mainly Clear", "fa-cloud-sun", "text-amber-300"),
    2: ("Partly Cloudy", "fa-cloud-sun", "text-slate-300"),
    3: ("Overcast", "fa-cloud", "text-slate-400"),
    45: ("Foggy", "fa-smog", "text-slate-400"),
    48: ("Depositing Rime Fog", "fa-smog", "text-slate-400"),
    51: ("Light Drizzle", "fa-cloud-rain", "text-cyan-400"),
    61: ("Slight Rain", "fa-cloud-showers-heavy", "text-blue-400"),
    63: ("Moderate Rain", "fa-cloud-showers-heavy", "text-blue-500"),
    65: ("Heavy Rain", "fa-cloud-showers-heavy", "text-blue-600"),
    71: ("Slight Snow", "fa-snowflake", "text-sky-200"),
    95: ("Thunderstorm", "fa-bolt", "text-purple-400"),
}


def get_coordinates(city_name):
    """Fetch latitude and longitude for a city name."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get("results"):
            loc = res["results"][0]
            return {
                "name": loc.get("name"),
                "country": loc.get("country", ""),
                "lat": loc["latitude"],
                "lon": loc["longitude"],
            }
    except Exception as e:
        print(f"Geocoding Error: {e}")
    return None


def get_weather_data(lat, lon):
    """Fetch current conditions and daily forecasts."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset"
        f"&timezone=auto"
    )
    try:
        res = requests.get(url, timeout=5).json()
        return res
    except Exception as e:
        print(f"Weather API Error: {e}")
        return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    city = request.form.get("city", "").strip()
    if not city:
        return redirect(url_for("index"))
    return redirect(url_for("result", city=city))


@app.route("/weather")
def result():
    city = request.args.get("city", "London")
    location = get_coordinates(city)

    if not location:
        return render_template("index.html", error=f"City '{city}' not found. Please try again.")

    weather_raw = get_weather_data(location["lat"], location["lon"])
    if not weather_raw or "current" not in weather_raw:
        return render_template("index.html", error="Failed to fetch weather data.")

    current = weather_raw["current"]
    daily = weather_raw["daily"]

    code = current.get("weather_code", 0)
    cond_desc, cond_icon, cond_color = WEATHER_CODES.get(
        code, ("Cloudy", "fa-cloud", "text-slate-300")
    )

    # Process 5-day daily forecast
    forecast = []
    for i in range(min(5, len(daily["time"]))):
        day_date = datetime.datetime.strptime(daily["time"][i], "%Y-%m-%d").strftime("%a, %b %d")
        d_code = daily["weather_code"][i]
        d_desc, d_icon, d_color = WEATHER_CODES.get(d_code, ("Cloudy", "fa-cloud", "text-slate-300"))

        forecast.append(
            {
                "date": day_date,
                "max_temp": round(daily["temperature_2m_max"][i]),
                "min_temp": round(daily["temperature_2m_min"][i]),
                "icon": d_icon,
                "color": d_color,
                "condition": d_desc,
            }
        )

    sunrise = datetime.datetime.fromisoformat(daily["sunrise"][0]).strftime("%I:%M %p")
    sunset = datetime.datetime.fromisoformat(daily["sunset"][0]).strftime("%I:%M %p")

    weather_data = {
        "city": location["name"],
        "country": location["country"],
        "temp": round(current["temperature_2m"]),
        "feels_like": round(current["apparent_temperature"]),
        "humidity": current["relative_humidity_2m"],
        "wind_speed": round(current["wind_speed_10m"], 1),
        "pressure": round(current["surface_pressure"]),
        "condition": cond_desc,
        "icon": cond_icon,
        "color": cond_color,
        "sunrise": sunrise,
        "sunset": sunset,
        "forecast": forecast,
    }

    return render_template("result.html", data=weather_data)


if __name__ == "__main__":
    app.run(debug=True)