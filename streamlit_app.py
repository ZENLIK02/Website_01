import streamlit as st
import subprocess
import sqlite3
import hashlib

# VULNERABILITY 1: Hardcoded Secrets
# Semgrep rule: python.lang.security.audit.hardcoded-password
DB_PASSWORD = "super_secret_db_password_123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE" 

st.title("Vulnerable App for SAST (Semgrep)")

# VULNERABILITY 2: SQL Injection (SQLi)
st.header("1. User Search (SQLi)")
username_search = st.text_input("Search Username:")
if st.button("Search"):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'admin'), (2, 'testuser')")
    
    # Semgrep rule: python.lang.security.audit.sqli.sqlite3-sqli
    query = f"SELECT * FROM users WHERE name = '{username_search}'"
    try:
        cursor.execute(query) 
        st.write(cursor.fetchall())
    except Exception as e:
        st.error(f"Error: {e}")

# VULNERABILITY 3: Command Injection
st.header("2. Network Diagnostic (Command Injection)")
target_ip = st.text_input("Enter IP to ping (e.g., 8.8.8.8):")
if st.button("Ping"):
    # Semgrep rule: python.lang.security.audit.subprocess-shell-true
    command = f"ping -c 1 {target_ip}"
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        st.code(result)
    except Exception as e:
        st.error("Ping failed")

# VULNERABILITY 4: Weak Cryptography (MD5)
st.header("3. Hash Generator (Weak Crypto)")
password_input = st.text_input("Enter text to hash:", type="password")
if st.button("Hash"):
    # Semgrep rule: python.lang.security.audit.insecure-hash-algorithms
    hasher = hashlib.md5() 
    hasher.update(password_input.encode('utf-8'))
    st.write(f"MD5 Hash: {hasher.hexdigest()}")