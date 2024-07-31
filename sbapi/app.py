from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from .llm import run_query

app = FastAPI()

class InputData(BaseModel):
    query: str
    context: str


@app.post("/process")
async def process_input(data: InputData):
    # Process the input data
    reponse = run_query(data.query, data.context)
    result = {
        "llm_response": reponse,
        "processed_result": f"Processed: {data.query} with context {data.context}"
    }
    return JSONResponse(content=result)

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
