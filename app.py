import streamlit as st

st.set_page_config(
    page_title="Vinylitics", # => Quick reference - Streamlit
    page_icon="🎶",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

'''
# Vinylitics
'''

""" Welcome to vinylitics, the crate-diggers goldmine!"""
"""Just enter the name of a track and artist, and Vynilitics returns you similar yet less known tracks - maybe a hidden gem? """

"""## Enter a track and artist below to get started!"""

columns = st.columns(2)
track = columns[0].text_input("Track name")
artist = columns[1].text_input("Artist name")


