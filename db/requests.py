from .connection import Session
from .models import User, BestProduct, LogSendProdcut


async def get_user(user_id: str):
    session = Session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    return user


async def create_user(user_id: str, username: str = None):
    session = Session()
    try:
        user = User(telegram_id=int(user_id), username=username)
        session.add(user)
        session.commit()
    except Exception as exp:
        print(f"ERROR | Что-то пошло не так. {exp}")
    finally:
        session.close()


async def check_user_best_products(user_id: str):
    session = Session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    user_best_products = (
        session.query(BestProduct).filter_by(user_id=user.id).first()
    )
    session.close()
    return user_best_products


async def create_best_product(
    user_id: str, message_id: int,
):
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        best_product = BestProduct(
            user_id=user.id,
            message_id=message_id,
        )
        session.add(best_product)
        session.commit()
    except Exception as exp:
        print(f"ERROR | Что-то пошло не так. {exp}")
    finally:
        session.close()


async def get_log_products():
    session = Session()
    all_products = session.query(LogSendProdcut).all()
    session.close()
    return all_products


async def save_log_products(products):
    session = Session()
    session.bulk_save_objects(products)
    session.commit()
    session.close()


async def update_was_send_product(product_id: int):
    session = Session()
    session.query(LogSendProdcut).filter_by(product_id=product_id).update({LogSendProdcut.was_send: True})
    session.commit()
    session.close()


async def get_log_product_first():
    session = Session()
    product = session.query(LogSendProdcut).filter_by(was_send=False).first()
    session.close()
    return product


async def delete_log_product():
    session = Session()
    session.query(LogSendProdcut).delete()
    session.commit()
    session.close()


