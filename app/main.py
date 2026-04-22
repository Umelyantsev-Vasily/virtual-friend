from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.v1 import router as v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database connected and tables created")
    yield
    await engine.dispose()
    print("✅ Database disconnected")

app = FastAPI(
    title="Virtual Friend",
    description="AI Companion with long-term memory",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Virtual Friend API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}