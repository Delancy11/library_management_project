# 图书管理系统

一个功能完整的图书管理系统，基于 Flask + MySQL 构建，支持用户注册登录、图书借阅管理、权限控制等功能。

## 📋 功能特点

### 🔐 用户认证
- ✅ 完整的用户注册和登录功能
- ✅ 管理员与普通用户权限分离
- ✅ 密码加密存储
- ✅ 会话管理和记住登录

### 👥 用户管理
- ✅ 用户注册、资料管理
- ✅ 管理员可查看和管理所有用户
- ✅ 用户数据隔离

### 📚 图书管理
- ✅ 图书的增删改查操作
- ✅ 图书分类管理
- ✅ 库存管理
- ✅ 图书搜索和筛选

### 🏷️ 分类管理
- ✅ 创建和管理图书分类
- ✅ 分类统计
- ✅ 空分类删除保护

### 📖 借阅管理
- ✅ 图书借阅和归还
- ✅ 借阅记录管理
- ✅ 逾期提醒
- ✅ 借阅历史查询

### 🛡️ 权限控制
- ✅ 管理员权限：管理用户、图书、分类、借阅记录
- ✅ 用户权限：浏览图书、借阅归还、管理个人资料
- ✅ 数据隔离：用户只能访问自己的数据

## 🏗️ 技术架构

### 后端技术
- **框架**: Flask 2.3.3
- **数据库**: MySQL
- **ORM**: SQLAlchemy
- **认证**: Flask-Login
- **表单**: WTForms
- **密码加密**: Bcrypt

### 前端技术
- **基础**: HTML5 + CSS3 + JavaScript
- **UI框架**: Bootstrap 5
- **图标**: Bootstrap Icons
- **模板引擎**: Jinja2

### 数据库设计
系统使用5张核心数据表：

1. **users** - 用户表（普通用户）
2. **admins** - 管理员表
3. **books** - 图书表
4. **categories** - 分类表
5. **borrow_records** - 借阅记录表

## 📦 安装部署

### 环境要求
- Python 3.7+
- MySQL 5.7+
- pip

### 1. 克隆项目
```bash
git clone <repository-url>
cd library-management-system
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置数据库
- 启动 MySQL 服务
- 创建数据库（或使用脚本自动创建）
- 修改 `config.py` 中的数据库连接信息

### 4. 初始化数据库
```bash
python create_database.py
```

### 5. 启动应用
```bash
python run.py
```

### 6. 访问系统
- 访问地址: http://localhost:5000
- 默认管理员账户: admin / admin123

## 📁 项目结构

```
library-management-system/
├── app.py                    # 主应用文件
├── models.py                 # 数据库模型
├── config.py                 # 配置文件
├── create_database.py        # 数据库创建脚本
├── run.py                    # 启动脚本
├── requirements.txt          # 依赖包列表
├── README.md                 # 项目说明
├── templates/                # HTML模板
│   ├── base.html            # 基础模板
│   ├── index.html           # 首页
│   ├── login.html           # 登录页
│   ├── register.html        # 注册页
│   ├── admin/               # 管理员页面
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   ├── books.html
│   │   ├── add_book.html
│   │   ├── edit_book.html
│   │   ├── categories.html
│   │   ├── add_category.html
│   │   ├── edit_category.html
│   │   └── borrow_records.html
│   └── user/                # 用户页面
│       ├── dashboard.html
│       ├── browse_books.html
│       ├── profile.html
│       └── borrow_history.html
└── static/                   # 静态资源
    ├── css/
    │   └── style.css        # 自定义样式
    └── js/
        └── script.js        # JavaScript脚本
```

## 🚀 使用指南

### 管理员功能
1. **仪表板**: 查看系统统计信息
2. **用户管理**: 查看和管理所有用户
3. **图书管理**: 添加、编辑、删除图书
4. **分类管理**: 创建和管理图书分类
5. **借阅记录**: 查看和管理所有借阅记录

### 用户功能
1. **用户中心**: 查看个人信息和借阅统计
2. **图书浏览**: 搜索和浏览图书
3. **图书借阅**: 借阅和归还图书
4. **借阅历史**: 查看个人借阅记录
5. **个人资料**: 管理个人信息

### 默认账户
- **管理员**: admin / admin123
- **普通用户**: 需要注册创建

## 🔧 配置说明

### 数据库配置
在 `config.py` 中修改数据库连接信息：
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/database_name'
```

### 系统配置
```python
SECRET_KEY = 'your-secret-key'  # Flask密钥
ADMIN_DEFAULT_PASSWORD = 'admin123'  # 默认管理员密码
BOOKS_PER_PAGE = 10  # 图书每页显示数量
RECORDS_PER_PAGE = 10  # 记录每页显示数量
```

## 🎯 核心功能演示

### 1. 用户注册
- 填写用户名、邮箱、密码等信息
- 系统自动验证用户名和邮箱唯一性

### 2. 图书借阅
- 用户浏览图书库
- 选择图书进行借阅
- 系统自动记录借阅信息（30天归还期）

### 3. 图书归还
- 用户在借阅历史中归还图书
- 系统自动更新库存和借阅状态

### 4. 管理员操作
- 添加新图书到系统
- 管理用户账户
- 查看借阅统计和逾期记录

## 🔒 安全特性

- 密码使用 Bcrypt 加密存储
- 用户会话管理
- 权限验证和访问控制
- CSRF 保护
- SQL 注入防护

## 📊 系统特性

### 响应式设计
- 支持桌面和移动设备
- Bootstrap 5 响应式布局

### 用户体验
- 直观的用户界面
- 实时搜索和筛选
- 分页浏览
- 操作确认对话框

### 性能优化
- 数据库查询优化
- 静态资源缓存
- 分页减少数据加载

## 🔄 数据备份

建议定期备份数据库：
```sql
mysqldump -u username -p database_name > backup.sql
```

## 🐛 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查 MySQL 服务是否启动
   - 确认数据库配置信息正确

2. **权限错误**
   - 确认数据库用户权限
   - 检查防火墙设置

3. **依赖包问题**
   - 重新安装依赖：`pip install -r requirements.txt`

4. **端口冲突**
   - 修改启动脚本中的端口号

## 📈 扩展功能

系统预留了扩展接口，可以轻松添加：
- 邮件通知功能
- 图书推荐系统
- 借阅预约功能
- 数据统计报表
- API 接口

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目。

## 📄 许可证

本项目采用 MIT 许可证。

---

**开发团队**: [您的团队名称]
**项目版本**: 1.0.0
**最后更新**: 2024年12月