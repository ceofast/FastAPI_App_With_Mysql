from fastapi import FastAPI, status, HTTPException, Depends
import schemas
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import engine, get_db
import models

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

# Create all tables define in models module
models.Base.metadata.create_all(bind=engine)

# Get all customers
@app.get("/customers")
async def get_customer(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return customers

# Get customers by id
@app.get("/customers/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowCustomer)
async def get_customer_by_id(id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customerId == id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer ID: {id} has not found.")
    return customer

# Create a customer
@app.post("/customers", status_code=status.HTTP_201_CREATED)
async def create_customer(request: schemas.Customer, db: Session = Depends(get_db)):
    new_customer = models.Customer(customerId = request.customerId,
                                   customerFName = request.customerFName,
                                   customerLName = request.customerLName,
                                   customerEmail = request.customerEmail,
                                   customerPassword = request.customerPassword,
                                   customerStreet = request.customerStreet,
                                   customerCity = request.customerCity,
                                   customerState = request.customerState,
                                   customerZipcode = request.customerZipcode)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

# Delete a customer by id
@app.delete("/customers({id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_id(id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.customerId == id
    ).delete(synchronize_session=False)

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer ID: {id} has not found.")
    db.commit()
    return {"detail": f"Customer {id} deleted."}

# Update a customer
@app.put("/customer/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_customer_by_id(id: int, request: schemas.Customer, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.customerId == id
    )

    if not customer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer ID: {id} has not found.")
    customer.update(request.dict(), synchronize_session=False)
    db.commit()
    return {"detail": f"Customer ID: {id} updated."}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
def get_password_hash(password):
    return pwd_context.hash(password)

# Create User
@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.Showuser)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name = request.name,
        email = request.email,
        password = get_password_hash(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# customerCity = Caguas
@app.get("/customer/{city}")
async def filter_customer(city: str, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customerCity == city).limit(3).all()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tehere is no customer with {city} as city.")
    return customer