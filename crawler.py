import requests
# 🌟 把你寫好的 Flask 應用程式和資料庫模型匯入進來
from app import app, db, Clothing

url = "https://dummyjson.com/products/category/womens-dresses"

print("🕷️ 爬蟲出動！前往網站抓取資料...")
response = requests.get(url)

if response.status_code == 200:
    clothes_data = response.json()['products']
    print(f"✅ 抓取成功！準備將 {len(clothes_data)} 件洋裝放入資料庫...\n")

    # 🌟 啟動 Flask 應用程式的情境 (這樣才能操作資料庫)
    with app.app_context():
        # 如果資料庫還沒建好，就順便建一下
        db.create_all() 

        for item in clothes_data:
            # 創造一件新衣服的資料物件
            new_clothes = Clothing(
                name=item['title'],
                category="洋裝", # DummyJSON 抓回來都是洋裝
                color="未分類",  # 這個 API 沒給顏色，我們就先填未分類
                image_url=item['images'][0] # 存入圖片網址
            )
            # 把衣服加進暫存區
            db.session.add(new_clothes)
        
        # 🌟 一次把暫存區的所有衣服正式寫進 SQLite！
        db.session.commit()
        print("🎉 太神啦！所有衣服都已經成功收納進你的 SQLite 衣櫥裡了！")
else:
    print(f"❌ 發生錯誤，狀態碼：{response.status_code}")