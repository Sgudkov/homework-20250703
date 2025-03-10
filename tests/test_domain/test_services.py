import unittest
from unittest.mock import MagicMock

from domain.models import Product, Order
from domain.services import WarehouseService
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository


class TestWarehouseService(unittest.TestCase):
    def test_positive_create_product(self):
        session = MagicMock()
        product_repo = SqlAlchemyProductRepository(session)
        order_repo = SqlAlchemyOrderRepository(session)

        warehouse_service = WarehouseService(product_repo, order_repo)

        test = Product(id=0, name="test2", quantity=10, price=10)

        warehouse_service.create_product = MagicMock(return_value=test)

        result = warehouse_service.create_product(test.name, test.quantity, test.price)

        self.assertEqual(result, test)

    def test_positive_create_order(self):
        session = MagicMock()
        product_repo = SqlAlchemyProductRepository(session)
        order_repo = SqlAlchemyOrderRepository(session)

        warehouse_service = WarehouseService(product_repo, order_repo)
        test_product = Product(id=0, name="test2", quantity=10, price=10)
        test_order = Order(id=0, products=[test_product])
        warehouse_service.create_order = MagicMock(return_value=test_order)

        result = warehouse_service.create_order([test_product])

        self.assertEqual(result, test_order)
