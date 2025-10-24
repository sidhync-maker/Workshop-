import streamlit as st
import sqlite3
from datetime import datetime
import hashlib
import os
import pandas as pd

DB_PATH = "workshop.db"

# ----------------- Initialize session state -----------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# ----------------- Database helpers -----------------
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT,
            created_at TEXT
        )
    ''')
    # Additional tables: purchases, stock, billing, mechanics, car_models
    conn.commit()
    # Default manager
    c.execute("SELECT * FROM users WHERE role='manager'")
    if c.fetchone() is None:
        default_user = "manager"
        default_pass = "admin123"
        c.execute(
            "INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
            (default_user, hash_password(default_pass), "manager", datetime.utcnow().isoformat())
        )
        conn.commit()
    conn.close()

if not os.path.exists(DB_PATH):
    init_db()

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="Workshop Manager", layout="wide")
st.title("Workshop Management — Multi-user")

# ----------------- Login -----------------
if not st.session_state.logged_in:
    st.sidebar.header("Login")
    username_input = st.sidebar.text_input("Username")
    password_input = st.sidebar.text_input("Password", type="password")
    login_btn = st.sidebar.button("Login")
    
    if login_btn:
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username_input,))
        user = c.fetchone()
        conn.close()
        
        if user and hash_password(password_input) == user["password_hash"]:
            st.session_state.user = dict(user)
            st.session_state.logged_in = True
            st.success(f"Logged in as {username_input} ({user['role']})")
        else:
            st.error("Invalid credentials")
    
    st.stop()  # Stop until login

# ----------------- Navigation -----------------
role = st.session_state.user["role"]
username = st.session_state.user["username"]

st.sidebar.header("Navigation")
pages = ["Home", "Purchase", "Stock", "Billing", "Mechanics", "Car Models", "Export/Import"]
if role == "mechanic":
    pages = ["Home", "Mechanics"]

st.session_state.page = st.sidebar.selectbox("Module", pages, index=pages.index(st.session_state.page))
page = st.session_state.page

st.write(f"Logged in as **{username}** ({role})")
st.write(f"Module selected: **{page}**")
st.info("Modules logic (Purchase, Stock, Billing, Mechanics, Car Models) goes here.")
