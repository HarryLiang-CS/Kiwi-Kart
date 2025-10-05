from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class SummaryRequest(BaseModel):
    items: List[str]
    user_lat: float
    user_lng: float
    radius_km: float = Field(default=5.0)

class PriceCell(BaseModel):
    store_id: str
    item: str
    unit: str
    price: float

class SingleStoreTotal(BaseModel):
    store_id: str
    total: float

class BestSingleStore(BaseModel):
    store_id: str
    store_name: str
    total: float
    assignment: Dict[str, str] 

class BestTwoStoreCombo(BaseModel):
    stores: List[str]                    
    total: float                        
    assignment: Dict[str, str]           


class SummaryResponse(BaseModel):
    items: List[str]
    stores: List[Dict]                   
    prices: List[PriceCell]             
    single_store_totals: List[SingleStoreTotal]  
    best_single_store: Optional[BestSingleStore] = None  
    best_two_store_combo: Optional[BestTwoStoreCombo] = None  
