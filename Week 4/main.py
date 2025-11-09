from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import urllib.request as url_request
import json

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="b9178e7811b6cb5238c6e7df291ca264")

# 設定路徑
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 抓取並整理飯店資料
def fetch_hotels():
    url_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
    url_eng = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
    
    with url_request.urlopen(url_ch) as response:
        data_ch = json.loads(response.read().decode("utf-8"))
    with url_request.urlopen(url_eng) as response:
        data_eng = json.loads(response.read().decode("utf-8"))
    
    # 排序並合併資料
    list_ch = sorted(data_ch['list'], key=lambda x: x['_id'])
    list_eng = sorted(data_eng['list'], key=lambda x: x['_id'])
    
    return [
        {
            'hotel_id': ch['_id'],
            'chinese_name': ch['旅宿名稱'],
            'english_name': eng['hotel name'],
            'phone': ch['電話或手機號碼'],
        }
        for ch, eng in zip(list_ch, list_eng)
    ]

hotels_result = fetch_hotels()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login")
async def login(request: Request, email: str = Form(), password: str = Form()):
    if not email or not password:
        return RedirectResponse(url="/ohoh?msg=請輸入信箱和密碼", status_code=303)
    
    if email == "abc@abc.com" and password == "abc":
        request.session["LOGGED_IN"] = True
        return RedirectResponse(url="/member", status_code=303)
    
    return RedirectResponse(url="/ohoh?msg=信箱或密碼輸入錯誤", status_code=303)


@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if not request.session.get("LOGGED_IN"):
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("member.html", {"request": request})


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()  
    return RedirectResponse(url="/", status_code=303)


@app.get("/ohoh", response_class=HTMLResponse)
async def ohoh(request: Request, msg: str):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg})


@app.get("/hotel/{hotel_id}", response_class=HTMLResponse)
async def hotel(request: Request, hotel_id: int):
    hotel_data = next((h for h in hotels_result if h['hotel_id'] == hotel_id), None)
    return templates.TemplateResponse("hotel.html", {"request": request, "hotel": hotel_data})