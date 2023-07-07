import base64

def set_font_css(css, font_size):
    css.markdown(
        """
        <style>
        .st-af {
            font-size: {font_size}px;
            font-weight: "bold";
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def set_padding_css(css_code):
    css_code.markdown(
            """
            <style>
            .reportview-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

def page_details(css_code):
    css_code.markdown(
            """
        <style>
            .stApp {{
            padding-top: -20rem;
            # margin-top: -20px;
            }}
        </style>
            """,
            unsafe_allow_html=True
        )

def grow_element(css):
        css.markdown(
        f"""
            <style>
        .grow {{
    transition: all .2s ease-in-out; 
    }}

        .grow:hover {{
        height: 200px; 
        }}
            </style>
            """,
            unsafe_allow_html=True
        )

def title_alignment(st):
    with open("ball.png", "rb") as f:
        image_left = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <h1 style="display: flex; text-align: center; align-items: center; justify-content: center;">
            <img src="data:image/jpg;base64,{image_left}" style="width: 50px; height: 50px; margin-right: 10px;" />
            SportSense Football Dashboard
            <img src="data:image/jpg;base64,{image_left}" style="width: 50px; height: 50px; margin-left: 10px;" />
        </h1>
        """,
        unsafe_allow_html=True
    )
