from logging import exception

from IPython.core.display_functions import display
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
UserSessions = {}
# UserSessions = {'sessionId': {'categoryFilters': {'productName': null, ...}, 'productFilters': }}

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
            gp.Id as CategoryId
            ,gp.Name as ProductName
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
    _data = [list(row) for row in cursor.fetchall()]
    conn.close()
    _dataInDF = pd.DataFrame(data=_data, columns=['categoryId', 'productName', 'graphicsProcessor', 'cores', 'TMUS', 'ROPS', 'memorySize',
                                                'memoryType', 'busWidth', 'mediumPrice', 'imagePath'])
    return _dataInDF

def _fetchProducts():
    conn = cp.connToSQL()
    cursor = conn.cursor()
    query = '''
                select 
                    rd.ProductName
                    ,rd.Price
                    ,sh.ShopName
                    ,rd.InsertDate
                    ,rd.CategoryId
                from 
                    dbo.RawData as rd
                    join dbo.Shops as sh on
                        sh.Id = rd.ShopId
                where
                    rd.CategoryId is not null
            '''
    cursor.execute(query)
    _data = [list(row) for row in cursor.fetchall()]
    conn.close()
    _dataInDF = pd.DataFrame(data=_data, columns=['productName', 'price', 'shopName', 'insertDate', 'categoryId'])
    return _dataInDF


@app.post("/createSession")
async def createSession(sessionId: str):
    try:
        UserSessions[sessionId] = {'categoryFilters': {}, 'productFilters': {}}
    except:
        return JSONResponse(content={"result": False})
    finally:
        logger.info(UserSessions)
        return JSONResponse(content={"result": True})


@app.post("/filterCategories/{sessionId}")
async def filterCategories(sessionId: str, params: CategoryFilter):
    try:
        UserSessions[sessionId]['categoryFilters'] = params
        logger.info(f'Для сессии {sessionId} были переданы параметры: {params}')
        return JSONResponse(content={"result": True})
    except:
        logger.error(f'Не получилось обновить параметры сессии. Сессия: {sessionId}, данные: {params}')
        return JSONResponse(content={"result": True})


@app.get("/getCategories/{sessionId}")
async def getCategories(sessionId: str):
    query_string = ''
    filterValues = UserSessions[sessionId]['categoryFilters']
    if filterValues != {}:
        # Собираем строку запроса
        for elem in filterValues:
            if elem[1] != '':
                if query_string != '':
                    query_string = query_string + ' and '
                query_string = query_string + f'{elem[0]}.str.contains("{elem[1]}")'

    if query_string != '':
        userCategories = categories.query(query_string)
    else:
        userCategories = categories
    _data = userCategories[
        [
            'categoryId',
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
    _categories = [
        {
            "categoryId": categoryId,
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
            categoryId,
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
        in _data
    ]
    return JSONResponse(content=_categories)


@app.post("/filterProducts/{sessionId}")
async def filterProducts(sessionId: str):
    pass


@app.get("/getProductsByCategory/{sessionId}/{categoryId}")
async def getProductsByCategory(sessionId: str, categoryId: str):
    if categoryId is None:
        logger.error('В метод getProductsByCategory не был передан идентификатор категории')
    userProducts = products.query(f'categoryId == {int(categoryId)}')
    _data = userProducts[
        [
            'productName',
            'price',
        ]
    ].astype('string').values.tolist()
    _products = [
        {
            "productName": name,
            "price": price
        }
        for
            name,
            price
        in _data
    ]
    return JSONResponse(content=_products)


@app.get("/getUniqueValues/{sessionId}/{columnName}/{listType}")
async def getUniqueValues(sessionId: str, columnName: str, listType: int):
    try:
        if listType == 1:
            uniqueValues = categories[columnName].unique().tolist()
            uniqueValues.insert(0, '')
        elif listType == 2:
            uniqueValues = products[columnName].unique().tolist()
            uniqueValues.insert(0, '')
        return JSONResponse(content=uniqueValues)
    except Exception as e:
        logger.error(e)
        return JSONResponse(content={'result': 'No data available'})


@app.get("/assets/{id}", response_class=FileResponse)
async def cards(id):
    return f'../Assets/{id}'


@app.get("/link")
# Нужно для работы скраппера DNS
async def link():
    data = """
    <html>
        <a target="_blank" rel="noopener noreferrer" href="https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?order=2&stock=now-today-tomorrow-later">DNS.com</a>
    </html>
    """
    return HTMLResponse(data)


products = _fetchProducts()
categories = _fetchCategories()
# print(categories.columns.tolist())


if __name__ == "__main__":
    uvicorn.run("api:app", host='0.0.0.0' ,port=8000, log_level="info")
# uvicorn main:app --reload
