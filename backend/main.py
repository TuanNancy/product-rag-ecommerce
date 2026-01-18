from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import products

app = FastAPI(
    title="Product RAG E-commerce API",
    description="FastAPI backend for product e-commerce with RAG chatbot",
    version="1.0.0"
)

# CORS middleware để frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Product RAG E-commerce API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
