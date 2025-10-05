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
    stores: List[str]                    # 参与组合的两个商店的ID
    total: float                         # 组合后的最低总价
    assignment: Dict[str, str]           # 每个商品分配到哪个商店 {item -> store_id}


class SummaryResponse(BaseModel):
    items: List[str]
    stores: List[Dict]                   # 半径内的所有商店
    prices: List[PriceCell]              # 所有 (store, item) 的价格信息
    single_store_totals: List[SingleStoreTotal]  # 每家商店单独买的总价
    best_single_store: Optional[BestSingleStore] = None  # 最便宜的单店
    best_two_store_combo: Optional[BestTwoStoreCombo] = None  # ✅ 新增字段
