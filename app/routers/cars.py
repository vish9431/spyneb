from fastapi import APIRouter, Depends, Form, HTTPException, status, UploadFile, File
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import car as car_models
from ..schemas import car as car_schemas
from ..utils.auth import get_current_user
from ..utils.image_handler import save_images
from sqlalchemy import or_

router = APIRouter(tags=["Cars"])

@router.post("/cars/", response_model=car_schemas.Car)
async def create_car(
    title: str = Form(...),
    description: str = Form(...),
    car_type: str = Form(...),
    company: str = Form(...),
    dealer: str = Form(...),
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    image_paths = await save_images(images)
    
    car = car_models.Car(
        title=title,
        description=description,
        car_type=car_type,
        company=company,
        dealer=dealer,
        images=image_paths,
        owner_id=current_user.id
    )
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

@router.get("/cars/", response_model=List[car_schemas.Car])
def list_cars(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(car_models.Car).filter(car_models.Car.owner_id == current_user.id)
    
    if search:
        query = query.filter(
            or_(
                car_models.Car.title.ilike(f"%{search}%"),
                car_models.Car.description.ilike(f"%{search}%"),
                car_models.Car.car_type.ilike(f"%{search}%"),
                car_models.Car.company.ilike(f"%{search}%"),
                car_models.Car.dealer.ilike(f"%{search}%")
            )
        )
    
    return query.all()

@router.get("/cars/{car_id}", response_model=car_schemas.Car)
def get_car(car_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    car = db.query(car_models.Car).filter(
        car_models.Car.id == car_id,
        car_models.Car.owner_id == current_user.id
    ).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.put("/cars/{car_id}", response_model=car_schemas.Car)
async def update_car(
    car_id: int,
    car_update: car_schemas.CarUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    car = db.query(car_models.Car).filter(
        car_models.Car.id == car_id,
        car_models.Car.owner_id == current_user.id
    ).first()
    
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    for key, value in car_update.dict().items():
        setattr(car, key, value)
    
    db.commit()
    db.refresh(car)
    return car

@router.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    car = db.query(car_models.Car).filter(
        car_models.Car.id == car_id,
        car_models.Car.owner_id == current_user.id
    ).first()
    
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    db.delete(car)
    db.commit()
    return {"message": "Car deleted successfully"}

