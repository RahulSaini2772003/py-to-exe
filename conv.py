import streamlit as st
import os

def select_file():
    file_path = st.file_uploader("Select Python File", type=["py"])
    if file_path is not None:
        return file_path.name
    return ""

def select_icon():
    icon_path = st.file_uploader("Select Icon File", type=["ico"])
    if icon_path is not None:
        return icon_path.name
    return ""

def select_output_dir():
    return st.text_input("Output Directory", value=os.getcwd())

def convert_to_exe(py_file, icon_file, output_dir, onefile, noconsole, clean):
    if not py_file.endswith(".py"):
        st.error("Please select a Python file (.py)")
        return

    output_name = os.path.splitext(os.path.basename(py_file))[0]

    options = []

    if onefile:
        options.append("--onefile")
    if noconsole:
        options.append("--noconsole")
    if icon_file:
        options.append("--icon=" + icon_file)
    if clean:
        options.append("--clean")

    options_str = " ".join(options)
    command = f"pyinstaller {options_str} {py_file}"
    st.write(f"Command: {command}")

    os.chdir(output_dir)
    os.system(command)
    os.chdir(os.path.dirname(__file__))

    st.success("Conversion completed!")

st.title(".PY to .EXE Converter")

py_file = select_file()
output_dir = select_output_dir()

st.write("Options:")
onefile = st.checkbox("One File", value=True)
noconsole = st.checkbox("No Console", value=False)
clean = st.checkbox("Clean Build", value=True)

icon_file = select_icon()

if st.button("Convert to .exe"):
    convert_to_exe(py_file, icon_file, output_dir, onefile, noconsole, clean)
