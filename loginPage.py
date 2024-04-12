import streamlit as st
from streamlit.components.v1 import html

def main():
    st.title("StarShadow Chat Bot - Login")
    st.markdown("---")  # Add a horizontal line for separation

    # Centering the login form
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.write("")  # Empty space for vertical centering
        st.write("")  # Empty space for vertical centering
        st.write("")  # Empty space for vertical centering

        # CSS to center align the form
        st.markdown(
            """
            <style>
            .login-form {
                margin: auto;
                max-width: 400px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        with st.container():
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if username == "admin" and password == "password":
                    st.success("Logged in successfully!")
                    # Redirect to app.py after successful login
                    st.markdown(
                        html('<a href="/app.py" id="redirect-link" style="display: none;"></a>'),
                        unsafe_allow_html=True
                    )
                    st.write('<script>document.getElementById("redirect-link").click()</script>', unsafe_allow_html=True)
                else:
                    st.error("Invalid username or password")

if __name__ == "__main__":
    main()
