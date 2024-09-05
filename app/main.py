from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db, engine
from . import models
from .router import user, auth, group, blog

# models.Base.metadata.create_all(bind = engine)
app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(group.router)
app.include_router(blog.router)
# Khi nào truyền path param và query param
# Check tồn tại của user_id và group_id khi nhận từ 2 cái trên

# search update và create
# kiểm tra người dùng đủ quyền trc khi get
# chấp nhận vào nhóm gộp chung
 