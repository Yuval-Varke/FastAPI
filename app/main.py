from fastapi import FastAPI, HTTPException, Query, Path
from service.products import get_all_products

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running"}


# @app.get('/products')
# def get_products():
#     return get_all_products()


@app.get('/products')
def list_products(
    name:str=Query(
        None,
        min_length=1,
        max_length=50,
        description="Filter products by name"
    ),

    sort_by_price:bool=Query(
        default=False,
        description="Sort products by price in ascending order"
    ),

    order:str=Query(
        default="asc",
        description="Order of sorting: 'asc' for ascending, 'desc' for descending"
    ),

    limit:int=Query(
        default=5,
        ge=1,
        le=100,
        description="Limit the number of products returned"
    )
):
    products = get_all_products()
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get('name', '').lower()]
    if not products:
        raise HTTPException(status_code=404, detail=f"No products found matching name: {name}")
    if sort_by_price:
        products.sort(key=lambda p: p.get('price', 0), reverse=(order == "desc"))


    if sort_by_price:
        reverse = (order=="desc")
        products = sorted(products,key=lambda p: p.get('price', 0), reverse=reverse)



    total = len(products)
    products = products[:limit]
    return {
        "total": total,
        "products": products,
        "limit": limit
    }



@app.get('/products/{product_id}')
def get_product(product_id: str = Path(...,min_length=1, max_length=100,example='1' ,description="The ID of the product to retrieve")):
    products = get_all_products()
    for product in products:
        if product['id'] == product_id:
            return product
    raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")