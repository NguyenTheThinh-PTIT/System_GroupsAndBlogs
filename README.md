Mô tả hệ thống quản lý nhóm và người dùng
# Tổng quan
  * Hệ thống quản lý nhóm và người dùng này cho phép người dùng tạo và quản lý các nhóm với nhiều vai trò khác nhau, đăng bài blog cá nhân hoặc trong nhóm, và kiểm soát nội dung bằng cách yêu cầu phê duyệt blog trước khi xuất bản. Người dùng có thể gửi yêu cầu tham gia nhóm, và sau khi được phê duyệt, họ sẽ được gán vai trò trong nhóm. Hệ thống hỗ trợ việc đánh dấu blog là "pending" để các thành viên có quyền hạn trong nhóm duyệt trước khi chính thức xuất bản.
# Thành phần chính của hệ thống
* Người dùng (Users):
    	* Người dùng có thể đăng ký tài khoản với username và mật khẩu.
    	* Người dùng có thể quản lý thông tin cá nhân và đăng các bài blog cá nhân (có thể chọn chế độ công khai hoặc riêng tư).
* Nhóm (Groups):
    *	Người dùng có thể tạo nhóm và quản lý nhóm, bao gồm mời người khác, duyệt yêu cầu tham gia, và gán vai trò.
    *	Mỗi nhóm có thể có nhiều vai trò khác nhau, chẳng hạn như Admin, Moderator, Member, v.v.
    *	Các thành viên trong nhóm có thể đăng bài blog, sửa, xóa bài viết của mình và xem blog của người khác trong nhóm.
* Vai trò (Roles):
    *	Hệ thống hỗ trợ nhiều vai trò trong mỗi nhóm, mỗi vai trò có các quyền hạn khác nhau.
    *	Vai trò xác định quyền hạn của thành viên trong nhóm như quản lý thành viên, đăng bài, duyệt bài, v.v.
* Pending Blog:
    *	Khi một bài blog được đăng trong nhóm, nó có thể được đánh dấu là "pending" và chờ duyệt.
    *	Các thành viên có quyền hạn (ví dụ: Admin, Moderator) có thể duyệt, từ chối, hoặc yêu cầu chỉnh sửa blog trước khi xuất bản.
# Quy trình hoạt động chi tiết
  ## Đăng ký và đăng nhập
    1.	Người dùng đăng ký tài khoản:
      ###	Người dùng tạo tài khoản với username và mật khẩu, đảm bảo username không trùng lặp.
      ###	Thông tin tài khoản được lưu trữ trong bảng Users.
    2.	Người dùng đăng nhập:
      ###	Người dùng đăng nhập bằng username và mật khẩu, và hệ thống xác thực thông tin để cho phép truy cập.
  ## Quản lý nhóm
    1.	Tạo nhóm mới:
      ###	Người dùng có thể tạo một nhóm mới và trở thành Admin của nhóm đó.
      ###	Thông tin về nhóm được lưu trữ trong bảng Groups.
    2.	Mời người dùng tham gia nhóm:
      ###	Admin có thể mời người dùng khác tham gia nhóm.
      ###	Người dùng được mời có thể chấp nhận hoặc từ chối lời mời.
    3.	Yêu cầu tham gia nhóm:
      ###	Người dùng có thể gửi yêu cầu tham gia vào một nhóm cụ thể.
      ###	Yêu cầu này được lưu trữ và trạng thái chờ phê duyệt trong bảng Group_Members.
    4.	Phê duyệt và gán vai trò:
      ###	Admin hoặc thành viên có quyền hạn có thể phê duyệt yêu cầu tham gia nhóm và gán vai trò cho thành viên mới.
  ## Quản lý blog
    1.	Đăng bài blog cá nhân:
      ###	Người dùng có thể đăng bài blog cá nhân và chọn chế độ công khai hoặc riêng tư.
      ###	Bài blog cá nhân được lưu trong bảng Blogs với group_id là NULL.
    2.	Đăng bài blog trong nhóm:
      ###	Thành viên trong nhóm có thể đăng bài blog mới.
      ###	Bài blog được lưu với trạng thái pending và chờ phê duyệt.
    3.	Duyệt bài blog:
      ###	Thành viên có quyền hạn (Admin, Moderator) được thông báo về các bài blog đang chờ duyệt.
      ###	Họ có thể duyệt để xuất bản, từ chối, hoặc yêu cầu chỉnh sửa bài viết.
    4.	Xuất bản bài blog:
      ###	Khi được duyệt, bài blog chuyển sang trạng thái published và hiển thị cho tất cả thành viên trong nhóm.
  ## Quản lý thành viên trong nhóm
    1.	Xem và quản lý thành viên:
      o	Admin hoặc thành viên có quyền quản lý có thể xem danh sách thành viên trong nhóm, gán hoặc thay đổi vai trò của họ.
    2.	Xóa thành viên khỏi nhóm:
      o	Admin hoặc thành viên có quyền quản lý có thể xóa thành viên khỏi nhóm nếu cần.
  ## Quản lý yêu cầu tham gia
    1.	Duyệt yêu cầu tham gia:
      o	Admin hoặc thành viên có quyền hạn duyệt yêu cầu tham gia của người dùng và gán vai trò phù hợp sau khi phê duyệt.


