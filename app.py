import csv
from io import StringIO
from flask import Flask, jsonify, request, render_template, redirect, url_for, Response
from models.products import db, Product

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:M1r34cl3@localhost:3306/products_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form.get("name").strip()
    price = request.form.get("price").strip()
    quantity = request.form.get("quantity").strip()

    error = None
    if not name:
        error = "Name is required"
    elif not price:
        error = "Price is required"
    elif not price.isdigit() or int(price) < 0:
        error = "Price must be a non-negative integer"
    elif not quantity.isdigit() or int(quantity) < 0:
        error = "Quantity must be a non-negative integer"

    if error:
        return render_template("index.html", error=error)


    new_product = Product(name=name, price=price, quantity=quantity)
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for("home"))

@app.route('/edit_product/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return redirect(url_for('home'))
    name = request.form.get('name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    product.name = name
    product.price = price
    product.quantity = quantity
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('home'))

@app.template_filter('ribuan')
def ribuan(value):
    try:
        return "{:,}".format(int(value))
    except Exception:
        return value

@app.route('/export_products')
def export_products():
    products = Product.query.all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'name', 'price', 'quantity'])
    for p in products:
        cw.writerow([p.id, p.name, p.price, p.quantity])
    output = si.getvalue()
    return Response(output, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=products.csv"})

@app.route('/import_products', methods=['POST'])
def import_products():
    file = request.files.get('file')
    if not file:
        return redirect(url_for('home'))
    stream = StringIO(file.stream.read().decode("UTF8"))
    reader = csv.DictReader(stream)
    for row in reader:
        product = Product(name=row['name'], price=row['price'], quantity=row.get('quantity', 0))
        db.session.add(product)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete_all_products', methods=['POST'])
def delete_all_products():
    Product.query.delete()
    db.session.commit()
    return redirect(url_for('home'))

# API Endpoints
@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify(products)

@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity })
    return jsonify({"error": "Product not found"}), 404


@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
    product = Product(name=data.get("name"), price=data.get("price"))
    db.session.add(product)
    db.session.commit()
    return jsonify({"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity}), 201

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.get_json()
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    db.session.commit()
    return jsonify({"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity})

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product_api(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
