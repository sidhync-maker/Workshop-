# Workshop Management Streamlit App

This is a Streamlit web app for managing a small vehicle workshop.
It includes modules for purchases, stock, billing, mechanics, and car models,
with a manager account and multiple mechanics users. Data is stored in SQLite.

## Files
- app.py        : main Streamlit app
- requirements.txt : Python dependencies
- README.md     : usage instructions
- workshop.db   : created automatically after first run (SQLite DB)

## Run locally
1. Install dependencies:
   pip install -r requirements.txt
2. Run the app:
   streamlit run app.py
3. Open the URL Streamlit prints (usually http://localhost:8501)

## Default manager account
- username: manager
- password: admin123

Change the password after first login.
