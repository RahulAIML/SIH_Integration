import sqlite3
import json
from typing import List, Dict, Any, Optional
import os

DB_NAME = "millet_marketplace.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Products Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        millet_type TEXT NOT NULL,
        product_form TEXT NOT NULL,
        description TEXT,
        available_quantity_kg REAL NOT NULL,
        price_per_kg REAL NOT NULL,
        minimum_order_kg REAL DEFAULT 1,
        harvest_date TEXT,
        organic_certified BOOLEAN DEFAULT 0,
        quality_grade TEXT,
        moisture_content REAL,
        location_state TEXT NOT NULL,
        location_district TEXT NOT NULL,
        seller_id TEXT NOT NULL,
        certifications TEXT, -- JSON string
        images TEXT, -- JSON string
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize DB on module load
init_db()

def create_product(product_data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Handle JSON fields
    certifications = json.dumps(product_data.get("certifications")) if product_data.get("certifications") else None
    images = json.dumps(product_data.get("images")) if product_data.get("images") else None
    
    cursor.execute('''
    INSERT INTO products (
        title, millet_type, product_form, description, available_quantity_kg,
        price_per_kg, minimum_order_kg, harvest_date, organic_certified,
        quality_grade, moisture_content, location_state, location_district,
        seller_id, certifications, images, is_active
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        product_data["title"], product_data["millet_type"], product_data["product_form"],
        product_data.get("description"), product_data["available_quantity_kg"],
        product_data["price_per_kg"], product_data.get("minimum_order_kg", 1),
        product_data.get("harvest_date"), product_data.get("organic_certified", False),
        product_data.get("quality_grade"), product_data.get("moisture_content"),
        product_data["location_state"], product_data["location_district"],
        product_data["seller_id"], certifications, images,
        product_data.get("is_active", True)
    ))
    
    product_id = cursor.lastrowid
    conn.commit()
    
    # Fetch created product
    product = get_product_by_id(product_id)
    conn.close()
    return product

def get_products(seller_id: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if seller_id:
        cursor.execute('SELECT * FROM products WHERE seller_id = ? ORDER BY created_at DESC', (seller_id,))
    else:
        cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
        
    rows = cursor.fetchall()
    conn.close()
    
    products = []
    for row in rows:
        product = dict(row)
        # Parse JSON fields
        if product.get("images"):
            try:
                product["images"] = json.loads(product["images"])
            except:
                product["images"] = []
        else:
            product["images"] = []
            
        if product.get("certifications"):
            try:
                product["certifications"] = json.loads(product["certifications"])
            except:
                product["certifications"] = []
        else:
            product["certifications"] = []
            
        products.append(product)
    
    conn.close()
    return products

def get_product_by_id(product_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        product = dict(row)
        # Parse JSON fields
        if product.get("images"):
            try:
                product["images"] = json.loads(product["images"])
            except:
                product["images"] = []
        else:
            product["images"] = []
            
        if product.get("certifications"):
            try:
                product["certifications"] = json.loads(product["certifications"])
            except:
                product["certifications"] = []
        else:
            product["certifications"] = []
            
        return product
    return None

def update_product(product_id: int, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if exists
    cursor.execute('SELECT id FROM products WHERE id = ?', (product_id,))
    if not cursor.fetchone():
        conn.close()
        return None
        
    # Build update query dynamically
    fields = []
    values = []
    
    for key, value in product_data.items():
        if key in ["certifications", "images"]:
            value = json.dumps(value) if value else None
            
        fields.append(f"{key} = ?")
        values.append(value)
        
    if not fields:
        conn.close()
        return get_product_by_id(product_id)
        
    values.append(product_id)
    query = f"UPDATE products SET {', '.join(fields)} WHERE id = ?"
    
    cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()
    
    return get_product_by_id(product_id)

def delete_product(product_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
