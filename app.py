import streamlit as st
import requests
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import time


st.set_page_config(
    page_title="vinylitics", # => Quick reference - Streamlit
    page_icon="🎶",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

# Then continue with your app
st.title(" __vinylitics__ "
         )


def load_css(file_name):
   with open(file_name, "r") as f:
       css = f"<style>{f.read()}</style>"
       st.markdown(css, unsafe_allow_html=True)
load_css("style.css")

#take it off when done with changes
#if st.sidebar.button("🔄 Reload Styles"):
#  load_css("style.css")

st.sidebar.markdown(f'''# welcome to __vinylitics__''')
st.sidebar.markdown(f'''
                    ## the crate-diggers goldmine''')
st.sidebar.markdown(f"""
                    enter a track and artist below to get started

                    """)

plot_cols = ['danceability',
       'energy', 'speechiness', 'acousticness',
       'instrumentalness', 'liveness', 'valence']


st.markdown(
    """<p style='text-align: center;'>
    just enter the name of a track and artist<br>
    vinylitics returns you similar yet less known tracks - maybe a hidden gem?
    </p>""",
    unsafe_allow_html=True
)


track = st.sidebar.text_input("track name", key="track")
artist = st.sidebar.text_input("artist name", key="artist")

url_fuzz = 'https://vinylitics-510572518429.europe-west1.run.app/fuzzy_search'
url_predict_spotify = 'https://vinylitics-510572518429.europe-west1.run.app/predict_spotify'
url_scrap = 'https://vinylitics-510572518429.europe-west1.run.app/song_scrap'

if st.sidebar.button("search"):
    # st.spinner(text=f"Searching for {track} by {artist}...", *, show_time=False)
    # st.write()
    try:
        # Vinyl emoji loading animation
        loader = st.empty()
        with loader:
            st.markdown("""
            <style>
        .spin-vinyl {
            font-size: 3em;
            display: inline-block;
            animation: spin 1.2s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        <div style="text-align:center; padding:1.5em;">
            <div class="spin-vinyl">💿</div>
            <div style="margin-top: 0.5em; font-size: 1.1em;">looking for your track...</div>
        </div>
            """, unsafe_allow_html=True)

        # API request
        st.session_state.results_fuzz = requests.get(
            url_fuzz,
            params={"track_name": track, "artist": artist}
        ).json()

        # Remove the loader
        loader.empty()

    except:

        st.sidebar.write("Looks like your song is not in our database 😕 ")
        st.sidebar.write("🏴‍☠️ Let's scrape Youtube to get this track's audio 🏴‍☠️")
        st.sidebar.write("❗️ _This might take a bit longer_ ❗️ ")


# if st.sidebar.button("Scrap my song"):
#     # st.markdown('''After you clic this button we:
#     #                 * Get the track audio file
#     #                 * Analyse the audio signal
#     #                 * Compute the high level features''')
#         with st.spinner(text="Getting and processing you track...", show_time=True):
#             gif_runner = st.image('https://global.discourse-cdn.com/streamlit/original/2X/2/247a8220ebe0d7e99dbbd31a2c227dde7767fbe1.gif')
#             st.session_state.results_scrap = requests.get(url_scrap, params={'track_name': f"{track} {artist}"}).json()
#             gif_runner.empty()


#         if st.session_state.results_scrap.get("result", None):

#             st.session_state.sel_track_name = track
#             st.session_state.sel_artist_name = artist
#             st.session_state.tempo_og = list(st.session_state.results_scrap['result']['tempo'].values())[0]


#         else:
#             st.write("# Something went wrong, wanna try another track?")
#             st.stop()


        st.sidebar.warning("looks like something went wrong 🫤 try another track or artist!")
        st.stop()


if 'results_fuzz' in st.session_state:
    if st.session_state.results_fuzz['result'] == "Exact match found":
        st.session_state.sel_track_name = track
        st.session_state.sel_artist_name = artist
        st.session_state.tempo_og = st.session_state.results_fuzz['track']['tempo']
        st.sidebar.success(f"found it in our database 🤘")

    else:
        choices = st.session_state.results_fuzz['choices']
        # st.button("Selection")
        song_selection = st.sidebar.radio(f"no exact match found for {track} by {artist}. did you mean:",
                                (choices[0][0], choices[1][0], choices[2][0]))
        st.session_state.sel_track_name = song_selection.split(" by ")[0]
        st.session_state.sel_artist_name = song_selection.split(" by ")[1]


    if 'sel_track_name' in st.session_state:
        st.sidebar.write(f"### let's find similar tracks to {st.session_state.sel_track_name} by {st.session_state.sel_artist_name}:")
        # st.stop()
        if st.sidebar.button("💥 show me the goods 💥"):
            try:
                st.session_state.results_predict = requests.get(url_predict_spotify, params={"track_name": st.session_state.sel_track_name, "artist": st.session_state.sel_artist_name}).json()

                if "error" in st.session_state.results_predict.keys():
                    st.warning('### We are missing values ')
                st.write("### here are some hidden gems we found for you:")

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
                    expander = st.expander ("extra insights")

                    # Metrics - BPM and popularity
                    col1, col2, col3 = expander.columns(3)
                    col2 = col2.metric("bpm", str(np.round(tempo,0)),str(tempo_change)+"%")
                    col3 = col3.metric("popularity", str(st.session_state.results_predict['result']['popularity'][key]))

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
                        name='recommended track'
                    ))

                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color="#31333f",
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 1],
                                gridcolor="black",
                                linecolor="gray",
                                tickfont=dict(color="#31333f")
                            ),
                            angularaxis=dict(
                                tickfont=dict(color="#31333f")
                            )
                        ),
                        legend=dict(
                            font=dict(
                                color="#31333f"
                            )
                        ),
                        showlegend=True
                    )

                    expander.plotly_chart(fig)
            except:
                st.warning('''##### bummer, we are missing features for this track, wanna try another one?''')
                st.stop()
