# streamlit_app.py
import streamlit as st
from app.auth import AuthManager
from app.db import create_db_and_tables, get_session
from app.sample_data import ensure_sample_data
from app.update_sanctions import update_all_sources_ui
from app.matching import run_single_screening_ui
from app.ai_integration import ai_review_ui


st.set_page_config(page_title="NIUM Screening (Demo)", layout="wide")


# initialize DB and sample data
create_db_and_tables()
ensure_sample_data()


auth = AuthManager()


if "user" not in st.session_state:
st.session_state.user = None


# --- Login ---
if st.session_state.user is None:
st.title("NIUM Screening — Login")
with st.form("login_form"):
username = st.text_input("Username")
password = st.text_input("Password", type="password")
submitted = st.form_submit_button("Login")
if submitted:
user = auth.authenticate(username, password)
if user:
st.session_state.user = user
st.experimental_rerun()
else:
st.error("Invalid username or password")


else:
st.sidebar.write(f"Logged in as: {st.session_state.user['username']}")
if st.sidebar.button("Logout"):
st.session_state.user = None
st.experimental_rerun()


page = st.sidebar.selectbox("Menu", [
"Dashboard",
"Single Screening",
"Bulk Screening",
"Update Sanctions DB",
"Admin: Sanctions Sources",
"AI Review",
])


if page == "Dashboard":
st.header("Dashboard — Summary")
st.write("(Demo) Summary metrics are shown from DB.")
# simple metrics
from app.db import get_metrics
metrics = get_metrics()
cols = st.columns(4)
cols[0].metric("Total Screenings", metrics['screenings'])
ai_review_ui(st, st.session_state.user)
