from flask import Flask, render_template, request, redirect, url_for, make_response
import requests

app = Flask(__name__)
FASTAPI_URL = "http://127.0.0.1:8000"

@app.route("/")
def home():
    response = requests.get(f"{FASTAPI_URL}/products")
    products = response.json()
    return render_template("index.html", products=products)

# Create Product
@app.route("/add_product", methods=["POST"])
def add_product():
    data = {
        "name": request.form["name"],
        "price": request.form["price"],
        "quantity": request.form["quantity"]
    }
    requests.post(f"{FASTAPI_URL}/products", json=data)
    return redirect(url_for("home"))

# Edit Product
@app.route("/edit_product/<int:product_id>", methods=["POST"])
def edit_product(product_id):
    data = {
        "name": request.form["name"],
        "price": request.form["price"],
        "quantity": request.form["quantity"]
    }
    requests.put(f"{FASTAPI_URL}/products/{product_id}", json=data)
    return redirect(url_for("home"))

@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    requests.delete(f"{FASTAPI_URL}/products/{product_id}")
    return redirect(url_for("home"))

@app.route("/export_products")
def export_products():
    api_response = requests.get(f"{FASTAPI_URL}/products/export")
    response = make_response(api_response.content)
    response.headers["Content-Disposition"] = "attachment; filename=products.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@app.route("/import_products", methods=["POST"])
def import_products():
    file = request.files.get("file")
    if not file:
        return redirect(url_for("home"))
    files = {"file": (file.filename, file.stream, file.mimetype)}
    requests.post(f"{FASTAPI_URL}/products/import", files=files)
    return redirect(url_for("home"))

@app.route("/delete_all_products", methods=["POST"])
def delete_all_products():
    requests.delete(f"{FASTAPI_URL}/products")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
