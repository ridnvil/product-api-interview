from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import csv
from io import StringIO
from models.products import Product
from config.base import get_db, Base, engine
from pydantic import BaseModel

app = FastAPI(title="Products API")

# Create tables if not exist
Base.metadata.create_all(bind=engine)

class ProductSchema(BaseModel):
    id: int = None
    name: str
    price: float
    quantity: int

    @classmethod
    def validate_product(cls, product):
        errors = []
        if not product.name or not product.name.strip():
            errors.append("Name is required.")
        if product.price is None or product.price < 0:
            errors.append("Price must be a non-negative number.")
        if product.quantity is None or product.quantity < 0:
            errors.append("Quantity must be a non-negative integer.")
        return errors

@app.get("/products/export")
def export_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'name', 'price', 'quantity'])
    for p in products:
        price = float(p.price) if p.price is not None else 0
        cw.writerow([p.id, p.name, price, p.quantity])
    output = si.getvalue().encode('utf-8')
    return StreamingResponse(
        iter([output]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products.csv"}
    )

@app.post("/products/import")
def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(StringIO(content))
    for row in reader:
        db.add(Product(name=row['name'], price=row['price'], quantity=row.get('quantity', 0)))
    db.commit()
    return {"detail": "Products imported"}

@app.get("/products", response_model=List[ProductSchema])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/products/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=ProductSchema)
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    errors = ProductSchema.validate_product(product)
    if errors:
        raise HTTPException(status_code=422, detail=errors)
    db_product = Product(name=product.name, price=product.price, quantity=product.quantity)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductSchema, db: Session = Depends(get_db)):
    db_product = db.query(Product).get(product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    errors = ProductSchema.validate_product(product)
    if errors:
        raise HTTPException(status_code=422, detail=errors)
    db_product.name = product.name
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).get(product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}

@app.delete("/products")
def delete_all_products(db: Session = Depends(get_db)):
    db.query(Product).delete()
    db.commit()
    return {"detail": "All products deleted"}