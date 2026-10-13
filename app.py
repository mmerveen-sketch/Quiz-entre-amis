import streamlit as st
from questons import questions, choix, reponses

st.set_page_config(page_title="Mon quiz entre amis", page_icon="🎯")

st.title("🎯 Quiz entre amis")
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

        st.success(f"Ton score final est : {score}/{len(questions)}")
        st.write("Merci d'avoir joué ! 🎉")