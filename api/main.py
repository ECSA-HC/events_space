from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    auth, users, roles, permissions, countries, org_units, events
)

app = FastAPI(
    title="ECSA Events Space API Documentation",
    description="The ECSA Events Space API is an API for ECSA Events Management System.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Joel",
        "url": "https://github.com/jkumwenda",
        "email": "jkumwenda@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# ✅ Mount after FastAPI is initialized
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

origins = [
    "https://events.ecsaconm.org",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, tags=["Auth"], prefix="/auth")
app.include_router(users.router, tags=["Users"], prefix="/users")
app.include_router(roles.router, tags=["Roles"], prefix="/roles")
app.include_router(permissions.router, tags=["Permissions"], prefix="/permissions")
app.include_router(countries.router, tags=["Countries"], prefix="/countries")
app.include_router(org_units.router, tags=["Org units"], prefix="/org_units")
app.include_router(events.router, tags=["Events"], prefix="/events")
