import streamlit as st

st.set_page_config(
    page_title="Student Space",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Space")
st.write("Your digital workspace for college.")

st.divider()

option = st.selectbox(
    "Choose an option",
    ["🏠 Home", "📁 My Files", "📊 My Projects", "🎤 Presentations"]
)

if option == "🏠 Home":
    st.header("Welcome to Student Space")
    st.write(
        "Student Space helps students create, manage and access "
        "their academic work."
    )

elif option == "📁 My Files":
    st.header("📁 My Files")
    st.write("Upload your college files here.")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "pptx", "xlsx", "png", "jpg", "jpeg", "txt"]
    )

    if uploaded_file is not None:
        st.success(f"{uploaded_file.name} uploaded successfully!")
        st.download_button(
            "⬇️ Download File",
            data=uploaded_file.getvalue(),
            file_name=uploaded_file.name
        )

elif option == "📊 My Projects":
    st.header("📊 My Projects")
    st.info("Your projects will appear here.")

elif option == "🎤 Presentations":
    st.header("🎤 Presentations")
    st.info("Your presentations will appear here.")
