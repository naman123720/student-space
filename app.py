import streamlit as st

st.set_page_config(
    page_title="Student Space",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Space")
st.subheader("A digital space for students without laptops")

st.write(
    "Student Space helps students create, save and access "
    "their academic work from college computers."
)

st.divider()

st.header("Welcome to Student Space")

st.info("Your student workspace is ready!")

st.button("📁 My Files")
st.button("📊 My Projects")
st.button("🎤 Presentations")
