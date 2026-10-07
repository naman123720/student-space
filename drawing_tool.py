import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image


def drawing_tool():

    st.title("🎨 Student Space - Drawing Studio")
    st.write("Create diagrams, sketches and notes.")

    # Tool selection
    col1, col2, col3 = st.columns(3)

    with col1:
        tool = st.selectbox(
            "Tool",
            ["Pencil", "Brush", "Eraser"]
        )

    with col2:
        color = st.color_picker(
            "Color",
            "#000000"
        )

    with col3:
        size = st.slider(
            "Brush Size",
            1,
            50,
            5
        )

    # Configure selected tool
    if tool == "Pencil":
        drawing_mode = "freedraw"
        stroke_width = size
        stroke_color = color

    elif tool == "Brush":
        drawing_mode = "freedraw"
        stroke_width = size * 2
        stroke_color = color

    else:
        drawing_mode = "freedraw"
        stroke_width = size * 3
        stroke_color = "#FFFFFF"

    # Drawing canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="#FFFFFF",
        height=550,
        width=900,
        drawing_mode=drawing_mode,
        key="student_space_canvas",
    )

    # Download drawing
    try:
        if canvas_result.image_data is not None:

            image = Image.fromarray(
                canvas_result.image_data.astype("uint8")
            )

            image_bytes = image.convert("RGB").tobytes()

            st.download_button(
                label="📥 Download Drawing",
                data=image_bytes,
                file_name="student_space_drawing.png",
                mime="image/png"
            )

    except RuntimeError:
        pass
