from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, utils, models, oauth2
from ..database import get_db
from sqlalchemy import or_

router = APIRouter(
    # prefix='/groups',
    tags=['blogs']
)

@router.get("/blogs", response_model=List[schemas.BlogResponse])
async def get_blogs(group_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Kiểm tra group_id có tồn tại không
    group_query = db.query(models.Group).filter(models.Group.group_id == group_id)
    if not group_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group {group_id} doesn't exits")
    
    # Kiêm tra xem current_user có thuộc group_id không
    member_query = db.query(models.Group_Member).filter(models.Group_Member.group_id == group_id,
                                                  models.Group_Member.user_id == current_user.user_id,
                                                  models.Group_Member.status == "approved")
    if not member_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not in group {group_id}")
    
    list_blogs = db.query(models.Blog).all()
    return list_blogs

@router.get("/blogs/{blog_id}/", response_model=schemas.BlogResponse)
async def get_blog(group_id: int, blog_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Kiểm tra group_id có tồn tại không
    group_query = db.query(models.Group).filter(models.Group.group_id == group_id)
    if not group_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group {group_id} doesn't exits")
    
    # Kiêm tra xem current_user có thuộc group_id không
    member_query = db.query(models.Group_Member).filter(models.Group_Member.group_id == group_id,
                                                  models.Group_Member.user_id == current_user.user_id,
                                                  models.Group_Member.status == "approved")
    if not member_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not in group {group_id}")
    
    # Kiểm tra xem blog_id có trong group_id không
    blog_query = db.query(models.Blog).filter(models.Blog.group_id == group_id,
                                              models.Blog.blog_id == blog_id)
    blog = blog_query.first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {blog_id} doesn't belongs to group {group_id}")

    return blog

@router.post("/blogs/{group_id}/", response_model=schemas.BlogResponse)
def create_group_blog(group_id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Kiểm tra sự tồn tại của group_id
    group_query = db.query(models.Group).filter(models.Group.group_id==group_id)
    if not group_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"group id: {group_id} doesn't exist")
    
    # Kiểm tra nếu người dùng là thành viên của nhóm
    member = db.query(models.Group_Member).filter(models.Group_Member.group_id==group_id, 
                                                  models.Group_Member.user_id==current_user.user_id, 
                                                  models.Group_Member.status=="approved").first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not a member of this group")

    # Tạo blog với trạng thái "pending"
    new_blog = models.Blog(user_id=current_user.user_id, group_id=group_id, title=blog.title, content=blog.content, status="pending", is_public = blog.is_public)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog

@router.post("/blogs/{group_id}/approve/{blog_id}/")
def approve_blog(group_id: int, blog_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Kiểm tra sự tồn tại của group_id
    group_query = db.query(models.Group).filter(models.Group.group_id==group_id)
    if not group_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"group id: {group_id} doesn't exist")
    
    # Kiểm tra sự tồn tại của blog_id trong group_id
    blog_query = db.query(models.Blog).filter(models.Blog.blog_id == blog_id, models.Blog.group_id==group_id)
    if not blog_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog id: {blog_id} doesn't belong group id: {group_id}")

    # Kiểm tra quyền duyệt blog của người dùng
    admin = db.query(models.Group_Member).filter( models.Group_Member.group_id == group_id, 
                                                  or_(models.Group_Member.role_id == 1, models.Group_Member.role_id == 2), 
                                                  models.Group_Member.user_id == current_user.user_id,
                                                  models.Group_Member.status == "approved" ).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to approve blog")
    
    # Duyệt blog
    blog = db.query(models.Blog).filter(models.Blog.blog_id==blog_id, models.Blog.group_id==group_id, models.Blog.status=="pending").first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog already approved")
    
    blog.status = "approved"
    db.commit()
    
    return {"message": "Blog approved"}


@router.post("/blogs/{blog_id}/reactions/{group_id}", response_model=schemas.ReactionResponse)
def react_to_blog(blog_id: int, group_id: int,reaction: schemas.ReactionCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Kiểm tra current_user thuộc group này không
    user_query = db.query(models.Group_Member).filter(models.Group_Member.group_id == group_id,
                                                      models.Group_Member.user_id == current_user.user_id,
                                                      models.Group_Member.status == "approved")
    
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not in group {group_id}")
    
    # Kiểm tra sự tồn tại của blog_id trong group_id
    blog_query = db.query(models.Blog).filter(models.Blog.blog_id == blog_id, models.Blog.group_id==group_id)
    if not blog_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog id: {blog_id} doesn't belong group id: {group_id}")
    
    # Kiểm tra sự tồn tại của react
    react_query = db.query(models.Reaction).filter(models.Reaction.blog_id == blog_id,
                                                   models.Reaction.user_id == current_user.user_id,
                                                   models.Reaction.reaction_type == reaction.reaction_type)
    
    if react_query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You already reacted this post with reaction type {reaction.reaction_type}")
    
    # Nếu đã tồn tại react cũ và có react mới từ current user tới bài viết thì thay đổi theo cái mới nhất
    react_query = db.query(models.Reaction).filter(models.Reaction.blog_id == blog_id,
                                                   models.Reaction.user_id == current_user.user_id,
                                                   models.Reaction.reaction_type != reaction.reaction_type)
    react_post = react_query.first()
    if react_post:
        react_post.reaction_type = reaction.reaction_type
        db.commit()
        db.refresh(react_post)
        return react_post
    else:
        # Tạo phản ứng mới
        new_reaction = models.Reaction(user_id=current_user.user_id, blog_id=blog_id, reaction_type=reaction.reaction_type)
        db.add(new_reaction)
        db.commit()
        db.refresh(new_reaction)
        
        return new_reaction


@router.post("/blogs/{blog_id}/comment1s/{group_id}", response_model=schemas.CommentResponse)
def comment_on_blog(blog_id: int,group_id: int, comment: schemas.CommentOfPostCreate, db: Session = Depends(get_db), current_user= Depends(oauth2.get_current_user)):
    # Kiểm tra current_user thuộc group này không
    user_query = db.query(models.Group_Member).filter(models.Group_Member.group_id == group_id,
                                                      models.Group_Member.user_id == current_user.user_id,
                                                      models.Group_Member.status == "approved")
    
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not in group {group_id}")

    # Kiểm tra sự tồn tại của blog_id trong group_id
    blog_query = db.query(models.Blog).filter(models.Blog.blog_id == blog_id, models.Blog.group_id==group_id)
    if not blog_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog id: {blog_id} doesn't belong group id: {group_id}")
    
    # Tạo bình luận mới
    new_comment = models.Comment(user_id=current_user.user_id, blog_id=blog_id, content=comment.content)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment

@router.post("/blogs/{blog_id}/comment2s/{group_id}", response_model=schemas.CommentResponse)
def comment_on_childComment(blog_id: int,group_id: int,comment: schemas.CommentOfMemberCreate, db: Session = Depends(get_db), current_user= Depends(oauth2.get_current_user)):
    # Kiểm tra current_user thuộc group này không
    user_query = db.query(models.Group_Member).filter(models.Group_Member.group_id == group_id,
                                                      models.Group_Member.user_id == current_user.user_id,
                                                      models.Group_Member.status == "approved")
    
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not in group {group_id}")

    # Kiểm tra sự tồn tại của blog_id trong group_id
    blog_query = db.query(models.Blog).filter(models.Blog.blog_id == blog_id, models.Blog.group_id==group_id)
    if not blog_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog id: {blog_id} doesn't belong group id: {group_id}")
    
    # Kiểm tra sự tồn tại của parent_comment_id
    comment_query = db.query(models.Comment).filter(models.Comment.comment_id == comment.parent_comment_id)
    if not comment_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {comment.parent_comment_id} doesn't exist")

    # Tạo bình luận mới
    new_comment = models.Comment(user_id=current_user.user_id, blog_id=blog_id, content=comment.content, parent_comment_id = comment.parent_comment_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment

# @router.put