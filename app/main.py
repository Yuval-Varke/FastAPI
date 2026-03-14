from fastapi import FastAPI, HTTPException, Query
from service.products import get_all_products

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running"}


# @app.get('/products')
# def get_products():
#     return get_all_products()


@app.get('/products')
def list_products(name:str=Query(None,min_length=1,max_length=50,description="Filter products by name")):
    products = get_all_products()
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get('name', '').lower()]
        if not products:
            raise HTTPException(status_code=404, detail=f"No products found matching name: {name}")
        total = len(products)
        return {
            "total": total,
            "products": products
        }
    return products