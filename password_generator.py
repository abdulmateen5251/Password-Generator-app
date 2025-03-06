import streamlit as st
import random 
import string
import pyperclip
import json
import os
from datetime import datetime

def generate_password(length, use_digits, use_special_chars):
    characters = string.ascii_letters

    if use_digits:
        characters += string.digits  # add digits to the characters (0-9) if selected

    if use_special_chars:
        characters += string.punctuation  # add special characters to the characters (e.g., !, @, #, $, %, ^, &, *)

    return ''.join(random.choice(characters) for _ in range(length))  # join the characters to form a password

def suggest_strong_password():
    # Generate a strong password with at least 16 characters, including digits and special characters
    length = random.randint(16, 20)
    
    # Ensure we have at least one of each type of character
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    
    # Fill the rest with random characters
    remaining_length = length - len(password)
    all_chars = string.ascii_letters + string.digits + string.punctuation
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle the password characters
    random.shuffle(password)
    
    return ''.join(password)

def calculate_password_strength(password):
    # Simplified password strength calculator
    score = 0
    feedback = []
    
    # Length check
    if len(password) < 8:
        score += 1
        feedback.append("Password is too short.")
    elif len(password) < 12:
        score += 2
        feedback.append("Password length is moderate.")
    else:
        score += 3
        feedback.append("Good password length.")
    
    # Character diversity checks
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")
        
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")
        
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers.")
        
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Add special characters.")
    
    # Common password check (simplified)
    common_passwords = ["password", "123456", "qwerty", "admin"]
    if any(common in password.lower() for common in common_passwords):
        score = 1
        feedback.append("Contains common password patterns.")
    
    # Calculate strength category
    if score <= 2:
        strength = "Weak"
        color = "red"
    elif score <= 4:
        strength = "Moderate"
        color = "orange"
    elif score <= 6:
        strength = "Strong"
        color = "green"
    else:
        strength = "Very Strong"
        color = "blue"
    
    return strength, color, feedback

def save_password(password, label):
    # Create a data structure to save
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    password_data = {
        "password": password,
        "label": label,
        "created_at": timestamp
    }
    
    # Load existing passwords
    saved_passwords = []
    if os.path.exists("saved_passwords.json"):
        try:
            with open("saved_passwords.json", "r") as file:
                saved_passwords = json.load(file)
        except:
            saved_passwords = []
    
    # Add the new password
    saved_passwords.append(password_data)
    
    # Save the updated list
    with open("saved_passwords.json", "w") as file:
        json.dump(saved_passwords, file, indent=4)
    
    return saved_passwords

# Set page title and icon
st.set_page_config(page_title="Password Generator", page_icon="🔐")

