import streamlit as st
from supabase import create_client
SUPABASE_URL=st.secrets["https://ypxkpfuhawjnccmqaxvv.supabase.co"]
SUPABASE_URL=st.secrets["sb_publishable_CN4LpskLdT5XolWHDxyCLQ_n_8yiuXh"]
supabase= create_client(SUPABASE_URL, SUPABASE_KEY)
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
        file_bytes = uploaded_file.getvalue()

        try:
            supabase.storage.from_("student-files").upload(
                uploaded_file.name,
                file_bytes
            )

            st.success(f"✅ {uploaded_file.name} saved permanently!")

        except Exception as e:
            st.error(f"Upload failed: {e}")

elif option == "📊 My Projects":
    st.header("📊 My Projects")

    st.subheader("➕ Add a New Project")

    project_name = st.text_input("Project Name")
    project_description = st.text_area("Project Description")

    if st.button("Add Project"):
        if project_name and project_description:
            st.success(f"Project '{project_name}' added successfully!")
            st.write("### Project Details")
            st.write(f"**Name:** {project_name}")
            st.write(f"**Description:** {project_description}")
        else:
            st.warning("Please enter both project name and description.")

elif option == "🎤 Presentations":
    st.header("🎤 Presentations")

    st.write("Upload your presentation and access it when you need to present.")

    presentation = st.file_uploader(
        "Choose your presentation",
        type=["pptx", "pdf"]
    )

    if presentation is not None:
        st.success(f"{presentation.name} uploaded successfully!")

        st.download_button(
            "⬇️ Download Presentation",
            data=presentation.getvalue(),
            file_name=presentation.name
        )
