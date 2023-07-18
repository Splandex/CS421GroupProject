from flask import Flask, render_template, request
app = Flask (__name__)

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
@app.route ('/Purchase/<bookName>')
def purchase_book(bookName):
    render_template ('base.html')
    return render_template("purchase.html",
        PageName = bookName,
        Author = "John Doe",
    )

# Purchase successful
@app.route ('/PurchaseSuccess')
def purchase_success():
    render_template ('base.html')
    return render_template("purchaseConfirmed.html",
        PageName = "Success",
    )


if __name__ == '__main__':
    app.run()