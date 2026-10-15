import streamlit as st
from questons import questions, choix, reponses

st.set_page_config(
    page_title="Quiz entre amis",
    page_icon="🎯",
    layout="centered"
)

if "prenom" not in st.session_state:
    st.session_state.prenom = ""

if "quiz_commence" not in st.session_state:
    st.session_state.quiz_commence = False

if "quiz_termine" not in st.session_state:
    st.session_state.quiz_termine = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "total_questions" not in st.session_state:
    st.session_state.total_questions = len(questions)

if "mauvaises_reponses" not in st.session_state:
    st.session_state.mauvaises_reponses = []

st.title("🎯 Quiz entre amis")
st.write("Bienvenue dans le quiz ! Teste tes connaissances et découvre ton score.")
st.divider()

if not st.session_state.quiz_commence:

    st.subheader("👋 Bienvenue !")

    with st.form("form_prenom"):
        prenom = st.text_input(
            "Entre ton prénom pour commencer :",
            value=st.session_state.prenom
        )
        commencer = st.form_submit_button("🚀 Commencer le quiz")

    if commencer:
        if prenom.strip():
            st.session_state.prenom = prenom.strip()
            st.session_state.quiz_commence = True
            st.session_state.quiz_termine = False
            st.session_state.score = 0
            st.session_state.mauvaises_reponses = []
            st.rerun()
        else:
            st.warning("⚠️ Entre ton prénom avant de commencer.")

elif not st.session_state.quiz_termine:

    st.subheader(f"Bonne chance, {st.session_state.prenom} ! 🍀")
    st.write(
        f"Tu as {len(questions)} questions. "
        "Réponds à chacune d'elles avant de terminer."
    )

    with st.form("form_quiz"):

        reponses_utilisateur = []

        for i, question in enumerate(questions):
            st.markdown(f"### Question {i + 1}")
            st.write(question)

            reponse = st.radio(
                "Sélectionne une réponse :",
                choix[i],
                key=f"question_{i}",
                index=None
            )

            reponses_utilisateur.append(reponse)
            st.divider()

        terminer = st.form_submit_button("🏁 Terminer le quiz")

    if terminer:

        if any(rep is None for rep in reponses_utilisateur):
            st.warning(
                "⚠️ Tu dois répondre à toutes les questions "
                "avant de terminer le quiz."
            )
        else:
            score = 0
            mauvaises_reponses = []

            for i, reponse_utilisateur in enumerate(reponses_utilisateur):
                if (
                    reponse_utilisateur.strip().casefold()
                    == reponses[i].strip().casefold()
                ):
                    score += 1
                else:
                    mauvaises_reponses.append({
                        "question": questions[i],
                        "reponse_choisie": reponse_utilisateur
                    })

            st.session_state.score = score
            st.session_state.total_questions = len(questions)
            st.session_state.mauvaises_reponses = mauvaises_reponses
            st.session_state.quiz_termine = True
            st.rerun()

if st.session_state.quiz_termine:

    score = st.session_state.score
    total = st.session_state.total_questions
    pourcentage = score / total * 100 if total > 0 else 0

    st.balloons()
    st.success("🎉 Quiz terminé !")
    st.subheader(f"Bravo, {st.session_state.prenom} !")

    st.metric(
        label="🏆 Ton score final",
        value=f"{score} / {total}"
    )

    st.write(f"Tu as obtenu **{pourcentage:.1f} %** de bonnes réponses.")
    st.progress(int(pourcentage))

    if pourcentage == 100:
        st.success("🌟 Excellent ! Tu as répondu correctement à toutes les questions !")
    elif pourcentage >= 75:
        st.success("👏 Très bon résultat ! Tu maîtrises bien le sujet.")
    elif pourcentage >= 50:
        st.info("👍 Pas mal ! Tu peux encore améliorer ton score.")
    else:
        st.warning("💪 Continue à t'entraîner ! Tu feras mieux la prochaine fois.")

    st.divider()
    st.subheader("❌ Tes mauvaises réponses")

    mauvaises_reponses = st.session_state.mauvaises_reponses

    if mauvaises_reponses:
        st.write(
            "Voici les questions auxquelles tu as mal répondu "
            "et les réponses que tu as choisies."
        )

        for i, erreur in enumerate(mauvaises_reponses, start=1):
            st.markdown(f"**❌ Question : {erreur['question']}**")
            st.write(f"Ta réponse : {erreur['reponse_choisie']}")
            st.divider()
    else:
        st.success("🎉 Félicitations ! Tu as répondu correctement à toutes les questions.")

    st.info(
        "📸 Fais une capture d'écran de ton résultat "
        "et envoie-la à l'organisateur du quiz."
    )

    if st.button("🔄 Recommencer le quiz"):

        for i in range(len(questions)):
            cle = f"question_{i}"
            if cle in st.session_state:
                del st.session_state[cle]

        st.session_state.prenom = ""
        st.session_state.quiz_commence = False
        st.session_state.quiz_termine = False
        st.session_state.score = 0
        st.session_state.total_questions = len(questions)
        st.session_state.mauvaises_reponses = []

        st.rerun()
    
