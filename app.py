from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
db.init_app(app)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birthdate']
        date_of_death = request.form['date_of_death']
        author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        print(author)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('add_author'))
    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']
        book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('add_book'))
    return render_template('add_book.html', authors=authors)


# def create_tables():
#   try:
#     db.create_all()
#     print("Tables created successfully.")
#   except Exception as e:
#     print(f"Error creating tables: {e}")

@app.route('/')
def home():
    search_query = request.args.get('search')
    if search_query:
        books = Book.query.filter(Book.title.contains(search_query)).all()
    else:
        books = Book.query.all()

    return render_template('home.html', books=books)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author_id = book.author_id
    db.session.delete(book)
    db.session.commit()

    # Check if the author has any other books
    other_books = Book.query.filter_by(author_id=author_id).count()
    if other_books == 0:
        author = Author.query.get(author_id)
        db.session.delete(author)
        db.session.commit()

    return redirect(url_for('home'))


# with app.app_context():
#     db.create_all()


if __name__ == '__main__':
    # create_tables()
    app.run(host="0.0.0.0", port=5002, debug=True)