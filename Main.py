from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask (__name__)

#will connect to books.db
def create_connection():
    return sql.connect('books.db')

connection = sql.connect('books.db')
cursor = connection.cursor()

#will create a new database if it already doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year_published INTEGER NOT NULL,
                    genre TEXT NOT NULL,
                    description TEXT NOT NULL,
                    image_url TEXT NOT NULL,
                    reviews TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS purchases (
                    id INTEGER PRIMARY KEY,
                    book_name TEXT NOT NULL,
                    author TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    shipping_method TEXT NOT NULL,
                    shipping_address TEXT
                )''')

connection.commit()
connection.close()


# Homepage
@app.route ('/')
def index():
    render_template ('base.html')
    return render_template (
        'homepage.html', 
        PageName = "Home"
    )

# View books
@app.route ('/Book/<bookName>')
def view_book(bookName):
    render_template ('base.html')
    return render_template("viewBook.html",
        PageName = bookName,
        Author = "John Doe",
        YearPublished = "2023",
        Genre = "Fiction",
        BookDescription = "This is a great book description. This book tells the wonderful tale of me trying to fill out space to make a description that looks like a real desciption.",
        ImageName = "/static/Test.png",
        Reviews = {
            "Jane Doe: This is great", 
            "Greg Doe: I hated this book"
        }
    )

# Purchase confirmation
@app.route('/Purchase/<bookName>', methods=['GET'])
def purchase_book(bookName):
    render_template ('base.html')
    return render_template("purchase.html",
        PageName = bookName,
        Author = "John Doe",
    )

# Purchase successful - added: whenever the customer clicks confirm purchase, it will automatically show up on "Customer Purchases" on the employee side
@app.route('/PurchaseSuccess', methods=['GET', 'POST'])
def purchase_success():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        book_name = request.form['bookName']
        shipping_method = request.form['shippingMethod']
        shipping_address = request.form['address'] if shipping_method == 'Ship' else None

        connection = create_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO purchases (book_name, author, first_name, last_name, email, shipping_method, shipping_address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (book_name, "Author 1", first_name, last_name, email, shipping_method, shipping_address))
            connection.commit()

        return render_template("purchaseConfirmed.html", PageName="Success")

    else:
        return redirect(url_for('index'))
    
# User Page
@app.route ('/Users')
def user_homepage():
    render_template ('base.html')
    return render_template("usersHomepage.html",
        PageName = "User",
    )

# Employee Page
@app.route ('/Employees')
def employee_homepage():
    render_template ('base.html')
    return render_template("workersHomepage.html",
        PageName = "Employee",
    )

# View Inventory - added all books 
@app.route('/ViewInventory')
def view_inventory():
    books_data = [
        ("The Hunger Games", "Suzanne Collins", 10),
        ("Harry Potter", "J.K Rowling", 3),
        ("Throne of Glass", "Sarah J Mass", 9),
        ("The Giver", "Lois Lowry", 20),
        ("The Fault in Our Stars", "John Green", 5),
        ("Six of Crows", "Leigh Bardugo", 21),
        ("The Ember in the Ashes", "Sabaa Tahir", 13),
        ("Legend", "Marie Lu", 22),
        ("Percy Jackson", "Rick Riordan", 6),
        ("I'll Give You The Sun", "Jandy Nelson", 2),
        ("Looking For Alaska", "John Green", 8),
        ("We Were Liars", "E. Lockhart", 5)
    ]
    return render_template("viewInventory.html", PageName="Inventory", books=books_data)



# View Purchases
@app.route('/ViewPurchases', methods=['GET'])
def view_purchases():
    connection = create_connection()
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM purchases")
        purchases = cursor.fetchall()
    return render_template("viewPurchases.html", PageName="Purchases", purchases=purchases)


if __name__ == '__main__':
    app.run()
