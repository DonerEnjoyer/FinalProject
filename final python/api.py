import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Response
from sqlalchemy import Column, Integer, String, create_engine, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "sqlite:///bim_market.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    class Config:
        orm_mode = True 

class ProductCreate(BaseModel):
    name: str
    type: str
    cost: str
    class Config:
        orm_mode = True 
    
class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=False, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Products(Base):
    __tablename__ = "Products"
    product_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    type = Column(String(10), nullable=False)
    description = Column(String(50), nullable=False)
    cost = Column(Integer, nullable=False)
    picture_data = Column(LargeBinary, nullable=True) 
    picture_mimetype = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)
app = FastAPI()
 

class FastU:

    @app.post("/users/")
    async def create(user: UserCreate):
        db = SessionLocal()
        new_user = Users(
            name=user.name,
            email=user.email,
            phone=user.phone,
            password=user.password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @app.post("/users/{user_id}/upload-picture/")
    async def upload_user_picture(user_id: int, file: UploadFile = File(...)):
        db = SessionLocal()
        user = db.query(Users).filter(Users.id == user_id).first()
        user.picture_data = await file.read()
        user.picture_mimetype = file.content_type
        db.commit()
        db.refresh(user)
        return {"message": "Picture uploaded successfully"}

    @app.get("/users/get/{name}")
    async def read(name: str):
        db = SessionLocal()
        user = db.query(Users).filter(Users.name == name).first()
        if user:
            return user.name 
        else:
            return "NotFound"

    @app.get("/users/{id}/picture/")
    async def get_user_picture(id: int):
        db = SessionLocal()
        user = db.query(Users).filter(Users.id == id).first()
        if not user or not user.picture_data:
            raise HTTPException(status_code=404, detail="Picture not found")
        return Response(content=user.picture_data, media_type=user.picture_mimetype)

    @app.put("/users/update/{id}")
    async def update(id: int, user: UserCreate):
        db = SessionLocal()
        upd_user = db.query(Users).filter(Users.id == id).first()
        upd_user.name = user.name
        upd_user.email = user.email
        upd_user.phone = user.phone
        upd_user.password = user.password
        db.commit()
        return upd_user
    
    @app.delete("/users/{id}/delete-picture/")
    async def delete_picture(id: int):
        db = SessionLocal()
        user = db.query(Users).filter(Users.id == id).first()
        user.picture_data = None
        user.picture_mimetype = None
        db.commit()
        return "Success"



    @app.delete("/users/delete/{id}")
    async def delete(id: int):
        db = SessionLocal()
        user = db.query(Users).filter(Users.id == id).first()
        db.delete(user)
        db.commit()
        return "User deleted successfully"
'''////////////////////////////////////////////////Products////////////////////////////////////////////////'''   
class FastP:
    @app.post("/products/")
    async def create(new_product: ProductCreate):
        db = SessionLocal()
        new_product = Products(name=new_product.name, type=new_product.type, cost=new_product.cost)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    
    @app.post("/products/{product_id}/upload-picture/")
    async def upload_product_picture(product_id: int, file: UploadFile = File(...)):
        db = SessionLocal()
        product = db.query(Products).filter(Products.product_id == product_id).first()
        product.picture_data = await file.read()
        product.picture_mimetype = file.content_type
        db.commit()
        db.refresh(product)
        return {"message": "Picture uploaded successfully"}
 
    @app.get("/products/get/{name}")
    async def read(name: str):
        db = SessionLocal()
        product = db.query(Products).filter(Products.name == name).first()
        if product:
            return product.name
        else:
            return "NotFound"

    @app.get("/products/getall/")
    async def read():
        db = SessionLocal()
        product = db.query(Products).all()
        if product:
            return product
        else:
            return "NotFound"  

    @app.get("/products/{product_id}/picture/")
    async def get_product_picture(product_id: int):
        db = SessionLocal()
        product = db.query(Products).filter(Products.product_id == product_id).first()

        if not product or not product.picture_data:
            raise HTTPException(status_code=404, detail="Picture not found")
        return Response(content=product.picture_data, media_type=product.picture_mimetype)
          

    @app.put("/products/update/{product_id}")
    async def update(product_id: int, product: ProductCreate):
        db = SessionLocal()
        upd_product = db.query(Products).filter(Products.product_id == product_id).first()
        upd_product.name = product.name
        upd_product.type = product.type
        upd_product.cost = product.cost
        db.commit()
        return upd_product

    @app.delete("/products/delete/{product_id}")
    async def delete(product_id: int):
        db = SessionLocal()
        product = db.query(Products).filter(Products.product_id == product_id).first()
        db.delete(product)
        db.commit()
        return "Product deleted successfully"
    
    @app.delete("/products/{product_id}/delete-picture/")
    async def delete_picture(product_id: int):
        db = SessionLocal()
        prod = db.query(Products).filter(Products.product_id == product_id).first()
        prod.picture_data = None
        prod.picture_mimetype = None
        db.commit()
        return "Success"
