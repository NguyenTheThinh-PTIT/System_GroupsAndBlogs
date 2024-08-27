from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, utils, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/groups',
    tags=['groups']
)

# @router.post("/groups/", response_model=GroupResponse)
@router.post("/", response_model=schemas.GroupResponse)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Tạo nhóm mới
    query_group = db.query(models.Group).filter(models.Group.group_name == group.group_name)
    if query_group.first():
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="Group name already existed!")
    new_group = models.Group(**group.dict())
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    
    # Gán quyền Admin cho người tạo nhóm
    admin_role = db.query(models.Role).filter(models.Role.role_name == "admin").first()
    if not admin_role:
        raise HTTPException(status_code=404, detail="Admin role not found")
    
    new_group_member = models.Group_Member(group_id=new_group.group_id, user_id=current_user.user_id, role_id=admin_role.role_id, status="approved")
    db.add(new_group_member)
    db.commit()
    
    return new_group

@router.post("/{group_id}/join")
def request_to_join_group(group_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Kiểm tra nếu người dùng đã là thành viên của nhóm
    group = db.query(models.Group).filter(models.Group.group_id == group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Group with id {group_id} doesn't exits")

    member = db.query(models.Group_Member).filter(models.Group_Member.group_id == int(group_id), 
                                                  models.Group_Member.status == "pending", 
                                                  models.Group_Member.user_id==current_user.user_id ).first()
    if member:
        raise HTTPException(status_code=400, detail="Your request is pending approval")
    
    member = db.query(models.Group_Member).filter(models.Group_Member.group_id == int(group_id), 
                                                  models.Group_Member.status == "approved", 
                                                  models.Group_Member.user_id==current_user.user_id ).first()
    
    if member:
        raise HTTPException(status_code=400, detail="You are already a member of this group")

    # Tạo yêu cầu tham gia nhóm
    pending_request = models.Group_Member(group_id=int(group_id), user_id=current_user.user_id, status="pending")
    db.add(pending_request)
    db.commit()
    
    return {"message": "Request to join group is pending approval"}

@router.post("/{group_id}/approve/{user_id}")
def approve_member(group_id: int, user_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Kiểm tra nếu current_user là admin của nhóm
    member = db.query(models.Group_Member).filter(models.Group_Member.group_id == group_id, models.Group_Member.role_id == 1, models.Group_Member.status == "approved").first()
    if not member:
        raise HTTPException(status_code=403, detail="You do not have permission to approve members")
    
    # Duyệt yêu cầu
    pending_member = db.query(models.Group_Member).filter(models.Group_Member.group_id == group_id, models.Group_Member.user_id == user_id, models.Group_Member.status == "pending").first()
    if not pending_member:
        raise HTTPException(status_code=404, detail="Pending request not found")
    
    pending_member.status = "approved"
    db.commit()
    
    return {"message": "Member approved"}


