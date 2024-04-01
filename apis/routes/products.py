from fastapi import APIRouter, status
from pydantic import BaseModel
from prisma.models import User as UserModel

from apis.prisma import prisma

router = APIRouter()


class Product(BaseModel):
  name: str
  description: str
  price: float


@router.post("/product/create", tags=["product"], status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    product = await prisma.product.create(
        {
            "price": product.price,
            "name":  product.name,
            "description": product.description

        }
    )
    return product


@router.get("/product/{productId}", tags=["product"], status_code=status.HTTP_200_OK)
async def read_product(productId: str):
    product = await prisma.product.find_unique(where={"id": productId})

    return product


@router.get("/products", tags=["product"], status_code=status.HTTP_200_OK)
async def read_products():
    products = await prisma.product.find_many()

    return products


@router.delete("/product/{productId}", tags=["product"], status_code=status.HTTP_200_OK)
async def delete_product(productId: str):
    product = await prisma.product.delete(where={"id": productId})

    return product


@router.put("/update-product/{productId}", tags=["product"], status_code=status.HTTP_200_OK)
async def update_product(*, productId: str, product: Product):
    updatedProduct = await prisma.product.update(
        where={"id": productId},
        data={"name": product.name,
              "description": product.description, "price": product.price}
    )

    return {"message": f"Product with id {updatedProduct.id} has been updated successfully"}