# 数据库配置不一致问题 - SQLite vs MySQL 混用

## 📝 Issue 描述

项目中存在数据库配置不一致的问题：README.md文档声明使用MySQL，但实际代码配置为SQLite（library.db），这会导致新用户在配置和运行项目时产生困惑。

## 🔍 问题详情

### 1. 文档与实际配置不符

**README.md 声明：**
- 技术架构：**数据库**: MySQL
- 安装指南中提到了MySQL配置步骤

**实际代码配置 (config.py)：**
```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///library.db'
```

### 2. 数据库文件位置
实际生成的数据库文件位于：`instance/library.db`

### 3. 多种数据库初始化脚本存在
项目中存在多个数据库相关的脚本，分别针对不同的数据库：
- `init_sqlite_database.py` - SQLite版本
- `setup_database.py` - SQLite版本
- `rebuild_db.py` - MySQL版本
- `clean_database.py` - MySQL版本
- `create_database.py` - MySQL版本

### 4. 环境变量处理不完善
虽然代码中使用了环境变量 `DATABASE_URL`，但：
- 没有明确的环境变量配置说明
- 默认值直接使用SQLite，可能导致用户忽略MySQL配置

## 💡 建议解决方案

### 方案一：统一使用SQLite（推荐）
1. 更新README.md，说明项目默认使用SQLite
2. 简化安装和配置步骤
3. 删除或标记MySQL相关的脚本
4. 添加SQLite备份和恢复指南

### 方案二：统一使用MySQL
1. 修改config.py，默认使用MySQL
2. 提供完整的MySQL安装和配置指南
3. 删除SQLite相关脚本
4. 添加数据库迁移工具

### 方案三：支持两种数据库（混合方案）
1. 提供清晰的数据库选择机制
2. 创建统一的数据库初始化脚本
3. 为每种数据库提供详细的配置指南
4. 添加自动检测和配置工具

## 🎯 影响范围

- **新用户**：安装配置困难，环境搭建失败率高
- **开发者**：代码维护困难，测试环境不一致
- **部署**：生产环境配置混乱

## 📋 具体修改建议

1. **统一数据库声明**
   - 更新README.md，明确说明实际使用的数据库
   - 在安装指南中提供清晰的数据库配置步骤

2. **优化项目结构**
   - 保留当前使用的数据库配置文件
   - 删除或归档不需要的数据库脚本
   - 添加数据库类型检测和提示

3. **改进配置管理**
   - 添加环境变量示例文件（.env.example）
   - 提供数据库配置验证功能
   - 添加配置错误提示

4. **完善文档**
   - 创建详细的数据库配置文档
   - 提供常见问题解答
   - 添加数据库备份和恢复指南

## 🏷️ 标签

bug, enhancement, documentation, configuration, database

## 🔗 相关文件

- `config.py` - 数据库配置文件
- `README.md` - 项目文档
- `init_sqlite_database.py` - SQLite初始化脚本
- `rebuild_db.py` - MySQL重建脚本
- `setup_database.py` - SQLite设置脚本
- `.gitignore` - 包含数据库文件忽略规则