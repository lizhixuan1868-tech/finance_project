import pymysql

# 替换为你腾讯云控制台的真实信息
config = {
    'host': 'gz-cdb-8bco4w6f.sql.tencentcdb.com',  # 例如：cdb-xxxxx.cdb.myqcloud.com
    'port': 24347,
    'user': 'root',  # 通常是 root
    'password': 'lzx13695250408',  # 购买时设置的密码
     'database': 'use01',  # 你刚创建的数据库名
    # 'charset': 'utf8mb4'
}

try:
    conn = pymysql.connect(**config)
    print("✅ 连接成功！")

    # 可选：测试写入一条数据
    with conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INT AUTO_INCREMENT PRIMARY KEY, msg VARCHAR(100))")
        cursor.execute("INSERT INTO test_table (msg) VALUES ('Hello from local!')")
        conn.commit()
        print("✅ 数据写入成功！")

except Exception as e:
    print(f"❌ 连接失败：{e}")
finally:
    if 'conn' in locals():
        conn.close()