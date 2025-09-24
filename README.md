# Products API

## Database Connection Setup

1. Edit file `app.py` pada bagian berikut:
	 ```python
	 app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>"
	 ```
	 Contoh:
	 ```python
	 app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:yourpassword@localhost:3306/products_db"
	 ```
2. Pastikan MySQL sudah berjalan dan database sudah dibuat.
3. Install package yang dibutuhkan:
	 ```bash
	 pip install flask flask_sqlalchemy pymysql
	 ```

## API Documentation

### List Products
- **Endpoint:** `GET /api/products`
- **Response:**
	```json
	[
		{"id": 1, "name": "Product A", "price": 10000, "quantity": 5},
		...
	]
	```

### Get Product by ID
- **Endpoint:** `GET /api/products/<product_id>`
- **Response:**
	```json
	{"id": 1, "name": "Product A", "price": 10000, "quantity": 5}
	```

### Create Product
- **Endpoint:** `POST /api/products`
- **Request Body:**
	```json
	{"name": "Product A", "price": 10000, "quantity": 5}
	```
- **Response:**
	```json
	{"id": 1, "name": "Product A", "price": 10000, "quantity": 5}
	```

### Export Products (CSV)
- **Endpoint:** `GET /export_products`
- **Response:** CSV file download

### Import Products (CSV)
- **Endpoint:** `POST /import_products`
- **Form Data:**
	- `file`: CSV file
- **Response:** Redirect to home

### Delete All Products
- **Endpoint:** `POST /delete_all_products`
- **Response:** Redirect to home

## How to Run
1. Jalankan perintah berikut:
	 ```bash
	 python app.py
	 ```
2. Buka browser ke `http://localhost:5001`

## Catatan
1. Buatlah sebuah database dan gunakan pada konfigurasi database di bagian app.py sebelum menjalankan aplikasi.
2. Wajib konek internet untuk penggunaan tailwindcss dari CDN.
---