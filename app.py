import streamlit as st
from supabase import create_client
from drawing_tool import drawing_tool

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Student Space",
    page_icon="🎓",
    layout="wide"
)

# =========================
# SUPABASE CONNECTION
# =========================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =========================
# LOGIN / SIGN UP
# =========================

if "user" not in st.session_state:
    st.session_state.user = None


if st.session_state.user is None:

    st.title("🎓 Student Space")
    st.write("Your digital workspace for college.")
    st.divider()

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    # =========================
    # LOGIN
    # =========================

    with login_tab:

        st.subheader("🔐 Student Login")

        email = st.text_input(
            "📧 Email",
            key="login_email"
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if not email or not password:
                st.warning(
                    "Please enter your email and password."
                )

            else:
                try:

                    response = supabase.auth.sign_in_with_password(
                        {
                            "email": email,
                            "password": password
                        }
                    )

                    if response.user:

                        st.session_state.user = response.user

                        st.success(
                            "✅ Login successful!"
                        )

                        st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Login failed: {e}"
                    )

    # =========================
    # SIGN UP
    # =========================

    with signup_tab:

        st.subheader("📝 Create Student Account")

        signup_email = st.text_input(
            "📧 Email",
            key="signup_email"
        )

        signup_password = st.text_input(
            "🔑 Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "🔑 Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not signup_email or not signup_password:
                st.warning(
                    "Please enter an email and password."
                )

            elif signup_password != confirm_password:
                st.error(
                    "❌ Passwords do not match."
                )

            elif len(signup_password) < 6:
                st.warning(
                    "Password should be at least 6 characters."
                )

            else:

                try:

                    response = supabase.auth.sign_up(
                        {
                            "email": signup_email,
                            "password": signup_password
                        }
                    )

                    if response.user:

                        st.success(
                            "✅ Account created successfully!"
                        )

                        st.info(
                            "📧 Check your email for a verification link if email verification is enabled."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Account creation failed: {e}"
                    )

    st.stop()


# =========================
# LOGGED-IN USER
# =========================

user = st.session_state.user

# =========================
# HEADER
# =========================

st.title("🎓 Student Space")

st.write(
    "Your digital workspace for college."
)

st.success(
    f"👤 Logged in as: {user.email}"
)

# =========================
# LOGOUT
# =========================

if st.button("🚪 Logout"):

    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    st.session_state.user = None
    st.rerun()

st.divider()

# =========================
# NAVIGATION
# =========================

option = st.selectbox(
    "Choose an option",
    [
        "🏠 Home",
        "📁 My Files",
        "📊 My Projects",
        "🎤 Presentations",
        "🎨 Drawing Studio"
    ]
)

# =========================
# HOME
# =========================

if option == "🏠 Home":

    st.header(
        "Welcome to Student Space 👋"
    )

    st.write(
        "Student Space helps students create, "
        "manage and access their academic work."
    )

    st.info(
        "💡 Your Student Space account is now protected by Supabase Authentication."
    )


# =========================
# MY FILES
# =========================

elif option == "📁 My Files":

    st.header("📁 My Files")

    st.write(
        "Upload your college files here."
    )

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=[
            "pdf",
            "docx",
            "pptx",
            "xlsx",
            "png",
            "jpg",
            "jpeg",
            "txt"
        ]
    )

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        try:

            # Store files inside the logged-in user's folder
            file_path = (
                f"{user.id}/{uploaded_file.name}"
            )

            supabase.storage.from_(
                "student-files"
            ).upload(
                file_path,
                file_bytes
            )

            st.success(
                f"✅ {uploaded_file.name} saved successfully!"
            )

        except Exception as e:

            st.error(
                f"Upload failed: {e}"
            )

    st.subheader(
        "📂 Your Saved Files"
    )

    try:

        files = supabase.storage.from_(
            "student-files"
        ).list(
            str(user.id)
        )

        if files:

            for file in files:

                file_name = file["name"]

                st.write(
                    f"📄 {file_name}"
                )

                try:

                    file_path = (
                        f"{user.id}/{file_name}"
                    )

                    file_data = (
                        supabase.storage
                        .from_("student-files")
                        .download(file_path)
                    )

                    st.download_button(
                        label=f"⬇️ Download {file_name}",
                        data=file_data,
                        file_name=file_name
                    )

                except Exception as e:

                    st.error(
                        f"Could not download {file_name}: {e}"
                    )

        else:

            st.info(
                "No files saved yet."
            )

    except Exception as e:

        st.error(
            f"Could not load files: {e}"
        )


# =========================
# MY PROJECTS
# =========================

elif option == "📊 My Projects":

    st.header("📊 My Projects")

    st.subheader(
        "➕ Add a New Project"
    )

    project_name = st.text_input(
        "Project Name"
    )

    project_description = st.text_area(
        "Project Description"
    )

    if st.button(
        "Add Project"
    ):

        if project_name and project_description:

            st.success(
                f"Project '{project_name}' added successfully!"
            )

            st.write(
                "### Project Details"
            )

            st.write(
                f"**Name:** {project_name}"
            )

            st.write(
                f"**Description:** {project_description}"
            )

        else:

            st.warning(
                "Please enter both project name and description."
            )


# =========================
# PRESENTATIONS
# =========================

elif option == "🎤 Presentations":

    st.header(
        "🎤 Presentation Editor"
    )

    if "slides" not in st.session_state:
        st.session_state.slides = [1]

    if "current_slide" not in st.session_state:
        st.session_state.current_slide = 1

    # Sidebar tools

    st.sidebar.subheader(
        "🎨 Presentation Tools"
    )

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

        if st.button(
            "➕ Add Slide"
        ):

            st.session_state.slides.append(
                len(st.session_state.slides) + 1
            )

            st.rerun()

    with col2:

        if st.button(
            "⬅️ Previous"
        ):

            if st.session_state.current_slide > 1:

                st.session_state.current_slide -= 1

            st.rerun()

    with col3:

        if st.button(
            "➡️ Next"
        ):

            if st.session_state.current_slide < len(
                st.session_state.slides
            ):

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

    st.subheader(
        "👀 Slide Preview"
    )

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

        <h1 style="
            font-size:{font_size}px;
        ">
            {title}
        </h1>

        <p style="
            font-size:20px;
        ">
            {content}
        </p>

    </div>
    """

    st.markdown(
        slide_html,
        unsafe_allow_html=True
    )


# =========================
# DRAWING STUDIO
# =========================

elif option == "🎨 Drawing Studio":

    drawing_tool()
