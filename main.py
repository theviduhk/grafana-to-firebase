import requests
import json
import datetime
import firebase_admin
from firebase_admin import credentials, db

# ------------------------------
# 1. Firebase Initialize
# ------------------------------
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://grafana-27a10-default-rtdb.firebaseio.com/'
})

# ------------------------------
# 2. Grafana Dashboard Data URL (public view or direct API JSON)
# ------------------------------
GRAFANA_URL = "https://monitor.trax-cloud.com/d/uPJ9-4CGk/hourly-report-team-leaders?orgId=18&var-selected_projects=All&var-task_name=All&var-tl_name=G14923-OTL&var-staff_id=All&var-template_name=All&var-Other_ID=G21337&from=now%2Fd&to=now"

# OPTIONAL: If your Grafana instance requires login
USERNAME = "gss.colombo@gssintl.biz"
PASSWORD = "GSS_Trax@24Sep"

# ------------------------------
# 3. Get Data from Grafana
# ------------------------------
try:
    response = requests.get(GRAFANA_URL, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        data = response.text  # If HTML or JSON

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Push to Firebase under /grafana_logs
        db.reference("/grafana_logs").push({
            "timestamp": now,
            "data": data
        })

        print("✅ Grafana data pushed to Firebase successfully.")

    else:
        print(f"❌ Failed to fetch Grafana data: Status {response.status_code}")

except Exception as e:
    print(f"❌ Error occurred: {str(e)}")
