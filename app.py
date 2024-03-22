import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "model")))
import streamlit as st
from route import home
from route import about
from route import try_it


routes = {
    "Home": home.main,
    "Try it out": try_it.main,
    "About": about.main,
}


st.set_page_config(
    page_title="Brain Tumor Detection",
    page_icon=":brain:",
    layout="wide",
    menu_items={
        "Get Help": "https://github.com/Chaganti-Reddy/Brain-Tumor-Classification",
        "Report a bug": "https://github.com/Chaganti-Reddy/Brain-Tumor-Classification/issues",
        "About": "Brain Tumor Classification using *Deep Convolutional Neural Networks*",
    },
)
st.markdown(
    """
<script type="text/javascript" src="https://code.jquery.com/jquery-3.5.1.min.js" />
<script src="https://raw.githubusercontent.com/darcyclarke/Repo.js/master/repo.min.js" />""",
    unsafe_allow_html=True,
)


pages = list(routes.items())
def format_func(page):
    return page[0]


page = st.sidebar.selectbox(
    "Menu",
    pages,
    index=0,
    format_func=format_func,
)

page[1]()
