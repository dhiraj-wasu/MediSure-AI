from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_Agent.redis_state import load_state, save_state
from app.services.chat_Agent.conversational_agent import ConversationalAgent

router = APIRouter()
agent = ConversationalAgent()

@router.post("/", response_model=ChatResponse)
def chat(req: ChatRequest):

    state = load_state(req.session_id)
    print("Current state:\n", state)  
    reply, updated_state, payload = agent.run(state, req.message)

    save_state(req.session_id, updated_state)

    return ChatResponse(message=reply)
