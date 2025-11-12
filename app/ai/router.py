from fastapi import APIRouter
from pydantic import BaseModel


class AIRouteRequest(BaseModel):
    tenant_id: str
    message: str
    client_id: str | None = None


class AIRouteResponse(BaseModel):
    intent: str
    suggestions: list[str]


router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/route", response_model=AIRouteResponse)
async def route_message(payload: AIRouteRequest) -> AIRouteResponse:
    message_lower = payload.message.lower()
    if any(keyword in message_lower for keyword in ["book", "appointment", "schedule"]):
        return AIRouteResponse(intent="book_appointment", suggestions=["Suggest timeslot", "Collect client info"])

    return AIRouteResponse(intent="answer_from_kb", suggestions=["Search knowledge base", "Escalate to operator"])
