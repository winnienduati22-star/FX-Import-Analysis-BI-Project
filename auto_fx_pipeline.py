import time
import os
from datetime import datetime

print("Starting FX data pipeline...")

# run until 13:00 (1pm)
while datetime.now().hour < 13:
    print("Running FX job at:", datetime.now())

    os.system("python fx_rates_job.py")

    print("Completed run. Waiting 5 minutes...\n")

    time.sleep(300)  # 5 minutes

print("Pipeline finished at 1pm")