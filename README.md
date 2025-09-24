# Products API

## Database Connection Setup

1. Buat file `.env` di root project Anda dengan isi seperti berikut:
	```env
	DATABASE_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
	```
	Contoh:
	```env
	DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/products_db
	```
	File `.env` ini akan otomatis dibaca oleh aplikasi (menggunakan python-dotenv).
2. Pastikan MySQL sudah berjalan dan database sudah dibuat.
3. Install package yang dibutuhkan:
	```bash
	pip install flask fastapi uvicorn sqlalchemy pymysql requests pydantic python-dotenv
	```

## API Documentation

### List Products
- **Endpoint:** `GET /products`
- **Response:**
	```json
	[
		{"id": 1, "name": "Product A", "price": 10000, "quantity": 5},
		...
	]
	```

### Get Product by ID
- **Endpoint:** `GET /products/{product_id}`
- **Response:**
	```json
	{"id": 1, "name": "Product A", "price": 10000, "quantity": 5}
	```

### Create Product
- **Endpoint:** `POST /products`
- **Request Body:**
	```json
	{"name": "Product A", "price": 10000, "quantity": 5}
	```
- **Response:**
	```json
	{"id": 1, "name": "Product A", "price": 10000, "quantity": 5}
	```

### Update Product
- **Endpoint:** `PUT /products/{product_id}`
- **Request Body:**
	```json
	{"name": "Product A", "price": 10000, "quantity": 5}
	```
- **Response:**
	```json
	{"id": 1, "name": "Product A", "price": 10000, "quantity": 5}
	```

### Delete Product
- **Endpoint:** `DELETE /products/{product_id}`
- **Response:**
	```json
	{"detail": "Product deleted"}
	```

### Delete All Products
- **Endpoint:** `DELETE /products`
- **Response:**
	```json
	{"detail": "All products deleted"}
	```

### Export Products (CSV)
- **Endpoint:** `GET /products/export`
- **Response:** CSV file download

### Import Products (CSV)
- **Endpoint:** `POST /products/import`
- **Form Data:**
	- `file`: CSV file
- **Response:**
	```json
	{"detail": "Products imported"}
	```

## How to Run
1. Jalankan perintah berikut untuk Flask FE:
	 ```bash
	 python app.py
	 ```
2. Jalankan perintah berikut untuk FastAPI nya:
    ```bash
    uvicorn main:app --reload
   ```
3. Buka browser ke `http://localhost:5001`
4. API running di `http://localhost:8000`

## Catatan
1. Wajib konek internet untuk penggunaan tailwindcss dari CDN.
---