import streamlit as st
import os

def save_to_txt(data, filename):
    with open(filename, 'w') as f:
        for item in data:
            f.write("%s\n" % item)

def main():
    st.title("Data Saver")

    data = st.text_area("Enter data here (one item per line):", height=200)
 # Prompt user to choose directory
    default_dir = os.path.expanduser('~')
    save_dir = st.text_input("Enter save directory path here")
    if st.button("Save to .txt file"):
        lines = data.split('\n')
        filename = st.text_input("Enter filename:", "data.txt")
        
       
        
        if save_dir is not None:
            save_path = os.path.join(save_dir, filename)
            save_to_txt(lines, save_path)
            st.success(f"Data saved to {save_path}")

if __name__ == "__main__":
    main()