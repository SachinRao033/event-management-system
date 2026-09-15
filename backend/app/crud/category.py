from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

def create_category(
        db: Session,
        category: CategoryCreate,
) -> Category:
        db_category = Category(
            name=category.name,
            description=category.description,   
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

def get_category_by_id(
    db: Session,
    category_id: int,
) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(
    db: Session,
    name: str,
) -> Category | None:
    return db.query(Category).filter(func.lower(Category.name) == name.lower()).first()

def get_all_categories(
    db: Session,
) -> list[Category]:
    return db.query(Category) .order_by(Category.name).all()

def update_category(
    db: Session,
    db_category: Category,
    category_update: CategoryUpdate,
) -> Category:
    update_data = category_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)

    return db_category

def delete_category(
    db: Session,
    db_category: Category,
) -> None:
    db.delete(db_category)
    db.commit()