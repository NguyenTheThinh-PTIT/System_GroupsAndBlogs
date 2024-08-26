from fastapi import status, HTTPException, Depends, APIRouter, FastAPI, Response
from sqlalchemy.orm import Session
from .. import schemas, utils, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.username == user.username)
    user_found = user_query.first()

    if user_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"username: {user.username} already existd")
    
    utils.validate_password_strength(user.password)

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)

    return new_user  

@router.put("/update", response_model=schemas.UserOut)
async def update_user(user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.user_id == current_user.user_id).first()

    user.username = user_update.username
    user.password = utils.hash(user_update.password)
    user.email = user_update.email
    user.full_name = user_update.full_name

    db.commit()
    db.refresh(user)
    return user




