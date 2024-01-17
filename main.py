from flask import Flask,render_template,request,redirect
import psycopg2
from mydb import check_email_password,sale_info

conn=psycopg2.connect(
host='localhost',
dbname='myduka_db',
user='postgres',
password='tosh',
port='5432'
)

curr=conn.cursor()

app=Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/home')
def home():
    return "home"

@app.route('/products')
def products():
    curr.execute('select*from products')
    products=curr.fetchall()
    return render_template("products.html",products=products)
@app.route ('/add_product',methods=['post'])
def add_products():
    product_name=request.form["name"]
    buying_price=request.form["Buying_price"]
    selling_price=request.form["Selling_price"]
    stock_quantity=request.form["Stock_quantity"]
    values=(product_name,buying_price,selling_price,stock_quantity)

    insert_query='''INSERT INTO products(name, buying_price, selling_price, stock_quantity)VALUES(%s, %s, %s, %s)'''

    curr.execute(insert_query, values)
    conn.commit()
    return redirect("/products")


@app.route("/sale")
def sale():
    curr.execute('SELECT*from sale')
    sale=curr.fetchall()
    print(sale)

    curr.execute('SELECT*from products')
    products=curr.fetchall()
    return render_template("sale.html", sale=sale, products=products)

@app.route("/add_sale",methods=["POST"])
def add_sale():
    product_id=request.form["pid"]
    quantity=request.form["quantity"]
    my_sale=(product_id,quantity)
    insert_sale='''INSERT INTO public.sale(pid, quantity, created_at)VALUES(%s, %s, now())'''
    curr.execute(insert_sale,my_sale)
    conn.commit()
    return redirect("/sale")



@app.route('/register',methods=['post','get'])
def register():
    if request.method=='post':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        value=(name,email,password)
        register_user="insert into users(name,email,password)values(%s,%s,%s);"
        curr.execute(register_user,value)
        conn.commit()
    return render_template('register.html')

    

@app.route('/login', methods=["POST",'GET'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=check_email_password(email,password)
        if user:
            return redirect('/dashboard')
        else:
            return redirect('/register')
    return render_template('login.html')    


@app.route('/dashboard')
def dashboard():
    productss=[]
    total_saless=[]
    for i in sale_info():
        productss.append(str(i[0]))
        total_saless.append(i[1])
    return render_template('dashboard.html',productss=productss,total_saless=total_saless)


conn.commit()
app.run( debug=True)    