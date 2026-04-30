# 🪨 Clay Analysis Website

> A web-based application built with **Flask** and **PostgreSQL** to monitor, input, and analyze clay (tanah liat) stock data across mining sites at **PT Semen Indonesia**.

---

## 📖 About This Project

Clay Analysis Website is an internal data management system that allows operators to input daily clay stock data per shift, per mining site. The system automatically calculates stock levels, estimates how many production shifts remain before clay runs out, and generates **automatic warnings** when stock is critically low.

The application covers **4 active mining sites (Tuban 1–4)** and tracks two clay types: **High Alumina (HAL)** and **Low Alumina (LAL)**.

---

## ✨ Key Features

- 📥 **Per-shift data input** for clay stock across 4 Tuban mining sites
- 🟡 **High Alumina & Low Alumina** clay tracking, each managed independently
- 📊 **Open Yard (OPY)** stock calculation — distributes crusher output per active location
- ⚠️ **Automatic WARNING** triggered when stock is estimated to run out within ≤ 14 production shifts
- 🔢 **Estimated depletion** counter — calculates how many shifts of clay remain
- 🎯 **Minimum next-shift target** recommendation to keep production on track
- 📈 **Visualization page** for data monitoring
- 💾 **PostgreSQL integration** — all data saved directly to the `tanah_liat` database

---

## 🗂️ Project Structure

```
Clay-Analysis-Website/
│
├── app.py                  ← Main Flask application (routes & business logic)
├── models.py               ← SQLAlchemy database model definitions
├── flask.exe               ← Flask executable
├── psycopg2-*.whl          ← PostgreSQL adapter (offline install)
│
└── templates/              ← HTML pages
    ├── homepage.html       ← Landing page
    ├── openyard.html       ← Open Yard daily data input
    ├── lokasicrusher.html  ← Crusher location overview
    ├── tuban1.html         ← Tuban 1 clay input form
    ├── tuban2.html         ← Tuban 2 clay input form
    ├── tuban3.html         ← Tuban 3 clay input form
    ├── tuban4.html         ← Tuban 4 clay input form
    └── visualisasi.html    ← Data visualization page
```

---

## 🔗 Application Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage |
| `/home` | GET/POST | Open Yard data input |
| `/submit_index` | POST | Save Open Yard data to database |
| `/index2` | GET/POST | Crusher location page |
| `/tuban1` | GET/POST | Tuban 1 clay stock input & calculation |
| `/tuban2` | GET/POST | Tuban 2 clay stock input & calculation |
| `/tuban3` | GET/POST | Tuban 3 clay stock input & calculation |
| `/tuban4` | GET/POST | Tuban 4 clay stock input & calculation |
| `/visualisasi` | GET/POST | Data visualization |

---

## 🗄️ Database Schema

The application uses **PostgreSQL** with the database named `tanah_liat`.

| Table | Description |
|-------|-------------|
| `index` | Open Yard daily data: date, shift, target, OPY high/low, active locations |
| `tuban1` | Clay stock data for Tuban 1 site |
| `tuban2` | Clay stock data for Tuban 2 site |
| `tuban3` | Clay stock data for Tuban 3 site |
| `tuban4` | Clay stock data for Tuban 4 site |

Each `tuban` table stores: `mining_date`, `shift`, `permpro_high_al`, `permpro_low_al`, `stok_storage_hal`, `stok_storage_lal`, `tambang_hal`, `tambang_lal`, `hari_habis_hal`, `hari_habis_lal`, `warning_hal`, `warning_lal`, `target_lanjut_hal`, `target_lanjut_lal`.

---

## 🛠️ Tech Stack

| Technology | Role |
|------------|------|
| **Python** | Backend logic (60%) |
| **Flask** | Web framework |
| **SQLAlchemy** | ORM for database interaction |
| **PostgreSQL** | Relational database |
| **psycopg2** | PostgreSQL adapter for Python |
| **HTML** | Frontend templates (40%) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- PostgreSQL installed and running
- Virtual environment (`myenv`)

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/Chelseaayu/Clay-Analysis-Website.git
   cd Clay-Analysis-Website
   ```

2. **Activate the virtual environment**
   ```bash
   # Windows
   myenv\Scripts\activate

   # macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask_sqlalchemy
   pip install psycopg2-2.8.6-cp36-cp36m-win_amd64.whl
   ```

4. **Set up the PostgreSQL database**

   Create a database named `tanah_liat` in PostgreSQL:
   ```sql
   CREATE DATABASE tanah_liat;
   ```

   Update the connection string in `app.py` if needed:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:<your_password>@localhost/tanah_liat'
   ```

5. **Initialize the database tables**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open in browser**
   ```
   http://localhost:5000
   ```

---

## 📋 How to Use

1. **Start at the Open Yard page** (`/home`) — input daily OPY High/Low values, production target, shift, and number of active crusher locations. This data is used as the base for all site calculations.

2. **Go to each Tuban site page** (`/tuban1` to `/tuban4`) — input the clay stock data per shift, including storage stock, mining output, and crusher output for both High and Low Alumina types.

3. **The system automatically calculates:**
   - Total stock (storage + crusher output)
   - Production surplus/deficit vs. target
   - Estimated shifts before stock depletion
   - A warning message if stock will run out within 14 shifts
   - Recommended minimum tonnage for the next shift

4. **Check the Visualization page** (`/visualisasi`) to monitor trends across all sites.

---

## ⚠️ Warning System Logic

| Condition | Result |
|-----------|--------|
| Estimated depletion ≤ 14 shifts | ⚠️ **WARNING** message generated |
| `permpro` = 0 | Displayed as "Tidak ada produksi" |
| Estimated depletion > 45 shifts | Treated as 0 (stock sufficient) |

---

## 👩‍💻 Author

**Chelsea Ayu**
- GitHub: [@Chelseaayu](https://github.com/Chelseaayu)

---

## 📄 License

This project was developed for operational use at **PT Semen Indonesia**. All rights reserved.
