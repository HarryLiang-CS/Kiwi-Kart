from typing import Dict, Tuple, List
from app.models.dto import SummaryRequest, SummaryResponse, PriceCell, SingleStoreTotal, BestSingleStore
from app.repositories.data_access import load_stores, load_prices
from app.services.geo import haversine_km

DEFAULT_UNIT = {"milk": "L", "eggs": "each", "bread": "each"}

def _norm(s: str) -> str:
    return s.strip().lower()

def build_single_store_summary(req: SummaryRequest) -> SummaryResponse:
    items = [_norm(x) for x in req.items]#给每个items去空格以及小写

    stores_all = load_stores()#读取json文件，返回store值
    stores_in = []# empty list
    for s in stores_all:
        d = haversine_km(req.user_lat, req.user_lng, s["lat"], s["lng"])
        if d <= req.radius_km:
            stores_in.append({**s, "distance_km": round(d, 2)})
    if not stores_in:
        raise ValueError("No stores within the radius.")

    # 2) 价格映射 (store,item)->最低价
    prices = load_prices()
    price_map: Dict[Tuple[str, str], float] = {}
    allowed = {s["id"] for s in stores_in}
    for r in prices:
        if r["store_id"] in allowed:
            key = (r["store_id"], _norm(r["item_key"]))
            if (key not in price_map) or (r["price"] < price_map[key]):
                price_map[key] = r["price"]

    # 3) 输出给前端画表的 cells
    cells: List[PriceCell] = []
    for (sid, it), p in price_map.items():
        cells.append(PriceCell(store_id=sid, item=it, unit=DEFAULT_UNIT.get(it, "each"), price=float(p)))

    # 4) 每家店的总价（假设都不缺货）
    singles: List[SingleStoreTotal] = []
    for s in stores_in:
        total = 0.0
        for it in items:
            key = (s["id"], it)
            if key not in price_map:
                raise ValueError(f"Missing price for {it} at {s['id']}")
            total += price_map[key]
        singles.append(SingleStoreTotal(store_id=s["id"], total=round(total, 2)))

    # 5) 选最便宜的一家（并列则距离近者优先）
    singles_sorted = sorted(
        singles,
        key=lambda x: (x.total, next(st["distance_km"] for st in stores_in if st["id"] == x.store_id))
    )
    best = singles_sorted[0]
    best_store = next(st for st in stores_in if st["id"] == best.store_id)
    assignment = {it: best.store_id for it in items}

    best_summary = BestSingleStore(
        store_id=best.store_id,
        store_name=best_store["name"],
        total=best.total,
        assignment=assignment
    )

    return SummaryResponse(
        items=items,
        stores=stores_in,
        prices=cells,
        single_store_totals=singles_sorted,
        best_single_store=best_summary
    )
