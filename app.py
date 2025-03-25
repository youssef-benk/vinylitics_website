import streamlit as st
import requests
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Vinylitics", # => Quick reference - Streamlit
    page_icon="🎶",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

st.sidebar.markdown(f'''# Welcome to __Vinylitics__''')
st.sidebar.markdown(f'''
                    ## The crate-diggers goldmine''')
st.sidebar.markdown(f"""
                    Enter a track and artist below to get started

                    """)

plot_cols = ['danceability',
       'energy', 'speechiness', 'acousticness',
       'instrumentalness', 'liveness', 'valence']

'''
# Vinylitics
'''

"""Just enter the name of a track and artist, and Vynilitics returns you similar yet less known tracks - maybe a hidden gem? """



track = st.sidebar.text_input("Track name", key="track")
artist = st.sidebar.text_input("Artist name", key="artist")

url_fuzz = 'https://vinylitics-510572518429.europe-west1.run.app/fuzzy_search'
url_predict_spotify = 'https://vinylitics-510572518429.europe-west1.run.app/predict_spotify'

if st.sidebar.button("Search"):
    # st.spinner(text=f"Searching for {track} by {artist}...", *, show_time=False)
    # st.write()
    try:
        with st.spinner(text="Looking for your track...", show_time=False):
            st.session_state.results_fuzz = requests.get(url_fuzz, params={"track_name": track, "artist": artist}).json()

    except:
        st.sidebar.warning("Looks like something went wrong 🫤 Try another track or artist!")
        st.stop()


if 'results_fuzz' in st.session_state:
    if st.session_state.results_fuzz['result'] == "Exact match found":
        st.session_state.sel_track_name = track
        st.session_state.sel_artist_name = artist
        st.session_state.tempo_og = st.session_state.results_fuzz['track']['tempo']
        st.sidebar.success(f"Found it in our database 🤘")

    else:
        choices = st.session_state.results_fuzz['choices']
        # st.button("Selection")
        song_selection = st.sidebar.radio(f"No exact match found for {track} by {artist}. Did you mean:",
                                (choices[0][0], choices[1][0], choices[2][0]))
        st.session_state.sel_track_name = song_selection.split(" by ")[0]
        st.session_state.sel_artist_name = song_selection.split(" by ")[1]


    if 'sel_track_name' in st.session_state:
        st.sidebar.write(f"### Let's find similar tracks to {st.session_state.sel_track_name} by {st.session_state.sel_artist_name}:")
        # st.stop()
        if st.sidebar.button("💥 Show me the goods 💥"):
            try:
                st.session_state.results_predict = requests.get(url_predict_spotify, params={"track_name": st.session_state.sel_track_name, "artist": st.session_state.sel_artist_name}).json()

                st.write("### Here are some hidden gems we found for you:")
                keys = st.session_state.results_predict['result']['track_name'].keys()

                tempo_og = list(st.session_state.results_predict['sel_track']['tempo'].values())[0]

                for i, key in enumerate(keys):
                    st.write(f"#### {i+1}. {st.session_state.results_predict['result']['track_name'][key].title()} by {st.session_state.results_predict['result']['artists'][key].title()}")
                    track_id = st.session_state.results_predict['result']['track_id'][key]
                    track_url = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator"
                    tempo = st.session_state.results_predict['result']['tempo'][key]
                    tempo_change = np.round((tempo - tempo_og)/ tempo_og * 100, 0 )
                    # Spotify embedded player:
                    components.iframe(track_url, width=800, height=400)
                    # Drop-down insights
                    expander = st.expander ("Extra insights")

                    # Metrics - BPM and popularity
                    col1, col2, col3 = expander.columns(3)
                    col2 = col2.metric("BPM", str(np.round(tempo,0)),str(tempo_change)+"%")
                    col3 = col3.metric("Popularity", str(st.session_state.results_predict['result']['popularity'][key]))

                    # Radar plot
                    r_key = []
                    r_key = [st.session_state.results_predict['result'][col][key] for col in plot_cols]

                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=r_key,
                        theta=plot_cols,
                        fill='toself',
                        fillcolor='orange',
                        line_color ='orange',
                        opacity=.5,
                        name='Recommended track'
                    ))

                    fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                        )),
                    showlegend=True
                    )

                    expander.plotly_chart(fig)
            except:
                st.warning('''#### Bummer, looks like we are missing features for this track. Wanna try another one?''')
                st.stop()