# Custom CSS for icons and styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    .section-header {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }
    .icon-text {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .password-label {
        font-weight: 500;
        color: #0066cc;
    }
    .sidebar-header {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for password and saved passwords
if 'password' not in st.session_state:
    st.session_state.password = ""
if 'saved_passwords' not in st.session_state:
    if os.path.exists("saved_passwords.json"):
        try:
            with open("saved_passwords.json", "r") as file:
                st.session_state.saved_passwords = json.load(file)
        except:
            st.session_state.saved_passwords = []
    else:
        st.session_state.saved_passwords = []

# Create sidebar for saved passwords
with st.sidebar:
    st.markdown('<p class="sidebar-header">📋 Saved Passwords</p>', unsafe_allow_html=True)
    
    if st.session_state.password:
        # Form for saving a password
        st.markdown('<p class="section-header">💾 Save Current Password</p>', unsafe_allow_html=True)
        with st.form("save_password_form"):
            label = st.text_input("🏷️ Label for this password (e.g., 'Gmail Account')")
            submit = st.form_submit_button("💾 Save Password")
            
            if submit and label:
                st.session_state.saved_passwords = save_password(st.session_state.password, label)
                st.success(f"✅ Password saved with label: {label}")
    
    # Display saved passwords
    if st.session_state.saved_passwords:
        st.markdown('<p class="section-header">🔑 Your Passwords</p>', unsafe_allow_html=True)
        for idx, pwd in enumerate(st.session_state.saved_passwords):
            with st.expander(f"🔐 {pwd['label']} ({pwd['created_at']})"):
                st.text_input(f"🔒 Password", value=pwd['password'], type="password", key=f"saved_pwd_{idx}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy", key=f"copy_btn_{idx}", use_container_width=True):
                        pyperclip.copy(pwd['password'])
                        st.success("✅ Copied!")
                with col2:
                    if st.button("👁️ Show/Hide", key=f"show_btn_{idx}", use_container_width=True):
                        if f"show_pwd_{idx}" not in st.session_state:
                            st.session_state[f"show_pwd_{idx}"] = True
                        else:
                            st.session_state[f"show_pwd_{idx}"] = not st.session_state[f"show_pwd_{idx}"]
                
                if f"show_pwd_{idx}" in st.session_state and st.session_state[f"show_pwd_{idx}"]:
                    st.code(pwd['password'])
    else:
        st.info("📭 No saved passwords yet.")
        
    st.markdown("---")
    st.markdown("🔧 Built with ❤️ by [@Abdul Mateen](https://github.com/abdulmateen5251)")
    
    # Settings section in sidebar
    st.markdown('<p class="section-header">⚙️ Settings</p>', unsafe_allow_html=True)
    st.checkbox("🌙 Dark Mode", key="dark_mode", value=True)
    if st.button("🗑️ Clear All Saved Passwords"):
        if os.path.exists("saved_passwords.json"):
            os.remove("saved_passwords.json")
            st.session_state.saved_passwords = []
            st.success("✅ All passwords cleared!")
            st.rerun()

# Main content
st.markdown('<p class="main-header">🔐 Password Generator</p>', unsafe_allow_html=True)

# Create two columns for the main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="section-header">🛠️ Password Options</p>', unsafe_allow_html=True)
    length = st.slider("🔢 Password Length", min_value=8, max_value=32, value=16)
    use_digits = st.checkbox("🔢 Include digits (0-9)", value=True)
    use_special_chars = st.checkbox("✳️ Include special characters (!@#$%)", value=True)
    
    # Create a row of buttons
    col_gen, col_suggest = st.columns(2)
    
    with col_gen:
        generate_button = st.button("🔄 Generate Password", use_container_width=True)
    
    with col_suggest:
        suggest_button = st.button("⭐ Suggest Strong Password", use_container_width=True)

with col2:
    st.markdown('<p class="section-header">📊 Strength Guide</p>', unsafe_allow_html=True)
    st.markdown("🔴 **Weak**: Less than 8 chars, limited variety")
    st.markdown("🟠 **Moderate**: 8-12 chars, some variety")
    st.markdown("🟢 **Strong**: 12+ chars, good mix")
    st.markdown("🔵 **Very Strong**: 16+ chars, excellent mix")

# Generate the password
if generate_button:
    st.session_state.password = generate_password(length, use_digits, use_special_chars)
elif suggest_button:
    st.session_state.password = suggest_strong_password()

# Display the generated password and related actions
if st.session_state.password:
    st.markdown('<p class="section-header">🔑 Generated Password</p>', unsafe_allow_html=True)
    
    # Calculate and display password strength
    strength, color, feedback = calculate_password_strength(st.session_state.password)
    
    # Determine the strength icon
    strength_icon = "🔴" if color == "red" else "🟠" if color == "orange" else "🟢" if color == "green" else "🔵"
    
    st.markdown(f"📊 Password Strength: <span style='color:{color};font-weight:bold'>{strength_icon} {strength}</span>", unsafe_allow_html=True)
    
    # Show password in a text box
    password_box = st.text_input("🔒 Your password:", value=st.session_state.password, type="password")
    
    # Show/hide password toggle
    show_password = st.checkbox("👁️ Show password")
    if show_password:
        st.code(st.session_state.password)
    
    # Action buttons
    col_copy, col_another = st.columns(2)
    
    with col_copy:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            pyperclip.copy(st.session_state.password)
            st.success("✅ Password copied to clipboard!")
    
    with col_another:
        if st.button("🔄 Generate Another", use_container_width=True):
            if use_digits and use_special_chars:
                st.session_state.password = generate_password(length, use_digits, use_special_chars)
                st.rerun()
            else:
                st.session_state.password = suggest_strong_password()
                st.rerun()
        
    # Encourage saving
    st.info("👈 Use the sidebar to save this password")

    # Display feedback on password strength
    if feedback:
        st.markdown('<p class="section-header">✅ Improvement Suggestions</p>', unsafe_allow_html=True)
        for tip in feedback:
            st.markdown(f"📝 {tip}")

# Display application footer
st.markdown("---")
st.markdown('<div style="text-align: center;">🔒 <b>Secure Password Generator</b> | Version 2.0 | 🛡️ Your Security Matters</div>', unsafe_allow_html=True)