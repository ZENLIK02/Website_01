import streamlit as st
import subprocess
import sqlite3
import hashlib
import pickle
import yaml
import requests

# VULNERABILITY 1: Hardcoded Secrets
# Semgrep rule: python.lang.security.audit.hardcoded-password
DB_PASSWORD = "super_secret_db_password_123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE" 
JWT_SECRET = "jwt_secret_for_demo_only_please_rotate"

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

# VULNERABILITY 5: Cross-site Scripting (unsafe HTML rendering)
st.header("4. Profile Preview (XSS)")
display_name = st.text_input("Display name:")
if st.button("Preview profile"):
    st.markdown(f"<h3>Hello {display_name}</h3>", unsafe_allow_html=True)

# VULNERABILITY 6: Code Injection with eval
st.header("5. Calculator (Code Injection)")
formula = st.text_input("Formula:", value="1 + 2")
if st.button("Calculate"):
    result = eval(formula)
    st.write(f"Result: {result}")

# VULNERABILITY 7: Unsafe Deserialization
st.header("6. Import Backup (Unsafe Pickle)")
backup_file = st.file_uploader("Upload backup file", type=["pkl", "pickle"])
if st.button("Import backup") and backup_file is not None:
    backup = pickle.loads(backup_file.getvalue())
    st.write(backup)

# VULNERABILITY 8: Unsafe YAML Load
st.header("7. YAML Config Loader")
yaml_config = st.text_area("YAML config:", value="role: admin")
if st.button("Load config"):
    config = yaml.load(yaml_config, Loader=yaml.Loader)
    st.write(config)

# VULNERABILITY 9: Disabled TLS Verification
st.header("8. Fetch URL (TLS Verification Disabled)")
remote_url = st.text_input("Remote URL:", value="https://example.com")
if st.button("Fetch remote URL"):
    response = requests.get(remote_url, verify=False, timeout=5)
    st.write(response.text[:500])
