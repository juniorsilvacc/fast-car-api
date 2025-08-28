from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_car_api.database import get_session
from fast_car_api.models import Car
from fast_car_api.schemas import (
    CarList,
    CarPartialUpdate,
    CarPublic,
    CarSchema,
)

router = APIRouter(
    prefix='/api/v1/cars',
    tags=['cars'],
)


@router.post(
    '/', response_model=CarPublic, status_code=status.HTTP_201_CREATED
)
def create_car(car: CarSchema, db: Session = Depends(get_session)):
    car = Car(**car.model_dump())
    db.add(car)  # adiciona o objeto ao banco
    db.commit()  # confirma a transação
    db.refresh(car)  # atualiza o objeto com os dados do banco (ex: id gerado)
    return car


@router.get('/', response_model=CarList, status_code=status.HTTP_200_OK)
def list_cars(
    db: Session = Depends(get_session), offset: int = 0, limit: int = 100
):
    query = db.scalars(select(Car).offset(offset).limit(limit))
    cars = query.all()
    return {'cars': cars}


@router.get(
    path='/{car_id}', response_model=CarPublic, status_code=status.HTTP_200_OK
)
def get_car(car_id: int, db: Session = Depends(get_session)):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Car not found',
        )
    return car


@router.put(
    '/{car_id}', response_model=CarPublic, status_code=status.HTTP_200_OK
)
def update_car(
    car_id: int, car_update: CarSchema, db: Session = Depends(get_session)
):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Car not found',
        )

    for field, value in car_update.model_dump().items():
        setattr(car, field, value)

    db.commit()
    db.refresh(car)
    return car


@router.patch(
    '/{car_id}', response_model=CarPublic, status_code=status.HTTP_200_OK
)
def patch_car(
    car_id: int, car_data: CarPartialUpdate, db: Session = Depends(get_session)
):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Car not found',
        )

    update_data = car_data.model_dump(exclude_unset=True)  # só os enviados
    for field, value in update_data.items():
        setattr(car, field, value)

    db.commit()
    db.refresh(car)
    return car


@router.delete('/{car_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, db: Session = Depends(get_session)):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail='Car not found')

    db.delete(car)
    db.commit()
