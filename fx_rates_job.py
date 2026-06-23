import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import time

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres123@localhost:5432/mydatabase"
)

API_KEY = "6744b2db7d6073e4c614772c"
url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/EUR"

while True:
    now = datetime.now()

    # STOP CONDITION (after 13:00)
    if now.hour >= 13:
        print("Stopped: reached 13:00")
        break

    # START CONDITION (before 09:00, wait)
    if now.hour < 9:
        print("Waiting for 09:00...")
        time.sleep(60)
        continue

    # -----------------------------
    # API CALL
    # -----------------------------
    response = requests.get(url)

    if response.status_code != 200:
        print("API failed:", response.status_code)
        time.sleep(300)
        continue

    data = response.json()

    if data.get("result") != "success":
        print("API error:", data)
        time.sleep(300)
        continue

    rates = data.get("conversion_rates", {})

    # -----------------------------
    # SNAPSHOT ROW (HISTORICAL DATA)
    # -----------------------------
    row = {
        "timestamp": now,
        "date": now.date(),
        "hour": now.hour,
        "EUR_USD": rates.get("USD"),
        "EUR_GBP": rates.get("GBP"),
        "EUR_CNY": rates.get("CNY"),
        "EUR_KES": rates.get("KES")
    }

    df = pd.DataFrame([row])

    try:
        df.to_sql(
            "fx_rates_history",
            engine,
            if_exists="append",
            index=False
        )
        print("Inserted:", now)

    except Exception as e:
        print("DB error:", e)

    # -----------------------------
    # WAIT BETWEEN SAMPLES (10 MINUTES)
    # -----------------------------
    time.sleep(600)