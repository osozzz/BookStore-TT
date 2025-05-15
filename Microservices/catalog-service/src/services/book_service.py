from src.extensions import db
from src.models.book import Book

def get_all_books():
    books = Book.query.all()
    return [b.to_dict() for b in books]

def get_user_books(user_id):
    books = Book.query.filter_by(seller_id=user_id).all()
    return [b.to_dict() for b in books]

def add_book(data, user_id):
    required = ["title", "author", "description", "price", "stock"]
    if not all(k in data for k in required):
        return {"error": "Campos incompletos"}, 400

    book = Book(
        title=data["title"],
        author=data["author"],
        description=data["description"],
        price=float(data["price"]),
        stock=int(data["stock"]),
        seller_id=user_id
    )
    db.session.add(book)
    db.session.commit()
    return {"message": "Libro agregado"}, 201

def update_book(book_id, data, user_id):
    book = Book.query.get_or_404(book_id)
    if book.seller_id != user_id:
        return {"error": "No tienes permiso para editar este libro"}, 403

    for field in ["title", "author", "description", "price", "stock"]:
        if field in data:
            setattr(book, field, data[field])

    db.session.commit()
    return {"message": "Libro actualizado"}, 200

def delete_book(book_id, user_id):
    book = Book.query.get_or_404(book_id)
    if book.seller_id != user_id:
        return {"error": "No tienes permiso para eliminar este libro"}, 403

    db.session.delete(book)
    db.session.commit()
    return {"message": "Libro eliminado"}, 200
