from fastapi import FastAPI
from fastapi.responses import *
from pydantic import BaseModel
import uvicorn
import ConnectionPool as cp
import pandas as pd
import json
import logging
logger = logging.getLogger("uvicorn")

app = FastAPI()
data = pd.DataFrame
UserSessions = {}


class CategoryFilter(BaseModel):
    productName: str
    graphicsProcessor: str
    memorySize: str
    memoryType: str
    busWidth: str
    mediumPrice: str

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
    data = pd.DataFrame(data=data, columns=['productName', 'graphicsProcessor', 'cores', 'TMUS', 'ROPS', 'memorySize',
                                            'memoryType', 'busWidth', 'mediumPrice', 'imagePath'])
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

@app.post("/createSession")
async def createSession(sessionId: str):
    try:
        UserSessions[sessionId] = {'filters': {}, 'data': pd.DataFrame}
    except:
        return JSONResponse(content={"result": False})
    finally:
        print(UserSessions)
        return JSONResponse(content={"result": True})


@app.post("/filterCategories/{sessionId}")
async def filterCategories(sessionId: str, params: CategoryFilter):
    try:
        UserSessions[sessionId]['filters'] = params
        print(f'Для сессии {sessionId} были переданы параметры: {params}')
        return JSONResponse(content={"result": True})
    except:
        print(f'Не получилось обновить параметры сессии. Сессия: {sessionId}, данные: {params}')
        return JSONResponse(content={"result": True})

@app.get("/assets/{id}", response_class=FileResponse)
async def cards(id):
    return f'../Assets/{id}'


@app.get("/getCategories/{sessionId}")
async def getCategories(sessionId: str):
    query_string = ''
    userCategories = categories
    filterValues = UserSessions[sessionId]['filters']
    if filterValues == {}:
        print('Пусто')
    else:
        # Собираем строку запроса
        for elem in filterValues:
            if elem[1] != '':
                if query_string != '':
                    query_string = query_string + ' and '
                query_string = query_string + f'{elem[0]}.str.contains("{elem[1]}")'

    if query_string != '':
        userCategories = categories.query(query_string)
    productCategories = userCategories[
        [
            'productName',
            'graphicsProcessor',
            'cores',
            'TMUS',
            'ROPS',
            'memorySize',
            'memoryType',
            'busWidth',
            'mediumPrice',
            'imagePath'
        ]
    ].astype('string').values.tolist()
    products = [
        {
            "productName": productName,
            "graphicsProcessor": graphicsProcessor,
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

@app.get("/getUniqueValues/{sessionId}/{columnName}")
async def getUniqueValues(sessionId: str, columnName: str):
    try:
        uniqueValues = categories[columnName].unique().tolist()
        uniqueValues.insert(0, '')
        return JSONResponse(content=uniqueValues)
    except Exception as e:
        logger.error(e)
        return JSONResponse(content={'result': 'No data available'})

@app.get("/link")
# Нужно для работы скраппера DNS
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
    uvicorn.run("api:app", host='0.0.0.0' ,port=8000, log_level="info")
# uvicorn main:app --reload
