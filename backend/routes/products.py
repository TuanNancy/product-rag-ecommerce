from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.product_service import (
    get_products,
    get_product_by_id
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
async def list_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of products to return"),
    company: Optional[str] = Query(None, description="Filter by company name"),
    type_name: Optional[str] = Query(None, description="Filter by product type")
):
    """
    Lấy danh sách sản phẩm với pagination và filtering
    
    - **skip**: Số lượng sản phẩm bỏ qua (mặc định: 0)
    - **limit**: Số lượng sản phẩm tối đa (mặc định: 100, tối đa: 1000)
    - **company**: Lọc theo tên hãng (tùy chọn)
    - **type_name**: Lọc theo loại sản phẩm (tùy chọn)
    """
    try:
        result = get_products(
            skip=skip,
            limit=limit,
            company=company,
            type_name=type_name
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading products: {str(e)}")


@router.get("/{product_id}")
async def get_product(product_id: int):
    """
    Lấy thông tin chi tiết sản phẩm theo ID
    
    - **product_id**: ID của sản phẩm (laptop_ID)
    """
    product = get_product_by_id(product_id)
    
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )
    
    return product
