# backend/interview.py

import json
from LLM import ask
from STT import listen
from TTS import speak
from prompts import (
    vacancy_analyzer_prompt,
    question_generator_prompt,
    answer_evaluator_prompt,
    adaptive_question_prompt,
    final_report_prompt
)


def parse_json(text: str) -> dict:
    """LLM cavabından JSON çıxar"""
    try:
        clean = text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON parse xətası: {e}")
        return {}


# ============================================================
# STEP 1: Vacancy Analyze
# ============================================================
def analyze_vacancy(vacancy_text: str) -> dict:
    print("\n🔍 Vakansiya analiz edilir...")
    prompt = vacancy_analyzer_prompt(vacancy_text)
    response = ask(prompt)
    result = parse_json(response)
    print(f"Vakansiya analizi tamamlandı: {result.get('job_title')} | {result.get('level')}")
    speak(f"Vakansiya analiz edildi. Vəzifə: {result.get('job_title')}, səviyyə: {result.get('level')}.")
    return result


def generate_questions(vacancy_analysis: dict) -> list[dict]:
    print("\n📋 Suallar generasiya edilir...")
    speak("Suallar hazırlanır, bir az gözləyin.")
    prompt = question_generator_prompt(json.dumps(vacancy_analysis, ensure_ascii=False))
    response = ask(prompt)
    result = parse_json(response)
    questions = result.get("questions", [])
    print(f"{len(questions)} sual hazırlandı")
    speak(f"{len(questions)} sual hazırlandı. Müsahibəyə başlayırıq.")
    return questions

# ============================================================
# STEP 3 + 4: Candidate Answer (STT) + Evaluate
# ============================================================
def get_and_evaluate_answer(question: dict) -> dict:
    # Sualı həm ekranda göstər həm səsləndir
    print(f"\n❓ Sual ({question['difficulty']}): {question['question']}")
    speak(question["question"])

    print("\n🎤 Cavabınızı söyləyin...")
    candidate_answer = listen()

    if not candidate_answer:
        print("⚠️ Cavab alınmadı")
        speak("Cavab eşidilmədi, növbəti suala keçirik.")
        return {
            "question": question,
            "answer": "",
            "evaluation": {"score": 0, "feedback": "Cavab verilmədi"}
        }

    print("\n⚖️ Cavab qiymətləndirilir...")
    prompt = answer_evaluator_prompt(
        question=question["question"],
        skill=question["skill"],
        candidate_answer=candidate_answer
    )
    response = ask(prompt)
    evaluation = parse_json(response)

    score = evaluation.get("score", 0)
    feedback = evaluation.get("feedback", "")

    print(f"✅ Qiymət: {score}/10")
    print(f"💬 Feedback: {feedback}")

    # Feedback-i səsləndir
    speak(f"Balınız {score} üzərindən 10-dur. {feedback}")

    return {
        "question": question,
        "answer": candidate_answer,
        "evaluation": evaluation
    }


# ============================================================
# STEP 5: Adaptive Question Generator
# ============================================================
def get_adaptive_question(skill: str, previous_question: str, score: int) -> dict:
    print("\n🔄 Adaptiv sual generasiya edilir...")
    prompt = adaptive_question_prompt(
        skill=skill,
        question=previous_question,
        score=score
    )
    response = ask(prompt)
    result = parse_json(response)
    print(f"✅ Növbəti çətinlik: {result.get('next_difficulty')}")
    return result


# ============================================================
# STEP 6: Final Report
# ============================================================
def generate_final_report(results: list[dict]) -> dict:
    print("\n📊 Yekun hesabat hazırlanır...")

    interview_results = []
    for r in results:
        interview_results.append({
            "skill": r["question"]["skill"],
            "difficulty": r["question"]["difficulty"],
            "question": r["question"]["question"],
            "answer": r["answer"],
            "score": r["evaluation"].get("score", 0),
            "feedback": r["evaluation"].get("feedback", "")
        })

    prompt = final_report_prompt(json.dumps(interview_results, ensure_ascii=False))
    response = ask(prompt)
    report = parse_json(response)
    return report


# ============================================================
# ANA PIPELINE
# ============================================================
def run_interview(vacancy_text: str, max_questions: int = 5):
    print("\n" + "=" * 50)
    print("🤖 AI Müsahibə Assistanı Başladı")
    print("=" * 50)

    # Xoş gəlmisiniz
    speak("Salam! AI Müsahibə Assistantına xoş gəlmisiniz. Müsahibəyə başlayırıq.")

    # 1. Vacancy analiz
    vacancy_analysis = analyze_vacancy(vacancy_text)
    if not vacancy_analysis:
        print("❌ Vakansiya analizi uğursuz oldu")
        return

    # 2. Suallar generasiya
    questions = generate_questions(vacancy_analysis)
    if not questions:
        print("❌ Sual generasiyası uğursuz oldu")
        return

    speak(f"Vakansiya analiz edildi. {max_questions} sual veriləcək. Hər sualdan sonra cavabınızı söyləyin.")

    # 3. Müsahibə
    results = []
    current_questions = questions[:max_questions]

    for i, question in enumerate(current_questions):
        print(f"\n{'=' * 50}")
        print(f"📌 Sual {i + 1}/{len(current_questions)}")
        speak(f"{i + 1}-ci sual.")

        result = get_and_evaluate_answer(question)
        results.append(result)

        score = result["evaluation"].get("score", 0)

        # Son sual deyilsə adaptiv sual generasiya et
        if i < len(current_questions) - 1:
            adaptive = get_adaptive_question(
                skill=question["skill"],
                previous_question=question["question"],
                score=score
            )
            if adaptive.get("next_question"):
                current_questions[i + 1]["question"] = adaptive["next_question"]
                current_questions[i + 1]["difficulty"] = adaptive.get("next_difficulty", current_questions[i + 1]["difficulty"])

    # 4. Yekun hesabat
    speak("Müsahibə tamamlandı. Yekun hesabat hazırlanır.")
    report = generate_final_report(results)

    print("\n" + "=" * 50)
    print("📊 YEKUN HESABAT")
    print("=" * 50)
    print(f"🎯 Ümumi bal:      {report.get('overall_score', 'N/A')}/100")
    print(f"📋 Tövsiyə:        {report.get('recommendation', 'N/A')}")
    print(f"💪 Güclü tərəflər: {', '.join(report.get('technical_strengths', []))}")
    print(f"📈 Zəif tərəflər:  {', '.join(report.get('technical_weaknesses', []))}")
    print("=" * 50)

    speak(f"Yekun balınız {report.get('overall_score', 0)} üzərindən 100-dür. Tövsiyə: {report.get('recommendation', '')}.")

    return report