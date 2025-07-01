import requests
import json
import datetime
import firebase_admin
from firebase_admin import credentials, db

# ------------------------------
# 1. Firebase Initialize
# ------------------------------
cred = credentials.Certificate("firebase_key.json")  # <-- JSON key path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-id.firebaseio.com/'  # <-- replace this
})

# ------------------------------
# 2. Grafana Panel API URL
# ------------------------------
GRAFANA_URL = "https://monitor.trax-cloud.com/d/uPJ9-4CGk/hourly-report-team-leaders?orgId=18&var-selected_projects=All&var-task_name=All&var-tl_name=G8112-OTL&var-staff_id=All&var-template_name=All&var-Other_ID=G21337&from=now%2Fd&to=now&refresh=20m"

# OPTIONAL: If your Grafana requires login
USERNAME = "gss.colombo@gssintl.biz"
PASSWORD = "GSS_Trax@24Sep"

# ------------------------------
# 3. Get Data from Grafana
# ------------------------------
response = requests.get(GRAFANA_URL, auth=(USERNAME, PASSWORD))

if response.status_code == 200:
    data = response.text  # If it's raw HTML/JS panel

    # ✅ Save full response (as string or parse if JSON)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.reference("/grafana_reports").push({
        "timestamp": now,
        "raw_data": data  # If possible, convert this to dict
    })

    print("✅ Data pushed to Firebase.")
else:
    print(f"❌ Failed to fetch Grafana data: {response.status_code}")
