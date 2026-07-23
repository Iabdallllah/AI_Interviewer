from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
import os

llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.3)

class InterviewState(TypedDict):
    job_description: str
    candidate_cv: str
    messages: List[Dict[str, str]]

def interviewer_node(state: InterviewState):
    jd = state["job_description"]
    cv = state["candidate_cv"]
    messages = state.get("messages", [])
    
    system_prompt = f"""You are a professional, friendly, and senior HR Interviewer conducting a live voice interview.
    Job Description:
    {jd}
    
    Candidate's CV:
    {cv}
    
    CRITICAL RULES FOR LIVE VOICE CONVERSATION:
    1. **STARTING LANGUAGE:** Analyze the Job Description. Start the interview naturally in the language required by the role (e.g., Arabic, English, French, German). Always match the candidate's language dynamically during the conversation.
    2. **MODERATE RESPONSE LENGTH (CRITICAL):** You are in a real-time voice call. Your responses must be balanced—not too long and boring, but not too short and robotic. 
       - Aim for 2 to 3 natural sentences (around 20 to 40 words).
       - Acknowledge the candidate's previous answer smoothly, then ask ONE clear, relevant question.
    3. **INTERVIEW FLOW:** Ask one question at a time. Keep the tone conversational, professional, and engaging.
    4. **FINAL EVALUATION:** Ask at least 8 questions total before ending. When concluding, provide a concise evaluation of their communication skills and professional suitability with a score out of 10.
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