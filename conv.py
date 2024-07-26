import streamlit as st
import subprocess
import os
import tempfile
import shutil

# Define helper functions
def convert_to_exe(py_file_path, output_dir, onefile, noconsole, icon_path, clean):
    # Prepare PyInstaller command
    options = []
    if onefile:
        options.append("--onefile")
    if noconsole:
        options.append("--noconsole")
    if icon_path:
        options.append(f"--icon={icon_path}")
    if clean:
        options.append("--clean")
    
    options_str = " ".join(options)
    command = f"pyinstaller {options_str} --distpath {output_dir} {py_file_path}"
    
    # Execute the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        return os.path.join(output_dir, os.path.splitext(os.path.basename(py_file_path))[0] + ".exe")
    else:
        st.error(f"Error during conversion:\n{result.stderr}")
        return None

# Streamlit UI
st.title("Python to EXE Converter")

# File upload
uploaded_file = st.file_uploader("Upload your Python (.py) file", type="py")
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    st.write("Python file uploaded successfully.")

    # Options
    st.sidebar.header("Options")
    onefile = st.sidebar.checkbox("One File", value=True)
    noconsole = st.sidebar.checkbox("No Console")
    icon_file = st.sidebar.file_uploader("Upload an Icon File (.ico)", type="ico")
    clean = st.sidebar.checkbox("Clean Build", value=True)

    if icon_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ico") as temp_icon_file:
            temp_icon_file.write(icon_file.read())
            icon_path = temp_icon_file.name
    else:
        icon_path = None

    if st.button("Convert to EXE"):
        with tempfile.TemporaryDirectory() as temp_output_dir:
            exe_path = convert_to_exe(temp_file_path, temp_output_dir, onefile, noconsole, icon_path, clean)
            if exe_path:
                with open(exe_path, "rb") as f:
                    st.download_button(
                        label="Download EXE",
                        data=f,
                        file_name=os.path.basename(exe_path),
                        mime="application/x-msdownload"
                    )
