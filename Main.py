from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3 as sql

app = Flask (__name__)
app.secret_key = "ASF2T3B97V-2V930"

DATABASE_NAME = "bookstore.db"

#will connect to bookstore.db
def create_connection():
    return sql.connect(DATABASE_NAME)


connection = sql.connect(DATABASE_NAME)
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

cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                    book_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    review TEXT NOT NULL
                )''')

# Clearence level of 0 is a user; 1 is an employee
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY NOT NULL,
                    password TEXT NOT NULL,
                    clearenceLevel INTEGER NOT NULL
                )''')

# SQL command to insert a book
# cursor.execute(f'''INSERT INTO books (id, title, author, year_published, genre, description, image_url) 
#                            VALUES(2, "Book name", "Jane Doe", 2002, "Fiction", "Good book","Test.png")''')

# SQL command to insert an admin user
# cursor.execute(f'''INSERT INTO users (email, password, clearenceLevel) 
#                            VALUES("admin@uab.edu", "CS421Secured", 1)''')

connection.commit()
connection.close()


def isAccountAdmin():
    if "user" in session:
        email = session["user"]
        print(email)
        isAdmin = True

        connection = sql.connect(DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM users WHERE email = "{email}"')
        result = cursor.fetchall()
        if not result or not result[0]:
            isAdmin = False
        print(result[0])
        if result[0][2] != 1:
            isAdmin = False

        connection.commit()
        connection.close()
        return isAdmin

# Homepage
@app.route ('/')
def index():
    render_template ('base.html')
    if not isAccountAdmin():
        return render_template (
                'homepage.html', 
                PageName = "Home"
            )
    else:
        return redirect(url_for("employee_homepage"))

    

# View books
@app.route ('/Book/<bookName>', methods=['GET', 'POST'])
def view_book(bookName):
    if request.method == "POST":
        if not ("user" in session):
            return redirect(url_for("require_signIn"))
       
        connection = sql.connect(DATABASE_NAME)
        review = request.form['review']
        cursor = connection.cursor()
        cursor.execute(f'''INSERT INTO reviews (book_name, email, review) 
                            VALUES("{bookName}", "{session["user"]}", "{review}")''')
        connection.commit()
        connection.close()

    render_template ('base.html')

    connection = sql.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM books WHERE title LIKE "%{bookName}%"')
    bookData = cursor.fetchall()[0]

    cursor.execute(f'SELECT * FROM reviews WHERE book_name = "{bookName}"')
    reviewData = cursor.fetchall()
    reviews = []
    i = 0
    for review in reviewData:
        print(review)
        reviews.insert(i, review[1] + ": " + review[2])
        i += 1

    connection.commit()
    connection.close()

    return render_template("viewBook.html",
        PageName = bookName,
        Author = bookData[2],
        YearPublished = bookData[3],
        Genre = bookData[4],
        BookDescription = bookData[5],
        ImageName = "/static/"+bookData[6],
        Reviews = reviews
    )

# Purchase confirmation
@app.route('/Purchase/<bookName>', methods=['GET'])
def purchase_book(bookName):
    if not ("user" in session):
        return redirect(url_for("require_signIn"))
        

    render_template ('base.html')
    return render_template("purchase.html",
        PageName = bookName,
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

# User Sign Up
@app.route('/UserSignUp',methods=["POST", "GET"])
def user_signup():
    if request.method == "POST":
        email = request.form["Email"]
        password1 = request.form["Password1"]
        password2 = request.form["Password2"]

        def loginError(errorMsg):
            render_template ('base.html')
            return render_template("userSignUp.html",
                PageName = "Sign Up",  
                errorMsg = errorMsg     
            )

        if len(email) < 5:
            loginError("Invalid email")
        elif len(email) > 100:
            loginError("Invalid email")
        elif not "@" in email or not "." in email:
            loginError("Invalid email")
        elif len(password1) < 8:
            loginError("Password too short!" )
        elif len(password1) > 20:
            loginError("Password too long!")
        elif password1 != password2:
            loginError("Passwords must match!")

        connection = sql.connect(DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute(f'''INSERT INTO users (email, password, clearenceLevel) 
                            VALUES("{email}", "{password1}", 0)''')
        connection.commit()
        connection.close()

        return redirect(url_for('user_confirmed'))
    else:
        render_template ('base.html')
        return render_template("userSignUp.html",
            PageName = "Sign Up"        
        )


   

# User Sign In
@app.route('/UserSignIn',methods=["POST", "GET"])
def user_signin():
    if request.method == "POST":
        email = request.form["Email"]
        password = request.form["Password"]

        def loginError(errorMsg):
            render_template ('base.html')
            return render_template("userSignIn.html",
                PageName = "Sign in",  
                errorMsg = errorMsg     
            )

        connection = sql.connect(DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM users WHERE email = "{email}"')
        result = cursor.fetchall()
        if not result or not result[0]:
            loginError("Incorrect username!")
        cursor.execute(f'SELECT * FROM users WHERE email = "{email} & password = {password}"')
        result = cursor.fetchall()
        if not result or not result[0]:
            loginError("Incorrect password!")

        connection.commit()
        connection.close()


        session["user"] = email
        return redirect(url_for('index'))
    else:
        if "user" in session:
            return redirect(url_for("user_logout_confirmation"))
        else:
            render_template ('base.html')
            return render_template("userSignIn.html",
                PageName = "Sign in"
            )

# User Sign Out
@app.route('/LogoutConfirmation')
def user_logout_confirmation():
    render_template ('base.html')
    return render_template("logoutConfirmation.html",
        PageName = "Logout Confirmation",
        email = session["user"]
    )

# User Sign Out
@app.route('/UserLogout')
def user_logout():
    session.pop("user", None)
    return redirect(url_for("user_signin"))

# User Confirmed
@app.route('/UserConfirmed')
def user_confirmed():
    render_template ('base.html')
    return render_template("userConfirmed.html",
        PageName = "UserConfirmed"
    )

# Login Required
@app.route('/LoginRequired')
def require_signIn():
    render_template ('base.html')
    return render_template("loginRequired.html",
        PageName = "Login Required"
    )

# Employee Only
@app.route('/EmployeesOnly')
def require_employee_clearence():
    render_template ('base.html')
    return render_template("employeesOnly.html",
        PageName = "Login Required"
    )


# Employee Page
@app.route ('/Employees')
def employee_homepage():
    if not isAccountAdmin():
        return redirect(url_for("require_employee_clearence"))

    render_template ('base.html')
    return render_template("workersHomepage.html",
        PageName = "Employee",
    )


# View Inventory - added all books 
@app.route('/ViewInventory')
def view_inventory():
    if not isAccountAdmin():
        return redirect(url_for("require_employee_clearence"))

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

# Default search page for finding all
@app.route('/SearchAll')
def default_book_search():
    connection = sql.connect(DATABASE_NAME)
    cursor = connection.cursor()
    
    cursor.execute(f'SELECT * FROM books')
    bookData = cursor.fetchall()
    connection.commit()
    connection.close()

    books = []
    i = 0
    for book in bookData:
        bookDict = {
            "title" : book[1],
            "author" : book[2],
            "imageName" : "/static/" + book[6],
        }
        books.insert(i, bookDict)
        i += 1

    render_template ('base.html')
    return render_template("search.html",
        PageName = "Search",
        books = books
    )

# Search page
@app.route('/Search', methods=["POST", "GET"])
def book_search():
    bookName = request.form["search"]
    connection = sql.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM books WHERE title LIKE "%{bookName}%"')
    bookData = cursor.fetchall()
    connection.commit()
    connection.close()

    books = []
    i = 0
    for book in bookData:
        bookDict = {
            "title" : book[1],
            "author" : book[2],
            "imageName" : "/static/" + book[6],
        }
        books.insert(i, bookDict)
        i += 1

    render_template ('base.html')
    return render_template("search.html",
        PageName = "Search",
        books = books
    )


# View Purchases
@app.route('/ViewPurchases', methods=['GET'])
def view_purchases():
    if not isAccountAdmin():
        return redirect(url_for("require_employee_clearence"))
    
    connection = create_connection()
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM purchases")
        purchases = cursor.fetchall()
    return render_template("viewPurchases.html", PageName="Purchases", purchases=purchases)


if __name__ == '__main__':
    app.run()

    