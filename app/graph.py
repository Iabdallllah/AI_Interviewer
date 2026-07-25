from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
import os

llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.3)

class InterviewState(TypedDict):
    job_description: str
    candidate_cv: str
    messages: List[Dict[str, str]]
    persona: str
    difficulty: str
    length: str

def interviewer_node(state: InterviewState):
    jd = state["job_description"]
    cv = state["candidate_cv"]
    messages = state.get("messages", [])
    persona = state.get("persona", "general_hr")
    difficulty = state.get("difficulty", "medium")
    length = state.get("length", "medium")
    
    if length == "short":
        target_questions = 4
    elif length == "long":
        target_questions = 10
    else:
        target_questions = 7
        
    ai_msg_count = sum(1 for m in messages if m.get("role") == "ai")
    
    if persona == "technical_concepts":
        persona_behavior = "You are a Senior Technical Interviewer. Focus on software engineering concepts, system design, and problem-solving logic. No exact code dictation."
    elif persona == "linguistic_assessment":
        persona_behavior = "You are a strict Language Evaluator. Conduct the interview strictly in the language implied by the JD. Assess fluency, grammar, and vocabulary."
    elif persona == "stress_test":
        persona_behavior = "You are a Stress Interviewer. Test how the candidate handles pressure, ambiguity, and strict deadlines."
    elif persona == "executive_stakeholder":
        persona_behavior = "You are a Non-Technical Executive. Focus on ROI, business impact, and high-level strategy."
    else:
        persona_behavior = "You are a Professional HR Interviewer. Focus on behavioral questions, cultural fit, and soft skills."

    difficulty_prompt = f"The difficulty level is {difficulty.upper()}. Adjust the complexity and depth of your questions accordingly."

    # فصل منطق أول سؤال عن باقي المقابلة
    if ai_msg_count == 0:
        flow_rule = "This is the VERY FIRST message of the interview. Welcome the candidate naturally, briefly introduce the interview, and ask the FIRST question. DO NOT acknowledge any previous input because the candidate hasn't spoken yet. Keep your message natural and moderate in length (around 20-35 words)."
    elif ai_msg_count >= target_questions:
        flow_rule = "THIS IS THE FINAL MESSAGE. Do NOT ask any more questions. Give a brief VERBAL EVALUATION (max 3 sentences) summarizing their performance, giving a score out of 10, and thanking them. YOU MUST APPEND THE EXACT TEXT `[INTERVIEW_CONCLUDED]` at the very end of your response."
    else:
        flow_rule = f"This is question {ai_msg_count + 1} out of {target_questions}. Acknowledge the candidate's previous answer naturally in one short sentence. Then, ask EXACTLY ONE clear, relevant question. Keep your total response natural, conversational, and moderate in length (around 20 to 40 words). Do NOT be overly brief, but avoid long monologues."

    system_prompt = f"""{persona_behavior}
    
    {difficulty_prompt}
    
    Job Description:
    {jd}
    
    Candidate's CV:
    {cv}
    
    CRITICAL RULES:
    1. **STRICT LANGUAGE MATCHING:** You MUST speak in the EXACT SAME language as the Job Description.
    2. **NATURAL & CONVERSATIONAL:** Speak naturally like a real human interviewer.
    3. **NO IN-VOICE EVALUATION YET:** Never give the candidate a score or evaluate them verbally until the very end of the interview.
    4. {flow_rule}
    """
    
    formatted_messages = [("system", system_prompt)]
    for msg in messages:
        role = "assistant" if msg.get("role") == "ai" else "user"
        formatted_messages.append((role, msg.get("content", "")))
    
    response = llm.invoke(formatted_messages)
    new_messages = messages + [{"role": "ai", "content": response.content}]
    return {"messages": new_messages}

workflow = StateGraph(InterviewState)
workflow.add_node("interviewer", interviewer_node)
workflow.set_entry_point("interviewer")
workflow.add_edge("interviewer", END)

interview_app = workflow.compile()
