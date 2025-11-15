
# 🚑 **Rapid Response EMS — Intelligent Emergency Dispatch System**

*Graph-based ETA engine • Smart Ambulance Assignment • Hospital Bed Checking • Driver Live Tracking*

---

## 📌 **Overview**

**Rapid Response EMS** is a full-stack emergency dispatch system built with **Flask + Vanilla JS**, designed to:

* Register emergency incidents
* Assign the *best ambulance* using **Dijkstra shortest path algorithm**
* Estimate arrival time (ETA) using graph distances
* Check nearest hospitals + bed availability
* Track driver’s live GPS on the dashboard
* Provide separate dashboards for **Users** and **Drivers**

The system chooses the optimal ambulance and hospital based on:

* Distance (graph-calculated)
* Severity of emergency
* ICU/emergency facility availability
* Real-time ambulance & driver status

---

# 🏗 **Project Structure**

```
project/
│
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py          <-- login/signup
│   │   ├── dashboard.py     <-- user dashboard
│   │   ├── emergency.py     <-- incident creation + dispatch logic
│   │   ├── driver.py        <-- driver dashboard & GPS updates
│   ├── utils/
│   │   ├── graph.py         <-- Dijkstra algorithm + graph builder
│   │   ├── hospital_check.py
│   │   └── seed_data.py
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── emergency_form.html
│   ├── driver_dashboard.html
│
├── static/
│   ├── css/style.css
│   ├── js/auth.js
│   ├── js/dashboard.js
│   ├── js/emergency.js
│   ├── js/driver.js
│
├── seed.py
└── run.py
```

---

# ⚙️ **Features**

### ### **1️⃣ Authentication**

* User signup/login
* Driver login
* Session-based authentication
* Redirects based on role

---

### **2️⃣ Emergency Registration**

User fills:

* Name
* Location (GPS auto-detected)
* Severity (critical/high/medium/low)
* Description

Front-end calls:
`POST /api/emergency`

---

### **3️⃣ Dispatch Engine (Core Logic)**

The backend:

✔ Builds a graph of

* Ambulances
* Incident
* Hospitals

✔ Runs **Dijkstra’s Algorithm** for each ambulance
✔ Computes route cost & ETA
✔ Evaluates severity
✔ Finds nearest hospital with:

* Emergency department
* Available beds

✔ Assigns:

* Best ambulance
* Best driver
* Best hospital

---

### **4️⃣ Driver Dashboard**

Driver sees:

* Assigned incident
* Route info
* Maps with live ambulance GPS
* ETA
* Patient location

Driver sends updates:
`POST /api/driver/update_location`

---

### **5️⃣ User Dashboard**

User sees:

* Assigned ambulance
* Driver info
* Live ambulance location
* ETA
* Hospital assigned

---

# 🛠 **Setup Instructions**

## **1️⃣ Create Virtual Environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## **2️⃣ Install Dependencies**

### **Flask Essentials**

```bash
pip install flask flask_sqlalchemy flask_bcrypt flask_login flask_cors
```

### **Backend Tools**

```bash
pip install python-dotenv geopy
```

---

## **3️⃣ Initialize Database**

```bash
python seed.py
```

This creates:

* Users
* Drivers
* Ambulances
* Hospitals

---

## **4️⃣ Run Server**

```bash
python run.py
```

App runs at:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

# 🧠 **How the Dispatch Algorithm Works**

## **Graph Construction**

Each ambulance, hospital, and the incident becomes a **node**:

```
AMB-1  ————<
             >—— INCIDENT —— HOSP-1
AMB-2  ————<
```

Edges contain:

* Road distance (km)
* Weighted travel cost

---

## **Dijkstra Algorithm**

Located in:
📁 `app/utils/graph.py`

Used to compute:

* Shortest route from ambulance → incident
* Shortest route from incident → hospital

---

## **Hospital Selection**

Module:
📁 `app/utils/hospital_check.py`

Logic:

1. Sort hospitals by distance
2. Check:

   * Emergency department?
   * ICU?
   * Available beds?
3. If nearest is full → pick second nearest
4. Auto fallback mechanism

---

## **ETA Calculation**

```
ETA = distance(km) / avg_speed
```

Speed default: **60 km/h**
Fully customizable.

---

# 🧪 **Testing Guide**

You should test:

### ✔ Authentication

* Wrong password
* Missing fields
* Session expiration

### ✔ Emergency Form

* Missing GPS
* All severity levels

### ✔ Dispatch Logic

* No ambulances available
* No hospitals available
* Out-of-range distances

### ✔ Driver Dashboard

* Live GPS
* API updates
* Route refresh

### ✔ Background Load

* Multiple incidents
* Priority assignment
* Graph performance

---

# 🖼 **Screenshots (Suggested to Add)**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue" />
  <img src="https://img.shields.io/badge/Framework-Flask-green" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
  <img src="https://img.shields.io/badge/Build-Passing-brightgreen" />
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey" />
</p>



Add images in README:

* Login page
* User dashboard
* Emergency form
* Driver dashboard
* Real-time map

---

# 🔮 **Future Improvements**

Some cool features you can add:

* Real-time WebSocket GPS
* AI-based ambulance prediction
* Traffic-aware ETA (Google/OSRM)
* Panic-button mobile app
* Admin control dashboard
* Driver shift scheduling
* Multi-language support

---

# 🏁 **Conclusion**

This system gives you:

✔ Real dispatch logic
✔ Real hospital fallback
✔ Real graph algorithm
✔ Real driver GPS tracking
