# Group Management and Blogging System

## Overview
This system allows users to create and manage groups, post blogs within those groups, and interact with the content through reactions and comments. The system includes role-based access control within groups and a blog approval workflow, ensuring content quality and relevance.

## Features

### User Management
- **User Registration & Login**: Users can register with a unique username and password, and log in to the system.
- **Profile Management**: Users can manage their personal information and choose to publish personal blogs that can be public or private.

### Group Management
- **Group Creation**: Any user can create a group and become the initial Admin of that group.
- **Role-Based Access Control**: Users within a group can have multiple roles (e.g., Admin, Moderator, Member), each with different permissions.
- **Member Management**: Admins can invite users to join the group, approve or reject join requests, and assign roles.
- **Multiple Admins**: Groups can have multiple Admins who share the responsibility of managing the group.

### Blogging System
- **Personal Blogs**: Users can post personal blogs that are either public or private.
- **Group Blogs**: Users can post blogs within a group, which can be set to require approval before being published.
- **Pending Blogs**: Blogs posted in a group are marked as "pending" until approved by members with sufficient permissions.

### Interaction with Blogs
- **Reactions**: Users can react to published blogs with various emotions like "like," "love," "wow," etc.
- **Comments**: Users can comment on blogs and respond to other comments, creating nested discussions.

## Database Design

### Tables Overview

#### Users
Stores user information.

| Column      | Type        | Description                      |
|-------------|-------------|----------------------------------|
| user_id     | SERIAL      | Primary Key                      |
| username    | VARCHAR(50) | Unique username                  |
| password    | VARCHAR(255)| User's password (hashed)         |
| email       | VARCHAR(255)| User's email address             |
| full_name   | VARCHAR(255)| User's full name                 |
| created_at  | TIMESTAMP   | Account creation timestamp       |
| updated_at  | TIMESTAMP   | Account update timestamp         |

#### Groups
Stores information about user-created groups.

| Column     | Type        | Description                        |
|------------|-------------|------------------------------------|
| group_id   | SERIAL      | Primary Key                        |
| group_name | VARCHAR(255)| Name of the group                  |
| created_at | TIMESTAMP   | Group creation timestamp           |
| updated_at | TIMESTAMP   | Group update timestamp             |

#### Roles
Stores roles within groups.

| Column    | Type        | Description                        |
|-----------|-------------|------------------------------------|
| role_id   | SERIAL      | Primary Key                        |
| role_name | VARCHAR(50) | Name of the role (e.g., Admin)     |
| created_at| TIMESTAMP   | Role creation timestamp            |
| updated_at| TIMESTAMP   | Role update timestamp              |

#### Group_Members
Stores user membership and roles in groups.

| Column          | Type        | Description                        |
|-----------------|-------------|------------------------------------|
| group_member_id | SERIAL      | Primary Key                        |
| group_id        | INTEGER     | Foreign Key to Groups              |
| user_id         | INTEGER     | Foreign Key to Users               |
| role_id         | INTEGER     | Foreign Key to Roles               |
| created_at      | TIMESTAMP   | Membership creation timestamp      |
| updated_at      | TIMESTAMP   | Membership update timestamp        |

#### Blogs
Stores blog posts.

| Column      | Type        | Description                                  |
|-------------|-------------|----------------------------------------------|
| blog_id     | SERIAL      | Primary Key                                  |
| user_id     | INTEGER     | Foreign Key to Users                         |
| group_id    | INTEGER     | Foreign Key to Groups (NULL for personal blogs)|
| title       | VARCHAR(255)| Title of the blog                            |
| content     | TEXT        | Content of the blog                          |
| is_public   | BOOLEAN     | Indicates if a personal blog is public       |
| status      | VARCHAR(20) | Blog status ('pending', 'published', 'rejected')|
| created_at  | TIMESTAMP   | Blog creation timestamp                      |
| updated_at  | TIMESTAMP   | Blog update timestamp                        |

#### Reactions
Stores user reactions to blogs.

| Column      | Type        | Description                                  |
|-------------|-------------|----------------------------------------------|
| reaction_id | SERIAL      | Primary Key                                  |
| user_id     | INTEGER     | Foreign Key to Users                         |
| blog_id     | INTEGER     | Foreign Key to Blogs                         |
| reaction_type| VARCHAR(20)| Type of reaction (e.g., 'like', 'love')      |
| created_at  | TIMESTAMP   | Reaction timestamp                           |

#### Comments
Stores user comments on blogs.

| Column           | Type        | Description                                  |
|------------------|-------------|----------------------------------------------|
| comment_id       | SERIAL      | Primary Key                                  |
| blog_id          | INTEGER     | Foreign Key to Blogs                         |
| user_id          | INTEGER     | Foreign Key to Users                         |
| parent_comment_id| INTEGER     | Foreign Key to Comments (NULL for root comments)|
| content          | TEXT        | Content of the comment                       |
| created_at       | TIMESTAMP   | Comment creation timestamp                   |
| updated_at       | TIMESTAMP   | Comment update timestamp                     |

## System Workflow

### User Actions
1. **Registration & Login**: Users register with unique usernames and passwords, then log in.
2. **Profile Management**: Users can update their profiles and manage their personal blogs.

### Group Management
1. **Create Group**: A user creates a group and becomes its initial Admin.
2. **Invite Users**: Admins invite users to join the group.
3. **Join Requests**: Users request to join groups, and Admins approve or reject them.
4. **Assign Roles**: Admins assign roles to group members.

### Blog Posting & Approval
1. **Post Blog**: Group members can post blogs within the group.
2. **Pending Status**: The blog is marked as "pending" and awaits approval.
3. **Approval Process**: Members with sufficient permissions (e.g., Admins) can approve, reject, or request edits.
4. **Publication**: Once approved, the blog is published and visible to group members.

### Interacting with Blogs
1. **Reactions**: Users react to blogs with emotions like "like," "love," etc.
2. **Comments**: Users can comment on blogs and reply to other comments, creating nested discussions.

## Security and Permissions
- **Role-Based Access Control**: Roles within groups define what actions users can take (e.g., manage members, approve blogs).
- **Content Moderation**: Blogs are reviewed by authorized members before being published.
- **Privacy Controls**: Users control the visibility of their personal blogs (public or private).

## Conclusion
This system provides a robust platform for managing groups and content, with flexible role-based access control, content approval workflows, and enhanced interaction features through reactions and comments.
