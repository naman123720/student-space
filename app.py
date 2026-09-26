import streamlit as st 
from supabase import create_client
SUPABASE_URL=st.secrets["SUPABASE_URL"]
SUPABASE_KEY=st.secrets["SUPABASE_KEY"]
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

    st.subheader("📂 Your Saved Files")

    try:
        files = supabase.storage.from_("student-files").list()
        st.write(files)

        if files:
            for file in files:
                file_name = file["name"]
                st.write(f"📄 {file_name}")

                try:
                    file_data = supabase.storage.from_("student-files").download(file_name)

                    st.download_button(
                        label=f"⬇️ Download {file_name}",
                        data=file_data,
                        file_name=file_name
                    )

                except Exception as e:
                    st.error(f"Could not download {file_name}: {e}")
        else:
            st.info("No files saved yet.")

    except Exception as e:
        st.error(f"Could not load files: {e}")

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
    st.write("Create and edit your presentation.")

    if "slides" not in st.session_state:
        st.session_state.slides = [
            {"title": "My First Slide", "content": "Write your content here..."}
        ]

    st.subheader("➕ Create a Presentation")

    presentation_name = st.text_input(
        "Presentation Name",
        value="My Presentation"
    )

    for i, slide in enumerate(st.session_state.slides):
        st.markdown(f"### Slide {i + 1}")

        slide["title"] = st.text_input(
            "Slide Title",
            value=slide["title"],
            key=f"title_{i}"
        )

        slide["content"] = st.text_area(
            "Slide Content",
            value=slide["content"],
            height=150,
            key=f"content_{i}"
        )

    if st.button("➕ Add New Slide"):
        st.session_state.slides.append(
            {
                "title": f"Slide {len(st.session_state.slides) + 1}",
                "content": "Write your content here..."
            }
        )
        st.rerun()

    st.divider()

    st.subheader("👀 Presentation Preview")

    for i, slide in enumerate(st.session_state.slides):
        st.markdown(f"## Slide {i + 1}: {slide['title']}")
        st.write(slide["content"])
        st.divider()

    st.success("✅ Your presentation is ready!")
st.divider()

st.subheader("⬇️ Download Presentation")

presentation_text = f"Presentation: {presentation_name}\n\n"

for i, slide in enumerate(st.session_state.slides):
    presentation_text += f"SLIDE {i + 1}\n"
    presentation_text += f"Title: {slide['title']}\n"
    presentation_text += f"Content: {slide['content']}\n\n"

st.download_button(
    label="⬇️ Download Presentation",
    data=presentation_text,
    file_name=f"{presentation_name}.txt",
    mime="text/plain"
)
