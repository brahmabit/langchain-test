from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List
from app.api.data.pizza import pizza_menu

ORDER_COUNTER = 0

router = APIRouter(
    prefix="/v1/menu"
)

@router.get("")
def get_menu(req: Request, name: str):

    data = []
    for m in pizza_menu:
        if m.get('name') == name:
            data.append(m)

    return JSONResponse(status_code = 200, content = {"Success": True, "Data": data})

router2 = APIRouter(
    prefix="/v1/order"
)

@router2.post("")
async def create_order(req: Request):
    req_json = await req.json()
    global ORDER_COUNTER
    print(ORDER_COUNTER)
    order_id = str(ORDER_COUNTER).rjust(4, "0")
    ORDER_COUNTER = ORDER_COUNTER + 1

    total_value = 0
    for order in req_json.get('order', []):
        for m in pizza_menu:
            if m.get('id') == order.get('id'):
                total_value = total_value + m.get('price', 0) * order.get('quantity', 0)
                break

    return JSONResponse(status_code = 200, content = {"Success": True, "Data": {"order_id": order_id, "price": total_value}})
        
    