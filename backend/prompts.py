# backend/prompts.py


# ============================================================
# 1. VACANCY ANALYZER
# ============================================================
def vacancy_analyzer_prompt(vacancy_text: str) -> str:
    prompt = f"""You are a Senior Technical Recruiter and Staff Software Engineer with more than 15 years of hiring experience.
Your task is to analyze the provided job description and extract all information required for a professional technical interview.
Instructions:
1. Identify:
   - Job title
   - Seniority level
   - Required skills
   - Preferred skills
   - Technologies
   - Tools
   - Soft skills
2. Categorize skills into:
   - Core Skills
   - Secondary Skills
   - Nice-to-Have Skills
3. Estimate importance of each skill on a scale from 1 to 10.
4. Determine expected candidate level:
   - Junior
   - Mid
   - Senior
   - Lead
5. Create an interview blueprint.
Return JSON only.
Output Format:
{{
  "job_title": "",
  "level": "",
  "core_skills": [
    {{
      "skill": "",
      "importance": 10
    }}
  ],
  "secondary_skills": [],
  "nice_to_have": [],
  "interview_focus": [
    ""
  ]
}}
Job Description:
{vacancy_text}"""
    return prompt


# ============================================================
# 2. QUESTION GENERATOR
# ============================================================
def question_generator_prompt(vacancy_analysis: str) -> str:
    prompt = f"""You are a Senior Technical Interviewer.
Generate a professional interview based on the provided skills.
Requirements:
- Create 15 interview questions.
- Questions must be directly related to the job requirements.
- Include Easy, Medium, and Hard questions.
- Include both theoretical and practical questions.
- Include scenario-based questions whenever possible.
- Avoid generic questions.
- Questions should evaluate real-world experience.
- All questions must be written in Azerbaijani language.
Difficulty Distribution:
- Easy: 30%
- Medium: 50%
- Hard: 20%
Return JSON only.
Output Format:
{{
  "questions": [
    {{
      "id": 1,
      "skill": "Python",
      "difficulty": "Easy",
      "question": ""
    }}
  ]
}}
Skills:
{vacancy_analysis}"""
    return prompt

# ============================================================
# 3. ANSWER EVALUATOR
# ============================================================
def answer_evaluator_prompt(question: str, skill: str, candidate_answer: str) -> str:
    prompt = f"""You are a Senior Technical Interview Evaluator.
Evaluate the candidate's answer objectively.
Rules:
- Score from 0 to 10.
- Consider:
  - Technical correctness
  - Completeness
  - Depth of knowledge
  - Practical experience
  - Communication quality
Scoring Guide:
0-2:
Incorrect answer.
3-4:
Very weak understanding.
5-6:
Basic understanding.
7-8:
Good understanding.
9-10:
Excellent understanding with practical knowledge.
Return JSON only.
Question:
{question}
Expected Skill:
{skill}
Candidate Answer:
{candidate_answer}
Output Format:
{{
  "score": 8,
  "technical_accuracy": 8,
  "depth": 7,
  "communication": 9,
  "strengths": [
    ""
  ],
  "weaknesses": [
    ""
  ],
  "feedback": ""
}}"""
    return prompt

# ============================================================
# 4. ADAPTIVE QUESTION GENERATOR
# ============================================================
def adaptive_question_prompt(skill: str, question: str, score: int) -> str:
    prompt = f"""You are an intelligent technical interviewer.
Current Skill:
{skill}
Previous Question:
{question}
Candidate Score:
{score}
Rules:
If score >= 8:
Generate a more advanced follow-up question.
If score between 5 and 7:
Generate a question at the same difficulty level.
If score < 5:
Generate a simpler question to verify basic understanding.
Return JSON only.
{{
  "next_difficulty": "",
  "next_question": ""
}}"""
    return prompt


# ============================================================
# 5. FINAL REPORT GENERATOR
# ============================================================
def final_report_prompt(interview_results: str) -> str:
    prompt = f"""You are a Hiring Manager.
Analyze all interview results.
Provide:
1. Overall score (0-100)
2. Technical strengths
3. Technical weaknesses
4. Hiring recommendation
Recommendations:
90-100:
Strong Hire
75-89:
Hire
60-74:
Consider
40-59:
Weak Consider
0-39:
Reject
Return JSON only.
Interview Results:
{interview_results}"""
    return prompt