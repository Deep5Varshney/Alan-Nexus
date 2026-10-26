import os
from typing import Dict, Any, TypedDict
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

class AgentState(TypedDict):
    input_text: str
    context: Dict[str, Any]
    intent: str
    action_type: str
    execution_result: Any
    final_response: str
    json_payload: Dict[str, Any]

llm = ChatGroq(
    temperature=0.2,
    model_name="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)

def intent_classifier_node(state: AgentState) -> Dict[str, Any]:
    user_input = state["input_text"]
    
    prompt = f"""
    You are the Intent Routing Agent for Alan-Nexus. Analyze the user command:
    "{user_input}"
    
    Classify into EXACTLY one category:
    - CODE_EXPLAIN: Questions about code, errors, architectural concepts, or developer help.
    - DYNAMIC_ACTION: Requests to navigate, trigger client actions, open settings, or change state.
    - GENERAL_QA: General knowledge, chat, or open-ended reasoning.
    
    Respond in EXACTLY one line with only the category name.
    """
    response = llm.invoke([HumanMessage(content=prompt)]).content.strip()
    return {"intent": response}

def task_executor_node(state: AgentState) -> Dict[str, Any]:
    intent = state.get("intent", "GENERAL_QA")
    user_input = state["input_text"]
    context = state.get("context", {})
    
    if "CODE_EXPLAIN" in intent:
        sys_prompt = "You are a senior software engineer. Provide a concise 2-sentence explanation of the technical concept requested."
        res = llm.invoke([SystemMessage(content=sys_prompt), HumanMessage(content=user_input)])
        return {
            "execution_result": res.content,
            "action_type": "DISPLAY_CODE_DOCS",
            "json_payload": {
                "action": "RENDER_CARD",
                "type": "CODE_EXPLANATION",
                "content": res.content,
                "timestamp": context.get("timestamp")
            }
        }
        
    elif "DYNAMIC_ACTION" in intent:
        sys_prompt = f"""
        Extract intended action and parameters from: '{user_input}'.
        Return JSON format with 'target_view' and 'command_name'.
        """
        res = llm.invoke([SystemMessage(content=sys_prompt), HumanMessage(content=user_input)])
        return {
            "execution_result": "UI Action command parsed successfully.",
            "action_type": "TRIGGER_CLIENT_EVENT",
            "json_payload": {
                "action": "NAVIGATE_UI",
                "command": "EXECUTE_CLIENT_ACTION",
                "parsed_details": res.content
            }
        }
        
    else:  # GENERAL_QA
        res = llm.invoke([HumanMessage(content=user_input)])
        return {
            "execution_result": res.content,
            "action_type": "SPEAK_RESPONSE",
            "json_payload": {
                "action": "CHAT_RESPONSE",
                "summary": res.content[:100]
            }
        }

def response_synthesizer_node(state: AgentState) -> Dict[str, Any]:
    execution = state.get("execution_result", "")
    
    prompt = f"""
    Summarize this execution result into a single, natural 1-sentence response for an AI assistant to speak out loud:
    "{execution}"
    """
    voice_spoken_text = llm.invoke([HumanMessage(content=prompt)]).content.strip()
    return {"final_response": voice_spoken_text}

workflow = StateGraph(AgentState)

workflow.add_node("classify_intent", intent_classifier_node)
workflow.add_node("execute_task", task_executor_node)
workflow.add_node("synthesize_response", response_synthesizer_node)

workflow.set_entry_point("classify_intent")
workflow.add_edge("classify_intent", "execute_task")
workflow.add_edge("execute_task", "synthesize_response")
workflow.add_edge("synthesize_response", END)

checkpointer = InMemorySaver()
nexus_agent_graph = workflow.compile(checkpointer=checkpointer)