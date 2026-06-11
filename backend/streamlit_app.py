import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

import json
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from backend.interview import (
    analyze_vacancy,
    generate_questions,
    get_and_evaluate_answer,
    get_adaptive_question,
    generate_final_report
)

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .question-box {
    background-color: #1e3a5f;
    border-left: 4px solid #4a9eff;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    color: #ffffff !important;
}
    .score-box {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        font-size: 2rem;
        font-weight: bold;
    }
    .recommendation-box {
        text-align: center;
        padding: 1.5rem;
        border-radius: 12px;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .hire { background-color: #d4edda; color: #155724; }
    .consider { background-color: #fff3cd; color: #856404; }
    .reject { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
def init_state():
    defaults = {
        "stage": "vacancy",         # vacancy → analysis → interview → report
        "vacancy_text": "",
        "vacancy_analysis": {},
        "questions": [],
        "current_q_index": 0,
        "results": [],
        "final_report": {},
        "max_questions": 5
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/robot.png", width=80)
    st.title("AI Interview Assistant")
    st.divider()

    st.subheader("⚙️ Parametrlər")
    st.session_state.max_questions = st.slider(
        "Sual sayı", min_value=3, max_value=15, value=5
    )

    st.divider()

    # Progress
    stages = {"vacancy": 1, "analysis": 2, "interview": 3, "report": 4}
    current = stages.get(st.session_state.stage, 1)
    st.subheader("📍 İrəliləyiş")
    st.progress(current / 4)
    stage_names = {
        "vacancy": "📄 Vakansiya",
        "analysis": "🔍 Analiz",
        "interview": "🎤 Müsahibə",
        "report": "📊 Hesabat"
    }
    st.write(f"**Mərhələ:** {stage_names.get(st.session_state.stage, '')}")

    st.divider()

    if st.button("🔄 Yenidən Başla", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-header">🤖 AI Interview Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Süni intellekt ilə peşəkar texniki müsahibə</div>', unsafe_allow_html=True)

# ============================================================
# STAGE 1: VACANCY INPUT
# ============================================================
if st.session_state.stage == "vacancy":
    st.subheader("📄 Vakansiya Məlumatı")

    col1, col2 = st.columns([2, 1])

    with col1:
        vacancy_text = st.text_area(
            "Vakansiya mətnini daxil edin:",
            height=300,
            placeholder="""Məsələn:
Software Engineer - Python
We are looking for a Python developer with 3+ years experience.
Required: Python, FastAPI, PostgreSQL, Docker
Nice to have: Redis, AWS, Kubernetes""",
            value=st.session_state.vacancy_text
        )

 

    if st.button("🚀 Müsahibəyə Başla", type="primary", use_container_width=True):
        if not vacancy_text.strip():
            st.error("⚠️ Zəhmət olmasa vakansiya mətnini daxil edin!")
        else:
            st.session_state.vacancy_text = vacancy_text
            with st.spinner("🔍 Vakansiya analiz edilir..."):
                analysis = analyze_vacancy(vacancy_text)
                if analysis:
                    st.session_state.vacancy_analysis = analysis
                    st.session_state.stage = "analysis"
                    st.rerun()
                else:
                    st.error("❌ Vakansiya analizi uğursuz oldu. Yenidən cəhd edin.")

# ============================================================
# STAGE 2: VACANCY ANALYSIS
# ============================================================
elif st.session_state.stage == "analysis":
    analysis = st.session_state.vacancy_analysis

    st.subheader("🔍 Vakansiya Analizi")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💼 Vəzifə", analysis.get("job_title", "N/A"))
    with col2:
        st.metric("📊 Səviyyə", analysis.get("level", "N/A"))
    with col3:
        total_skills = (
            len(analysis.get("core_skills", [])) +
            len(analysis.get("secondary_skills", [])) +
            len(analysis.get("nice_to_have", []))
        )
        st.metric("🛠️ Ümumi Bacarıq", total_skills)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🔴 Əsas Bacarıqlar")
        for skill in analysis.get("core_skills", []):
            importance = skill.get("importance", 0)
            st.write(f"**{skill.get('skill')}**")
            st.progress(importance / 10)
            st.caption(f"Əhəmiyyət: {importance}/10")

    with col2:
        st.subheader("🟡 İkinci Dərəcəli")
        for skill in analysis.get("secondary_skills", []):
            importance = skill.get("importance", 0)
            st.write(f"**{skill.get('skill')}**")
            st.progress(importance / 10)
            st.caption(f"Əhəmiyyət: {importance}/10")

    with col3:
        st.subheader("🟢 Üstünlük")
        for skill in analysis.get("nice_to_have", []):
            importance = skill.get("importance", 0)
            st.write(f"**{skill.get('skill')}**")
            st.progress(importance / 10)
            st.caption(f"Əhəmiyyət: {importance}/10")

    st.divider()

    st.subheader("🎯 Müsahibə Fokusları")
    focuses = analysis.get("interview_focus", [])
    cols = st.columns(min(len(focuses), 3))
    for i, focus in enumerate(focuses):
        with cols[i % 3]:
            st.info(f"📌 {focus}")

    if st.button("🎤 Müsahibəyə Keç", type="primary", use_container_width=True):
        with st.spinner("📋 Suallar hazırlanır..."):
            questions = generate_questions(st.session_state.vacancy_analysis)
            if questions:
                st.session_state.questions = questions[:st.session_state.max_questions]
                st.session_state.stage = "interview"
                st.rerun()
            else:
                st.error("❌ Sual generasiyası uğursuz oldu.")

# ============================================================
# STAGE 3: INTERVIEW
# ============================================================
elif st.session_state.stage == "interview":
    total = len(st.session_state.questions)
    current_idx = st.session_state.current_q_index

    # Progress bar
    st.subheader(f"🎤 Müsahibə — Sual {current_idx + 1}/{total}")
    st.progress((current_idx) / total)

    if current_idx < total:
        question = st.session_state.questions[current_idx]

        # Sual göstər
        difficulty_color = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
        icon = difficulty_color.get(question.get("difficulty", "Medium"), "🟡")

        st.markdown(f"""
        <div class="question-box">
            <b>{icon} {question.get('difficulty')} — {question.get('skill')}</b><br><br>
            {question.get('question')}
        </div>
        """, unsafe_allow_html=True)

        # Cavab — yazılı və ya səsli
        tab1, tab2 = st.tabs(["⌨️ Yazılı Cavab", "🎤 Səsli Cavab"])

        with tab1:
            text_answer = st.text_area(
                "Cavabınızı yazın:",
                height=200,
                key=f"answer_{current_idx}"
            )
            if st.button("✅ Cavabı Göndər", type="primary", key=f"submit_{current_idx}"):
                if not text_answer.strip():
                    st.warning("⚠️ Cavab boş ola bilməz!")
                else:
                    with st.spinner("⚖️ Qiymətləndirilir..."):
                        from backend.prompts import answer_evaluator_prompt
                        from backend.LLM import ask
                        import json

                        prompt = answer_evaluator_prompt(
                            question=question["question"],
                            skill=question["skill"],
                            candidate_answer=text_answer
                        )
                        response = ask(prompt)
                        try:
                            clean = response.replace("```json", "").replace("```", "").strip()
                            evaluation = json.loads(clean)
                        except:
                            evaluation = {"score": 5, "feedback": "Qiymətləndirmə uğursuz oldu"}

                        result = {
                            "question": question,
                            "answer": text_answer,
                            "evaluation": evaluation
                        }
                        st.session_state.results.append(result)

                        score = evaluation.get("score", 0)
                        st.success(f"✅ Bal: {score}/10")
                        st.info(f"💬 {evaluation.get('feedback', '')}")

                        # Adaptiv sual
                        if current_idx + 1 < total:
                            from backend.prompts import adaptive_question_prompt
                            adapt_prompt = adaptive_question_prompt(
                                skill=question["skill"],
                                question=question["question"],
                                score=score
                            )
                            adapt_response = ask(adapt_prompt)
                            try:
                                adapt_clean = adapt_response.replace("```json", "").replace("```", "").strip()
                                adaptive = json.loads(adapt_clean)
                                if adaptive.get("next_question"):
                                    st.session_state.questions[current_idx + 1]["question"] = adaptive["next_question"]
                                    st.session_state.questions[current_idx + 1]["difficulty"] = adaptive.get("next_difficulty", "Medium")
                            except:
                                pass

                        st.session_state.current_q_index += 1

                        if st.session_state.current_q_index >= total:
                            st.session_state.stage = "report"

                        st.rerun()

        with tab2:
            st.info("🎤 Səsli cavab üçün aşağıdakı düyməni basın")
            if st.button("🎙️ Mikrofonu Aç və Cavabla", key=f"voice_{current_idx}"):
                with st.spinner("🎙️ Dinlənilir..."):
                    from backend.STT import listen
                    voice_answer = listen()
                    if voice_answer:
                        st.success(f"📝 Transkript: {voice_answer}")
                        st.session_state[f"voice_text_{current_idx}"] = voice_answer
                    else:
                        st.warning("⚠️ Səs aşkarlanmadı")

            if f"voice_text_{current_idx}" in st.session_state:
                if st.button("✅ Səsli Cavabı Göndər", type="primary", key=f"voice_submit_{current_idx}"):
                    voice_text = st.session_state[f"voice_text_{current_idx}"]
                    with st.spinner("⚖️ Qiymətləndirilir..."):
                        from backend.prompts import answer_evaluator_prompt
                        from backend.LLM import ask
                        import json

                        prompt = answer_evaluator_prompt(
                            question=question["question"],
                            skill=question["skill"],
                            candidate_answer=voice_text
                        )
                        response = ask(prompt)
                        try:
                            clean = response.replace("```json", "").replace("```", "").strip()
                            evaluation = json.loads(clean)
                        except:
                            evaluation = {"score": 5, "feedback": "Qiymətləndirmə uğursuz oldu"}

                        result = {
                            "question": question,
                            "answer": voice_text,
                            "evaluation": evaluation
                        }
                        st.session_state.results.append(result)

                        score = evaluation.get("score", 0)
                        st.success(f"✅ Bal: {score}/10")
                        st.session_state.current_q_index += 1

                        if st.session_state.current_q_index >= total:
                            st.session_state.stage = "report"

                        st.rerun()

    # Əvvəlki cavablar
    if st.session_state.results:
        with st.expander("📋 Əvvəlki Cavablar"):
            for i, r in enumerate(st.session_state.results):
                score = r["evaluation"].get("score", 0)
                color = "🟢" if score >= 7 else "🟡" if score >= 5 else "🔴"
                st.write(f"{color} **Sual {i+1}:** {r['question']['question'][:80]}...")
                st.caption(f"Bal: {score}/10 | {r['evaluation'].get('feedback', '')[:100]}")
                st.divider()

# ============================================================
# STAGE 4: FINAL REPORT
# ============================================================
elif st.session_state.stage == "report":
    if not st.session_state.final_report:
        with st.spinner("📊 Yekun hesabat hazırlanır..."):
            report = generate_final_report(st.session_state.results)
            st.session_state.final_report = report

    report = st.session_state.final_report
    overall_score = report.get("overall_score", 0)
    recommendation = report.get("recommendation", "")

    st.subheader("📊 Yekun Müsahibə Hesabatı")

    # Recommendation box
    rec_class = "hire" if "Hire" in recommendation else "consider" if "Consider" in recommendation else "reject"
    rec_emoji = "✅" if "Hire" in recommendation else "⚠️" if "Consider" in recommendation else "❌"
    st.markdown(f'<div class="recommendation-box {rec_class}">{rec_emoji} {recommendation}</div>', unsafe_allow_html=True)

    st.divider()

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Ümumi Bal", f"{overall_score}/100")
    with col2:
        avg_score = sum(r["evaluation"].get("score", 0) for r in st.session_state.results) / len(st.session_state.results) if st.session_state.results else 0
        st.metric("📊 Ortalama", f"{avg_score:.1f}/10")
    with col3:
        st.metric("❓ Cavablandı", f"{len(st.session_state.results)} sual")

    st.divider()

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Sual üzrə Ballar")
        scores = [r["evaluation"].get("score", 0) for r in st.session_state.results]
        labels = [f"S{i+1}: {r['question']['skill']}" for i, r in enumerate(st.session_state.results)]

        fig = go.Figure(go.Bar(
            x=labels,
            y=scores,
            marker_color=["#2ecc71" if s >= 7 else "#f39c12" if s >= 5 else "#e74c3c" for s in scores],
            text=scores,
            textposition="outside"
        ))
        fig.update_layout(
            yaxis=dict(range=[0, 10]),
            height=350,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🕸️ Bacarıq Radar")
        skills = list(set(r["question"]["skill"] for r in st.session_state.results))
        skill_scores = []
        for skill in skills:
            skill_results = [r["evaluation"].get("score", 0) for r in st.session_state.results if r["question"]["skill"] == skill]
            skill_scores.append(sum(skill_results) / len(skill_results))

        fig2 = go.Figure(go.Scatterpolar(
            r=skill_scores + [skill_scores[0]],
            theta=skills + [skills[0]],
            fill="toself",
            fillcolor="rgba(31, 119, 180, 0.2)",
            line_color="#1f77b4"
        ))
        fig2.update_layout(
            polar=dict(radialaxis=dict(range=[0, 10])),
            height=350,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Strengths & Weaknesses
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💪 Güclü Tərəflər")
        for strength in report.get("technical_strengths", []):
            st.success(f"✅ {strength}")

    with col2:
        st.subheader("📈 İnkişaf Sahələri")
        for weakness in report.get("technical_weaknesses", []):
            st.warning(f"⚠️ {weakness}")

    st.divider()

    # Detailed Q&A
    with st.expander("📋 Detallı Müsahibə Nəticələri"):
        for i, r in enumerate(st.session_state.results):
            score = r["evaluation"].get("score", 0)
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Sual {i+1} ({r['question']['difficulty']}):** {r['question']['question']}")
                st.caption(f"**Cavab:** {r['answer'][:200]}...")
                st.caption(f"**Feedback:** {r['evaluation'].get('feedback', '')}")
            with col2:
                color = "🟢" if score >= 7 else "🟡" if score >= 5 else "🔴"
                st.metric("Bal", f"{color} {score}/10")
            st.divider()

    # JSON export
    if st.button("📥 Hesabatı JSON Yüklə", use_container_width=True):
        full_report = {
            "vacancy": st.session_state.vacancy_text,
            "analysis": st.session_state.vacancy_analysis,
            "final_report": report,
            "detailed_results": st.session_state.results
        }
        st.download_button(
            label="⬇️ JSON Fayl",
            data=json.dumps(full_report, ensure_ascii=False, indent=2),
            file_name="interview_report.json",
            mime="application/json"
        )