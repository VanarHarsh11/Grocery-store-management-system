from flask import Flask, request, redirect, url_for, session, flash
from flask import render_template
from flask import current_app as app
from .models import *

app.secret_key = 'your_secret_key'
cmanager_user_name = 'jordan'
cmanager_password = '2003'

@app.route("/", methods=["GET","POST"])
def login_type():
    return render_template("login_type.html")

@app.route("/<type>-login", methods=["GET","POST"])
def login(type):
    if type=="manager":
        if request.method=="GET":
            return render_template("manager_login.html")
        elif request.method=="POST":
            user_name = request.form["manager_user_name"]
            password = request.form["manager_password"]
            session['user_name']=user_name
            if user_name==cmanager_user_name and password==cmanager_password:
                return redirect(url_for('manager_dashboard'))
            else:
                return render_template("manager_login.html",error='Invalid credentials')
        else:
            return render_template("error.html")
    elif type=="user":
        if request.method == 'GET':
            return render_template("user_login.html")
        elif request.method == 'POST':


            users = db.session.query(User).all()
    
            password_by_user={}
            for user in users:
                uname = user.u_name
                passwords = db.session.query(User.u_password).filter_by(u_id=user.u_id).all()
                pass_list = [pwd.u_password for pwd in passwords]
                password_by_user[uname] = pass_list

            
            
            username_got = request.form['user_user_name']
            password_got = request.form['user_password']
            
            
            if username_got in password_by_user:
                if password_got==password_by_user[username_got][0]:
                    return redirect(url_for('user_dashboard', username = username_got))
                else:
                    return render_template('wrong.html')
            else:
                new_user = User(u_name = username_got,u_password=password_got)
                db.session.add(new_user)
                db.session.commit()
                # return redirect(url_for('login', type='user'))
                return render_template('success.html')
            
                


        # return render_template("user_login.html")

@app.route("/manager-dashboard", methods=["GET","POST"])
def manager_dashboard():
    categories = db.session.query(Category).all()

    products_by_category = {}
    for category in categories:
        category_name = category.category_name
        products = db.session.query(Product.product_name).filter_by(c_id=category.c_id).all()
        products_list = [product.product_name for product in products]
        products_by_category[category_name] = products_list

    cat_table = Category.query.all()
    cat_names = [x for x in products_by_category]
    prod_table = Product.query.all()
    

    if 'user_name' in session:
        return render_template("manager_dashboard.html", manager_user_name=cmanager_user_name, category=cat_names, product_dict=products_by_category, cat_full=cat_table, prod_full=prod_table)
            
    else:
        return redirect(url_for('login',type='manager'))
    
@app.route('/logout')
def logout():
    session.pop('user_name',None)
    return redirect(url_for('login_type'))

@app.route('/add-category', methods=["GET","POST"])
def add_category():
    if request.method=='POST':
        category_name = request.form['category_name']
        new_category = Category(category_name=category_name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('manager_dashboard'))
    
@app.route('/edit-category', methods=["GET","POST"])
def edit_category():
    cat_name = request.args.get('category_name')
    cat_id = request.args.get('category_id')
    
    if request.method=='GET':
        return render_template('edit_category.html',oldcat_name=cat_name)
    elif request.method=='POST':
        newname = request.form['newcat_name']
        # newcategory_name = request.form['newcat_name']
        category = Category.query.get_or_404(cat_id)
        category.category_name = newname
        db.session.commit()
        return redirect(url_for('manager_dashboard'))
    
@app.route('/delete-category', methods=['GET','POST'])
def delete_category():
    cat_name = request.args.get('category_name')
    cat_id = request.args.get('category_id')
    if request.method=='GET':
        return render_template('delete_category.html',cat_name = cat_name )
    elif request.method=='POST':
        choice = request.form['choice']
        if choice == 'yes':
            category = Category.query.get(cat_id)
            db.session.delete(category)
            db.session.commit()
            return redirect(url_for('manager_dashboard'))
        else:
            return redirect(url_for('manager_dashboard'))
        
    
        

    
@app.route('/add-product', methods=["GET",'POST'])
def add_product(): 
    cat_name = request.args.get('category_name')
    if request.method=='GET':
        return render_template('add_product.html',category_name=cat_name)
        
    elif request.method=='POST':
        prdct_name = request.form['product_name']
        unit = request.form['unit']
        rate_per_unit = request.form['rate_per_unit']
        quantity = request.form['quantity']
        

        category = Category.query.filter_by(category_name = cat_name).first()

        new_product = Product(product_name=prdct_name, c_id=category.c_id)
        db.session.add(new_product)
        db.session.commit()

        product = Product.query.filter_by(product_name = prdct_name).first()
        new_stock = Stock(p_id = product.p_id, unit=unit, rate_per_unit=rate_per_unit, quantity=quantity)
        db.session.add(new_stock)
        db.session.commit()
        return redirect(url_for('manager_dashboard'))
    
@app.route('/edit-product', methods=['GET','POST'])
def edit_product():
    product_name = request.args.get('prdct_name')
    product_id = request.args.get('prdct_id')
    stock_table = Stock.query.filter_by(p_id = product_id).first()
    rate = stock_table.rate_per_unit
    quantity = stock_table.quantity
    if request.method=='GET':
        return render_template('edit_product.html',oldprdct_name=product_name,rate=rate, quantity=quantity)
    elif request.method=='POST':
        newname = request.form['newname']
        newrate = int(request.form['newrate'])
        new_quantity = int(request.form['new_quantity'])
        product = Product.query.get_or_404(product_id)
        stock = Stock.query.get_or_404(stock_table.s_id)
        product.product_name = newname
        stock.rate_per_unit = newrate
        stock.quantity += new_quantity

        db.session.commit()
        return redirect(url_for('manager_dashboard'))
    
