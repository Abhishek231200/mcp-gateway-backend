from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(title="Backend API", version="1.0.0")

VALID_KEYS = {"key-user-1", "key-user-2", "key-admin"}

class TokenRequest(BaseModel):
    api_key: str

class TokenResponse(BaseModel):
    token: str
    expires_in: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/token", response_model=TokenResponse)
def get_token(req: TokenRequest):
    if req.api_key not in VALID_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {"token": f"tok-{req.api_key}-xyz", "expires_in": 3600}

@app.post("/auth/refresh")
def refresh_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer tok-"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"token": authorization.replace("Bearer ", "") + "-refreshed", "expires_in": 3600}

@app.get("/auth/validate")
def validate_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer tok-"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"valid": True, "actor": authorization.split("-")[1]}
