import psycopg2

conn=psycopg2.connect(
    host='localhost',
    dbname='myduka_db',
    user='postgres',
    password='tosh',
    port=5432
)

curr=conn.cursor()


def check_email_password(email,password):
    query="SELECT user id,name from users WHERE email=%s AND password=%s"
    curr.execute(query, (email, password))
    result=curr.fetchone()
    if result is not None:
        id=result[0]
        name=result[1]
        return id,name
    else:
        return None

def sale_info():
    cur= conn.cursor()
    sales_info="""SELECT products.name,SUM(sale.quantity) AS total_sales
	FROM sale
	JOIN products ON products.id=sale.pid
	GROUP BY products.name;"""
    cur.execute(sales_info)
    info=cur.fetchall()
    print(info)
    return info

# def check_email_exists():