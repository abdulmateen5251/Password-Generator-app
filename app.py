import streamlit as st
import random 
import string


def generate_password(length, use_digits, use_special_chars):
    characters = string.ascii_letters

    if use_digits:
        characters += string.digits #add digits to the characters (0-9) if selected

    if use_special_chars:
        characters += string.punctuation #add special characters to the characters (e.g., !, @, #, $, %, ^, &, *)

    return ''.join(random.choice(characters) for _ in range(length)) #join the characters to form a password


st.title("Password Generator")

length = st.slider("Select the length of the password", min_value=8, max_value=32, value=16)

use_digits = st.checkbox("Include digits")

use_special_chars = st.checkbox("Include special characters")


if st.button("Generate Password"):
    password = generate_password(length, use_digits, use_special_chars)
    st.write(f"genrated password : `{password}`")

st.write(    "------------------------------------------")


st.write("Build  with ❤️ by [@Abdul Mateen](https://github.com/abdulmateen5251)")
        




