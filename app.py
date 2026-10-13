import streamlit as st
from questons import questions, choix, reponses

st.set_page_config(page_title="Mon quiz entre amis", page_icon="🎯")

if "prenom" not in st.session_state:
    st.session_state.prenom = ""

if not st.session_state.prenom:
    st.title("🎯 Quiz entre amis")
    st.write("Bienvenue ! Entre ton prénom pour commencer.")

    prenom = st.text_input("Ton prénom")

    if st.button("Commencer le quiz"):
        if prenom.strip():
            st.session_state.prenom = prenom.strip()
            st.rerun()
        else:
            st.warning("Entre ton prénom avant de continuer.")

else:
    st.title(f"🎯 Bienvenue, {st.session_state.prenom} !")
    st.write("Réponds aux questions et découvre ton score !")

    with st.form("quiz"):
        user_answers = []

        for i, question in enumerate(questions):
            st.subheader(f"Question {i + 1}")
            st.write(question)

            answer = st.radio(
                "Choisis ta réponse :",
                choix[i],
                key=f"question_{i}",
                index=None
            )
            user_answers.append(answer)

        submitted = st.form_submit_button("Valider mes réponses")

    if submitted:
        if any(answer is None for answer in user_answers):
            st.warning("Réponds à toutes les questions avant de valider.")
        else:
            score = sum(
                answer.strip().casefold() == correct.strip().casefold()
                for answer, correct in zip(user_answers, reponses)
            )

            st.success(
                f"{st.session_state.prenom}, ton score est : "
                f"{score}/{len(questions)}"
            )
            st.write("Merci d'avoir joué ! 🎉")
