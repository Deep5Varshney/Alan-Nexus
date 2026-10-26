import os
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from agents.graph import nexus_agent_graph

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("alan-nexus")

app = FastAPI(title="Alan-Nexus Engine API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AlanVoiceRequest(BaseModel):
    user_input: str = Field(..., description="Transcribed voice command")
    session_id: Optional[str] = Field(default="default_session", description="Conversation thread ID")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)

class AlanVoiceResponse(BaseModel):
    status: str
    spoken_text: str
    intent: str
    session_id: str
    json_payload: Dict[str, Any]

@app.get("/")
def health_check():
    return {"status": "online", "service": "Alan-Nexus Stateful Engine"}

@app.post("/api/nexus/voice", response_model=AlanVoiceResponse)
async def process_voice_command(request: AlanVoiceRequest):
    if not request.user_input.strip():
        raise HTTPException(status_code=400, detail="User input text cannot be empty.")
    
    logger.info(f"Processing command for session '{request.session_id}': '{request.user_input}'")
    
    try:
        initial_state = {
            "input_text": request.user_input,
            "context": request.context or {},
            "intent": "",
            "action_type": "",
            "execution_result": None,
            "final_response": "",
            "json_payload": {}
        }
        
        config = {"configurable": {"thread_id": request.session_id}}
        final_state = nexus_agent_graph.invoke(initial_state, config=config)
        
        return AlanVoiceResponse(
            status="success",
            spoken_text=final_state.get("final_response", "Done."),
            intent=final_state.get("intent", "GENERAL_QA"),
            session_id=request.session_id,
            json_payload=final_state.get("json_payload", {})
        )
        
    except Exception as e:
        logger.error(f"Execution Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Nexus Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)