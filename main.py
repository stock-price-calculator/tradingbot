import sys


import constants
from kiwoom import Kiwoom
# from account.account_sender import Kiwoom_Send_Account
# from order.trade import Kiwoom_Trade
# from market.stick_data_sender import Kiwoom_Price

from fastapi import FastAPI  # FastAPI import
from typing import Union


from fastapi import FastAPI
from typing import Optional, Union

kiwoom = Kiwoom()  # Kiwoom 클래스 인스턴스 생성


app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
async def read_root():
    if not kiwoom.get_connect_state():
        return {"message": "키움증권에 접속할 수 없습니다."}
    price = await kiwoom.get_master_last_price("005930")  # 삼성전자의 종목코드를 전달하여 가격 조회
    return {"samsung_price": price}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)