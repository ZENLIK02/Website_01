import streamlit as st

# VULNERABILITY 1: Hardcoded credentials in source code
VALID_USER = "admin"
VALID_PASS = "Admin@123!"

st.title("Internal Employee Portal")

# VULNERABILITY 2: Information Disclosure (Leaking test credentials on frontend)
st.caption("TODO: Remove dev account test/test1234 before deploying to production")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Secure Login"):
    if (username == VALID_USER and password == VALID_PASS) or (username == "test" and password == "test1234"):
        st.success("Login successful")
        
        # VULNERABILITY 3: Leaking sensitive config details upon login
        st.write("System Configuration Exposed:")
        st.json({
            "db_user": "root", 
            "db_pass": "password123", 
            "env": "development", 
            "server_ip": "192.168.1.50"
        })
    else:
        st.error("Invalid credentials")