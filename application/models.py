from .database import db
#by default value : nullable=True
class Category(db.Model):
    __tablename__ = 'category'
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(120), nullable=False, unique=True)

class Product(db.Model):
    __tablename__ = 'product'
    p_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    c_id = db.Column(db.Integer)
    product_name = db.Column(db.String(120), nullable=False, unique=True)

class cat_prod(db.Model):
    __tablename__ = 'cat_prod'
    c_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(120))
    product_name = db.Column(db.String(120))

class Stock(db.Model):
    __tablename__ = 'stock'
    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_id = db.Column(db.Integer)
    unit = db.Column(db.Integer, nullable=False)
    rate_per_unit = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class prod_stock(db.Model):
    __tablename__ = 'prod_stock'
    p_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer)
    product_name = db.Column(db.String(120))
    unit = db.Column(db.Integer)
    rate_per_unit = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

class combined_view(db.Model):
    __tablename__ = 'combined_view'
    c_id = db.Column(db.Integer)
    p_id = db.Column(db.Integer)
    s_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(120))
    product_name = db.Column(db.String(120))
    unit = db.Column(db.Integer)
    rate_per_unit = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

class User(db.Model):
    __bind_key__ = 'user_db'
    __tablename__ = 'user_details'
    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(120), nullable=False, unique=True)
    u_password = db.Column(db.String(120), nullable=False)


class Cart(db.Model):
    __bind_key__ = 'user_db'
    __tablename__ = 'cart'
    ct_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(120), nullable=False)
    category_name = db.Column(db.String(120), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    unit = db.Column(db.Integer, nullable=False)
    rate_per_unit = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_total = db.Column(db.Integer)




# class UserModel(db.Model):
#     __tablename__ = 'user'
#     __bind_key__ = 'user_db'
#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(100), nullable=False)