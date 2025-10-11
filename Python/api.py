from fastapi import FastAPI
from fastapi.responses import *
from pydantic import BaseModel
import uvicorn
import ConnectionPool as cp
import pandas as pd


app = FastAPI()
data = pd.DataFrame
UserSessions = []

class CategoryFilter(BaseModel):
    BusWidth: str = None,
    Cores: str = None,
    GraphicsProcessor: str = None,
    ImagePath: str = None,
    MemorySize: str = None,
    MemoryType: str = None,
    Name: str = None,
    ROPS: str = None,
    TMUS: str = None

def _fetchCategories():
    conn = cp.connToSQL()
    cursor = conn.cursor()
    query = '''
                    select 
                        gp.Name as ProductName
                        ,gp.GraphicsProcessor
                        ,gp.Cores
                        ,gp.TMUS
                        ,gp.ROPS
                        ,gp.MemorySize
                        ,gp.MemoryType
                        ,gp.BusWidth
                        ,800800 as MediumPrice
                        ,gp.ImagePath
                    from 
                        dbo.GPUs as gp
                '''
    cursor.execute(query)
    data = [list(row) for row in cursor.fetchall()]
    conn.close()
    data = pd.DataFrame(data=data, columns=['ProductName', 'GraphicsProcessor', 'Cores', 'TMUS', 'ROPS', 'MemorySize', 'MemoryType', 'BusWidth', 'MediumPrice', 'ImagePath'])
    # data = data.query('ProductName == "NVIDIA GeForce RTX 5090"')
    return data

def _fetchData():
    conn = cp.connToSQL()
    cursor = conn.cursor()
    query = '''
                select 
                    rd.ProductName
                    ,rd.Price
                    ,sh.ShopName
                    ,rd.InsertDate
                from 
                    dbo.RawData as rd
                    join dbo.Shops as sh on
                        sh.Id = rd.ShopId
            '''
    cursor.execute(query)
    data = [list(row) for row in cursor.fetchall()]
    conn.close()
    data = pd.DataFrame(data=data, columns=['ProductName', 'Price', 'ShopName', 'InsertDate'])
    return data

def _sortData(predicates: list[list]):
    pass



@app.post("/createSession")
async def createSession(sessionGUID: str):
    try:
        userData = _fetchCategories()
        UserSessions.append([sessionGUID, userData])
    except:
        return JSONResponse(content={"result": False})
    finally:
        return JSONResponse(content={"result": True})

@app.post("/filterCategories")
async def filterCategories(params: CategoryFilter):
    return JSONResponse(content={"result": params})


@app.get("/assets/{id}", response_class=FileResponse)
async def cards(id):
    return f'../Assets/{id}'

@app.get("/getCategories")
async def getCategories():
    productCategories = categories[
        [
            'ProductName',
            'GraphicsProcessor',
            'Cores',
            'TMUS',
            'ROPS',
            'MemorySize',
            'MemoryType',
            'BusWidth',
            'MediumPrice',
            'ImagePath'
        ]
    ].astype('string').values.tolist()
    products = [
        {
            "productName" : productName,
            "graphicsProcessor" : graphicsProcessor,
            "cores": cores,
            "tmus": tmus,
            "rops": rops,
            "memorySize": memorySize,
            "memoryType": memoryType,
            "busWidth": busWidth,
            "mediumPrice": mediumPrice,
            "imagePath": imagePath
        }
        for
            productName,
            graphicsProcessor,
            cores,
            tmus,
            rops,
            memorySize,
            memoryType,
            busWidth,
            mediumPrice,
            imagePath
        in productCategories
    ]
    return JSONResponse(content=products)

@app.get("/getVideoCards")
async def getVideoCards():
    videocards = data[['ProductName', 'Price']].astype('string').values.tolist()
    products = [
        {"productName": name, "price": price}
        for name, price in videocards
    ]
    return JSONResponse(content=products)

@app.get("/link")
async def link():
    data = """
    <html>
        <a target="_blank" rel="noopener noreferrer" href="https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?order=2&stock=now-today-tomorrow-later">DNS.com</a>
    </html>
    """
    return HTMLResponse(data)

data = _fetchData()
categories = _fetchCategories()
# print(categories.columns.tolist())

if __name__ == "__main__":
    uvicorn.run("api:app", port=5000, log_level="info")
# uvicorn main:app --reload