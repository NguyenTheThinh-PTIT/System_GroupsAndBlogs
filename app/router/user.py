from fastapi import status, HTTPException, Depends, APIRouter, FastAPI, Response
from sqlalchemy.orm import Session
from .. import schemas, utils, models, oauth2
from ..database import get_db
from sqlalchemy import or_

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.get("/{group_id}", response_model= list[schemas.GroupMemberResponse])
async def get_user(group_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Kiểm tra xem group_id có tồn tại không
    group_query = db.query(models.Group).filter(models.Group.group_id==group_id)
    if not group_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group {group_id} doesn't exist")
    
    # Kiểm tra xem current_user có phải là người có quyền GET user của nhóm với group_id không
    admin_query = db.query(models.Group_Member).filter( models.Group_Member.group_id == group_id, 
                                                  or_(models.Group_Member.role_id == 1, models.Group_Member.role_id == 2), 
                                                  models.Group_Member.user_id == current_user.user_id,
                                                  models.Group_Member.status == "approved" )

    if not admin_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You do not have permission to do this request")
    
    list_users = db.query(models.Group_Member).filter(models.Group_Member.group_id==group_id).all()

    return list_users

@router.get("/", response_model= schemas.GroupMemberResponse)
async def get_user(group_id: int, user_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Kiểm tra xem group_id có tồn tại không
    group_query = db.query(models.Group).filter(models.Group.group_id==group_id)
    if not group_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group {group_id} doesn't exist")

    # Kiểm tra xem current_user có phải là người có quyền GET user của nhóm với group_id không
    admin_query = db.query(models.Group_Member).filter( models.Group_Member.group_id == group_id, 
                                                  or_(models.Group_Member.role_id == 1, models.Group_Member.role_id == 2), 
                                                  models.Group_Member.user_id == current_user.user_id,
                                                  models.Group_Member.status == "approved" )

    if not admin_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You do not have permission to do this request")
    
    # Kiểm tra xem user_id có tồn tại trong group_id không
    user = db.query(models.Group_Member).filter(models.Group_Member.user_id == user_id,
                                                models.Group_Member.group_id == group_id,
                                                models.Group_Member.status == "approved").first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} doesn't exist in group {group_id}")

    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# @router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.username == user.username)
    user_found = user_query.first()

    if user_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"username: {user.username} already exits")
    
    user_query = db.query(models.User).filter(models.User.email == user.email)
    user_found = user_query.first()

    if user_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"email: {user.email} already exits")
    
    utils.validate_password_strength(user.password)

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)

    return new_user  

@router.put("/", response_model=schemas.UserOut)
async def update_user(user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    if user_update.username != current_user.username:
        user_query = db.query(models.User).filter(models.User.username == user_update.username)
        if user_query.first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"username: {user_update.username} already exits")
        
    if user_update.email != current_user.email:
        user_query = db.query(models.User).filter(models.User.email == user_update.email)
        if user_query.first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"email: {user_update.email} already exits")
        
    user = db.query(models.User).filter(models.User.user_id == current_user.user_id).first()

    user.username = user_update.username
    user.password = utils.hash(user_update.password)
    user.email = user_update.email
    user.full_name = user_update.full_name

    db.commit()
    db.refresh(user)
    return user

@router.delete("/")
async def delete_user(user_id: int, group_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Kiểm tra xem current_user có phải là người có quyền DELETE user của nhóm với group_id không
    admin_query = db.query(models.Group_Member).filter( models.Group_Member.group_id == group_id, 
                                                        models.Group_Member.role_id == 1, 
                                                        models.Group_Member.user_id == current_user.user_id,
                                                        models.Group_Member.status == "approved" )
    if not admin_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You do not have permission to do this request")
    
    # Kiểm tra xem trong bảng Group_Member có tồn tại user_id trùng với group_id không
    user_query = db.query(models.Group_Member).filter(models.Group_Member.group_id == group_id,
                                                models.Group_Member.user_id == user_id,
                                                models.Group_Member.status == "approved")
    
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} doesn't exits in group {group_id}")

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
