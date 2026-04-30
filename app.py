from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 設定 SQLite 資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wardrobe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 建立資料庫模型 (Model) - 衣服
class Clothing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    category = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=True)  
    image_url = db.Column(db.String(300), nullable=True) 

# 建立資料庫與測試資料
with app.app_context():
    db.create_all()
    if not Clothing.query.first():
        sample_clothes = [
            Clothing(name="日系純棉白 T 恤", category="上衣", color="白色"),
            Clothing(name="直筒牛仔長褲", category="褲子", color="藍色"),
            Clothing(name="工裝多口袋背心", category="外套", color="軍綠色"),
            Clothing(name="極簡風黑襯衫", category="上衣", color="黑色"),
            Clothing(name="百搭卡其寬褲", category="褲子", color="卡其色")
        ]
        db.session.add_all(sample_clothes)
        db.session.commit()

# ==========================================
# 這裡開始是 API 路由 (也就是大腦接收指令的神經)
# ==========================================

# 【R】讀取 (Read) - 首頁網頁 (呈現畫面用)
@app.route('/')
def home():
    # 從資料庫撈出所有衣服
    clothes = Clothing.query.all()
    # 把衣服資料傳給 show.html
    return render_template('show.html', items=clothes)

# 【C】新增 (Create) - 接收網頁表單傳來的資料並存入資料庫
@app.route('/add', methods=['POST'])
def add_clothing():
    new_name = request.form.get('name')
    new_category = request.form.get('category')
    new_color = request.form.get('color')
    new_image_url = request.form.get('image_url')

    new_item = Clothing(
        name=new_name, 
        category=new_category, 
        color=new_color, 
        image_url=new_image_url
    )
    
    db.session.add(new_item)
    db.session.commit()
    
    return redirect(url_for('home'))

# 【D】刪除 (Delete) - 根據衣服的 ID 把它從資料庫刪掉
@app.route('/delete/<int:id>', methods=['POST'])
def delete_clothing(id):
    item_to_delete = Clothing.query.get_or_404(id)
    
    db.session.delete(item_to_delete)
    db.session.commit()
    
    return redirect(url_for('home'))

# ==========================================
# 啟動馬達 (超級重要，這決定伺服器會不會跑起來)
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)