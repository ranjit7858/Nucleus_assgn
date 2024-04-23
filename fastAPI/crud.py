from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = f"mysql://ranjit:ranjit7858@localhost:3306/other"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
 
 
Base.metadata.create_all(bind=engine)



app = FastAPI()

@app.post("/add_items/")
async def create_item(name: str, description: str):
    db = SessionLocal()
    db_item = Item(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
@app.get("/read_items/{item_id}")
async def read_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    return item

@app.put("/update_items/{item_id}")
async def update_item(item_id: int, name: str, description: str):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db_item.name = name
    db_item.description = description
    db.commit()
    return db_item

@app.delete("/del_items/{item_id}")
async def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}
 
 