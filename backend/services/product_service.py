import pandas as pd
import os
from typing import List, Dict, Optional
from pathlib import Path

# Đường dẫn đến file CSV
CSV_PATH = Path(__file__).parent.parent / "data" / "laptop_price.csv"


def load_products() -> List[Dict]:
    """
    Đọc tất cả sản phẩm từ CSV file
    Returns: List of product dictionaries
    """
    if not CSV_PATH.exists():
        return []
    
    df = pd.read_csv(CSV_PATH)
    
    # Convert DataFrame to list of dictionaries
    # Replace NaN với None để JSON serializable
    products = df.replace({pd.NA: None}).to_dict(orient="records")
    
    return products


def get_product_by_id(product_id: int) -> Optional[Dict]:
    """
    Lấy sản phẩm theo ID
    Args:
        product_id: ID của sản phẩm (laptop_ID)
    Returns: Product dictionary hoặc None nếu không tìm thấy
    """
    products = load_products()
    
    for product in products:
        if product.get("laptop_ID") == product_id:
            return product
    
    return None


def get_products(
    skip: int = 0,
    limit: int = 100,
    company: Optional[str] = None,
    type_name: Optional[str] = None
) -> Dict:
    """
    Lấy danh sách sản phẩm với pagination và filtering
    Args:
        skip: Số lượng sản phẩm bỏ qua (pagination)
        limit: Số lượng sản phẩm tối đa trả về
        company: Lọc theo hãng (optional)
        type_name: Lọc theo loại (optional)
    Returns: Dict với 'products' và 'total'
    """
    products = load_products()
    
    # Filtering
    if company:
        products = [p for p in products if p.get("Company", "").lower() == company.lower()]
    
    if type_name:
        products = [p for p in products if p.get("TypeName", "").lower() == type_name.lower()]
    
    total = len(products)
    
    # Pagination
    paginated_products = products[skip : skip + limit]
    
    return {
        "products": paginated_products,
        "total": total,
        "skip": skip,
        "limit": limit
    }
