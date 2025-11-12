from fastapi import FastAPI

from app.ai.router import router as ai_router
from app.routers import auth, appointments, clients, deals, services, staff, tenant

app = FastAPI(title="Tenant Scheduling API")

app.include_router(tenant.router)
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(services.router)
app.include_router(staff.router)
app.include_router(appointments.router)
app.include_router(deals.router)
app.include_router(ai_router)
