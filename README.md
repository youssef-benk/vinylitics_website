![](./banner.png)

# vinylitics 🎵 frontend

> the face of a gold mine for crate diggers.

this is the streamlit-powered frontend for **vinylitics**, a music discovery app that recommends ten hidden gems based on a song you already love. no more algorithmic echo chambers, just music worth finding.

→ **[try it live 🎸](https://vinylitics.streamlit.app/)**

---

## what you'll find here

this repo contains the streamlit web app that connects to the [vinylitics backend api](https://github.com/youssef-benk/vinylitics), handles user input, and displays the recommendations.

each of the ten recommended songs is presented with an **embedded spotify player** so you can listen right away: no extra clicks, no leaving the page, just bangers.

---

## how the app flows

**1.** you type in a song title and artist name

**2.** the app sends your input to the backend api, which searches a database of 1 million songs using audio features and machine learning

**3.** you get back ten tracks similar in sound to your input, but deliberately chosen from the least-streamed songs in the database

**4.** each result comes with an embedded spotify player, ready to play 🎸

---

## tech stack

| layer | technology |
|---|---|
| frontend | streamlit |
| styling | css |
| language | python |

---

## the team
⚡️ [dj flore](https://github.com/flore-perr)

🎸 [dj adviti](https://github.com/advitis)

💥 [mc stephanie](https://github.com/3Digitals-Agentur)

🎸 [mc youssef](https://github.com/youssef-benk)

⚡️ [dj suzie](https://github.com/SuzieBeasse)

→ backend repo: [vinylitics](https://github.com/youssef-benk/vinylitics)

→ 🎵 live app 🎵: [vinylitics.streamlit.app](https://vinylitics.streamlit.app/)
