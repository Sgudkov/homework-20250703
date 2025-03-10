import unittest
from unittest.mock import MagicMock

from domain.models import Product, Order
from infrastructure.orm import ProductORM, OrderORM
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository


class TestWarehouseORM(unittest.TestCase):

    def test_positive_add_product_orm(self):
        session = MagicMock()
        product_repo = SqlAlchemyProductRepository(session)
        test = Product(id=0, name="test1", quantity=1, price=100)
        product_repo.add(test)

        product_repo.get = MagicMock(return_value=test)

        self.assertEqual(product_repo.get(0), test)

    def test_positive_add_order_orm(self):
        session = MagicMock()
        order_repo = SqlAlchemyOrderRepository(session)
        test = Order(id=0, products=[ProductORM(id=0, name="test1", quantity=1, price=100)])
        order_repo.add(test)
        order_repo.get = MagicMock(return_value=test)

        self.assertEqual(order_repo.get(0), test)
