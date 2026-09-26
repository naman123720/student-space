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
    st.header("🎤 Presentation Editor")

    if "slides" not in st.session_state:
        st.session_state.slides = [1]

    if "current_slide" not in st.session_state:
        st.session_state.current_slide = 1

    # Sidebar tools
    st.sidebar.subheader("🎨 Presentation Tools")

    background = st.sidebar.color_picker(
        "Slide Background",
        "#FFFFFF"
    )

    text_color = st.sidebar.color_picker(
        "Text Color",
        "#000000"
    )

    font_size = st.sidebar.slider(
        "Font Size",
        12,
        60,
        30
    )

    # Slide controls
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ Add Slide"):
            st.session_state.slides.append(
                len(st.session_state.slides) + 1
            )
            st.rerun()

    with col2:
        if st.button("⬅️ Previous"):
            if st.session_state.current_slide > 1:
                st.session_state.current_slide -= 1
            st.rerun()

    with col3:
        if st.button("➡️ Next"):
            if st.session_state.current_slide < len(st.session_state.slides):
                st.session_state.current_slide += 1
            st.rerun()

    st.write(
        f"Slide {st.session_state.current_slide} "
        f"of {len(st.session_state.slides)}"
    )

    # Text boxes
    title = st.text_input(
        "📝 Add Title",
        placeholder="Type your title here..."
    )

    content = st.text_area(
        "📝 Add Text",
        placeholder="Type your content here...",
        height=150
    )

    # Slide preview
    st.subheader("👀 Slide Preview")

    slide_html = f"""
    <div style="
        background-color:{background};
        width:100%;
        min-height:400px;
        border:2px solid #333;
        padding:40px;
        text-align:center;
        color:{text_color};
    ">
        <h1 style="font-size:{font_size}px;">{title}</h1>
        <p style="font-size:20px;">{content}</p>
    </div>
    """

    st.markdown(slide_html, unsafe_allow_html=True)
