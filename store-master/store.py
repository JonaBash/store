from bottle import route, run, template, static_file, get, post, delete, request, response
from sys import argv
import json
import pymysql


connection = pymysql.connect(host="localhost",
                             user="root",
                             password="admin",
                             db="store",
                             charset="utf8",
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@post('/category')
def add_category():
    name = request.forms.get('name')
    try:
        with connection.cursor() as cursor:
            if name == '':
                return json.dumps({'STATUS': 'ERROR', 'MSG': "Category name can't be empty"})
            else:
                sql = "INSERT INTO categories (name) VALUES ('{}')".format(name)
                cursor.execute(sql)
                connection.commit()
                cat_id = cursor.lastrowid
            return json.dumps({'STATUS': 'SUCCESS', 'CAT_ID': cat_id})
    except:
        if response.status_code == 200:
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'The category already exist'})
        elif response.status_code == 400:
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'Bad request'})
        elif response.status_code == 500:
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error'})


@delete('/category/<id>')
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM categories WHERE id = {}'.format(id)
            cursor.execute(sql)
            connection.commit()
        return json.dumps({'STATUS': 'SUCCESS', 'MSG': 'The category was deleted succesfully'})
    except:
        if response.status_code == 404:
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'Category not found'})
        elif response.status_code == 500:
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error'})


@get('/categories')
def show_categories():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT id, name FROM categories'
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
        return json.dumps({'STATUS': 'SUCCESS', 'CATEGORIES': result})
    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error'})


@post('/product')
def add_or_edit_product():
    id = request.forms.get('id')
    title = request.forms.get('title')
    desc = request.forms.get('desc')
    price = request.forms.get('price')
    img_url = request.forms.get('img_url')
    category = request.forms.get('category')
    favorite = request.forms.get('favorite')

    if favorite == "on":
        favorite = 1
    else:
        favorite = 0
    try:
        for i in [category, title, desc, favorite, price, img_url]:
            if i == "" or i is None:
                return json.dumps({"STATUS": "ERROR", "MSG": "Missing parameter"})
        with connection.cursor() as cursor:
            if id == "":
                sql = "INSERT INTO products (title, description, img_url, price, category, favorite) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(title, desc, img_url, price, category, favorite)
            else:
                sql = "UPDATE products SET title = '{}', description = '{}', img_url = '{}', price = '{}', category = '{}', favorite = '{}'"
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "Product was added/updated successfully", "PRODUCT_ID": cursor.lastrowid, "CODE": 201})

    except:
        if response.status_code == 404:
            return json.dumps({"STATUS": "ERROR", "MSG": "Category not found"})
        elif response.status_code == 500:
            return json.dumps({"STATUS": "ERROR", "MSG": "Internal Error"})


@get('/product/<id>')
def show_product(id):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM product WHERE id={}'.format(id)
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
        return json.dumps({'STATUS': 'SUCCESS', 'PRODUCT': result})
    except:
        if response.status_code == 404:
            return json.dumps({"STATUS": "ERROR", "MSG": "Category not found"})
        elif response.status_code == 500:
            return json.dumps({"STATUS": "ERROR", "MSG": "Internal Error"})


@delete('/product/<id>')
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM product WHERE id = {}'.format(id)
            cursor.execute(sql)
            connection.commit()
        return json.dumps({'STATUS': 'SUCCESS', 'MSG': 'The product was deleted succesfully'})
    except:
        if response.status_code == 404:
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'Product not found'})
        elif response.status_code == 500:
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error'})

@get('/products')
def show_products():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM products'
            cursor.execute(sql)
            connection.commit()
            products = cursor.fetchall()
        return json.dumps({'STATUS': 'SUCCESS', 'PRODUCTS': products})
    except:
        if response.status_code == 500:
            return json.dumps({"STATUS": "ERROR", "MSG": "Internal Error"})

@get('/category/<id>/products')
def get_products(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE category = '{}' ORDER BY favorite DESC, id ASC".format(id)
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
        return json.dumps({'STATUS': 'SUCCESS', 'PRODUCTS': result})
    except:
        if response.status_code == 404:
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'Category not found'})
        elif response.status_code == 500:
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error'})


run(host='0.0.0.0', port=argv[1])
#if __name__ == "__main__":
#   run(host='localhost', port=7000)