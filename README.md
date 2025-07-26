# SQLAlchemy ORM Example

This example demonstrates how to interact with a database using SQLAlchemy ORM with repository and unit of work
patterns.

## Code Example

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from domain.models import Product
from domain.services import WarehouseService
from infrastructure.orm import Base, ProductORM, OrderORM
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.database import DATABASE_URL

# Database initialization
engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def main():
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)

    uow = SqlAlchemyUnitOfWork(session)
    warehouse_service = WarehouseService(product_repo, order_repo)

    # Create product
    with uow:
        new_product = warehouse_service.create_product(name="test1", quantity=1, price=100)
        uow.commit()
        print(f"Created product: {new_product}")

    # Create order
    with uow:
        new_order = warehouse_service.create_order([new_product])
        uow.commit()
        print(f"Created order: {new_order}")


if __name__ == "__main__":
    main()
```

## Key Components

### Database Setup

- `create_engine()` - Connects to the database (URL defined in `DATABASE_URL`)
- `sessionmaker()` - Configures a factory for creating new sessions
- `Base.metadata.create_all()` - Creates tables for all mapped ORM classes

### Repository Pattern

- `SqlAlchemyProductRepository` - Handles database operations for Product entities
- `SqlAlchemyOrderRepository` - Handles database operations for Order entities

### Unit of Work

- `SqlAlchemyUnitOfWork` - Manages transactions using context manager (`with` blocks)
    - Automatically handles commits and rollbacks
    - Provides atomic operations

### Domain Service

- `WarehouseService` - Contains business logic and coordinates repositories
    - `create_product()` - Creates and persists new Products
    - `create_order()` - Creates Orders linked to products

## How It Works

1. **Initialization**:
   ```python
   engine = create_engine(DATABASE_URL)
   SessionFactory = sessionmaker(bind=engine)
   Base.metadata.create_all(engine)
   ```

2. **Operation Flow**:

    - Create session and repositories
    - Initialize Unit of Work
    - Perform operations within with blocks:
   ```python
   with uow:
    # Database operations
    uow.commit()"
   ```
3. **Entity Creation**:

    - Products are created first
    - Orders reference existing products

## Usage

1. **Install dependencies**:

```bash
pip install sqlalchemy
```

2. **Configure database URL in infrastructure/database.py**:

```python
DATABASE_URL = "sqlite:///warehouse.db"  # Example for SQLite
```

3. **Run the application**:

```bash
python main.py
```

## Expected Output

```text
Created product: <Product(id=1, name="test1", quantity=1, price=100)>
Created order: <Order(id=1, products=[1])>
```