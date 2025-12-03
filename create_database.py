import pymysql

# 数据库连接配置
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # 请修改为您的MySQL密码
    'charset': 'utf8mb4'
}

# 创建数据库
def create_database():
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()

        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS library_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("数据库 'library_management' 创建成功或已存在")

        # 使用数据库
        cursor.execute("USE library_management")

        cursor.close()
        connection.close()

        print("数据库初始化完成！")

    except Exception as e:
        print(f"数据库创建失败: {e}")

if __name__ == "__main__":
    create_database()