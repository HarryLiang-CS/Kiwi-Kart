from fastapi import APIRouter, HTTPException
from app.models.dto import SummaryRequest, SummaryResponse
from app.services.summary_single import build_single_store_summary

router = APIRouter(tags=["summary"])

@router.post("/summary", response_model=SummaryResponse)
def summary(req: SummaryRequest):
    try:
        return build_single_store_summary(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