@app.route('/delete-product', methods=['GET','POST'])
def delete_product():
    product_name = request.args.get('prdct_name')
    product_id = request.args.get('prdct_id')
    if request.method=='GET':
        return render_template('delete_product.html', product_name=product_name)
    elif request.method=='POST':
        choice = request.form['choice']
        if choice == 'yes':
            product = Product.query.get(product_id)
            db.session.delete(product)
            db.session.commit()
            return redirect(url_for('manager_dashboard'))
        else:
            return redirect(url_for('manager_dashboard'))



@app.route('/user-dashboard', methods=['GET','POST'])
def user_dashboard():

    username= request.args.get('username')
    categories = db.session.query(Category).all()

    products_by_category = {}
    for category in categories:
        category_name = category.category_name
        products = db.session.query(Product.product_name).filter_by(c_id=category.c_id).all()
        products_list = [product.product_name for product in products]
        products_by_category[category_name] = products_list

    cat_table = Category.query.all()
    cat_names = [x for x in products_by_category]
    
    stock = combined_view.query.all()

    return render_template('user_dashboard1.html',user_name = username, category=cat_names,product_dict=products_by_category,stock=stock )

@app.route('/buy-product', methods=['GET','POST'])
def buy_product():
    category_name = request.args.get('category_name')
    product_name = request.args.get('product_name')
    user_name = request.args.get('username')
    data = combined_view.query.filter_by(product_name = product_name).first()
    unit = data.unit
    quantity = data.quantity
    rate = data.rate_per_unit
    title = 'Buying product'
    function = 'Buy'
    what_done = 'Your order is placed'
    print(user_name)
    if request.method=='GET':
        return render_template('buy_product.html',
                                user_name=user_name, product_name=product_name, category_name=category_name,
                                unit=unit, quantity=quantity, rate=rate, title=title, function=function)
    elif request.method=='POST':
        bought_q = int(request.form['quantity_given'])
        product_table = Product.query.filter_by(product_name=product_name).first()
        p_id = product_table.p_id
        stock_table = Stock.query.filter_by(p_id = p_id).first()
        stock_table.quantity -= bought_q
        db.session.commit()
        return render_template('order_success.html',user_name=user_name, what_done=what_done)
    
@app.route('/add-to-cart', methods=['GET','POST'])
def addto_cart():
    category_name = request.args.get('category_name')
    product_name = request.args.get('product_name')
    user_name = request.args.get('username')
    data = combined_view.query.filter_by(product_name = product_name).first()
    unit = data.unit
    quantity = data.quantity
    rate = data.rate_per_unit
    title = 'Adding to cart'
    function = 'Add to cart'
    what_done = 'Added to cart'
    if request.method=='GET':
        return render_template('buy_product.html',
                                user_name=user_name, product_name=product_name, category_name=category_name,
                                unit=unit, quantity=quantity, rate=rate, title=title, function=function)

    elif request.method=='POST':
        bought_q = int(request.form['quantity_given'])
        price_total = rate * bought_q
        newdata = Cart(u_name=user_name, category_name=category_name, product_name=product_name,
                       unit=unit, rate_per_unit=rate, quantity=bought_q, price_total=price_total)
        db.session.add(newdata)
        db.session.commit()
        return render_template('order_success.html',user_name=user_name, what_done=what_done)

@app.route('/update-cart', methods=['GET','POST'])
def update_cart():
    category_name = request.args.get('category_name')
    product_name = request.args.get('product_name')
    user_name = request.args.get('username')
    data = db.session.query(Cart).filter_by(product_name=product_name).first()
    stock = db.session.query(combined_view).filter_by(product_name=product_name).first()
    title = 'Updating Cart'
    function = 'Update cart'
    if request.method=='GET':
        return render_template('buy_product.html',
                               user_name=user_name, product_name=product_name, category_name=category_name,
                               unit=stock.unit, quantity=stock.quantity, rate=stock.rate_per_unit,
                               title=title, function=function)
    elif request.method=='POST':
        bought_q = int(request.form['quantity_given'])

        cart = Cart.query.get_or_404(data.ct_id)
        cart.quantity = bought_q
        cart.price_total = bought_q * cart.rate_per_unit
        db.session.commit()
    return redirect(url_for('review_cart',username = user_name))

@app.route('/cart', methods=['GET','POST'])
def review_cart():
    user_name = request.args.get('username')
    cart_table = Cart.query.filter_by(u_name=user_name).all()
    
    x = db.session.query(Cart.price_total).filter_by(u_name = user_name)
    l = [i[0] for i in x]
    print(l)
    total_price = sum(x for x in l)
    print(total_price)
    return render_template('cart.html',user_name = user_name, cart=cart_table, total_price=total_price)

@app.route('/checkout-cart', methods=['GET','POST'])
def checkout():
    user_name = request.args.get('user_name')
    cart_data = db.session.query(Cart).filter_by(u_name = user_name).all()

    for i in cart_data:
        product_name = i.product_name
        # print(product_name,i.quantity)
        p_id = db.session.query(Product.p_id).filter_by(product_name=product_name).first()
        # print(p_id[0])
        s_id = db.session.query(Stock.s_id).filter_by(p_id=p_id[0]).first()
        # print(s_id[0])
        stock = Stock.query.get_or_404(s_id[0])
        # print(stock.quantity,i.quantity)

        stock.quantity -= i.quantity
        db.session.commit()

    print(cart_data)
    for i in cart_data:
        ct_id = i.ct_id
        print(ct_id)
        # product = Product.query.get(product_id)
        cart = Cart.query.get(ct_id)
        db.session.delete(cart)
        db.session.commit()
    return redirect(url_for('user_dashboard',username = user_name))

