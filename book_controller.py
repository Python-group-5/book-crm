from models import *
from flask import render_template,request


@app.route('/')         #---> http://localhost:5000/
def welcome_page():
    return render_template("dashboard.html")

#database={'admin':'admin123','vijay':'vijay123'}

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        formdata = request.form
        username1=formdata.get('user_name')
        print(username1)
        userpassword1=formdata.get('user_password')
        print(userpassword1)
        try:
            userinfo=  Userinfo.query.filter_by(username=username1).first()
            massage='Invalid username and password'

            if userinfo.username == username1:
                if userinfo.userpassword == userpassword1:
                    return render_template('home.html')
                return render_template('login.html',massage=massage)
        except:
            return render_template('login.html',massage=massage)
    return render_template('login.html')


@app.route('/signup',methods=["POST"])
def register():
    if request.method == "POST":
        formdata = request.form
        errors=[]
        if not formdata.get('user_name'):
            errors.append('User name cannot be Empty')
        if not formdata.get('user_password'):
            errors.append('User Password Cannot Be Empty')
        if not formdata.get('user_email'):
            errors.append('User Email cannot be Empty')
        if errors:
            return render_template('signup.html',emassage=errors)
        massage = ""
        try:
            userinfo = Userinfo(username= formdata.get('user_name'),userpassword=formdata.get('user_password'),
                        useremail=formdata.get('user_email'))
            db.session.add(userinfo)
            db.session.commit()
        except:
            return render_template('signup.html', massage='already user present')

        return render_template('signup.html', masasge='Registration Successfull')

    return render_template('signup.html')
    # username1 = request.form['user_name']
    # password1 = request.form['user_password']
    # if username1 not in database:
    #     return render_template('login.html',massage='Invalid USer Name')
    # else:
    #     if database[username1]!=password1:
    #         return render_template('login.html',massage='Invalid Password')
    #     else:
    #         return render_template("home.html")

@app.route('/home',methods=['GET'])     #---> login page madhe submit page var click kelyanantr http://localhost:5000/welcome-page madhe jail
def home_page():
    return render_template('home.html')


@app.route('/add-book',methods=['GET'])         #---> http://localhost:5000/add-book
@app.route('/save-book', methods=['GET','POST'])    #--> http://localhost:5000/save-book
def add_book():
    if request.method == 'POST':
        formdata = request.form
        print(formdata)

        errors = []
        if not formdata.get('bookid'):
            errors.append("Book Id Cannot be Empty")
        if not formdata.get('bookname'):
            errors.append("Book Name Cannot be Empty")
        if not formdata.get('booklanguage'):
            errors.append("Book Language Cannot be Empty")
        if not formdata.get('bookcategory'):
            errors.append("Book Category Cannot be Empty")
        if not formdata.get('bookwritter'):
            errors.append("Book writter Cannot be Empty")
        if not formdata.get('bookpublication'):
            errors.append("Book Publication Cannot be Empty")
        if not formdata.get('bookquantity'):
            errors.append("Book Quantity Cannot be Empty")
        if not formdata.get('bookweight'):
            errors.append("Book weight Cannot be Empty")
        else:
            try:
                weight=float(formdata.get('bookweight'))
                if weight<=0:
                    errors.append("Book Weight should not zero")
            except:
                errors.append("Invalid Weight")
        if not formdata.get('bookprice'):
            errors.append("Book Price Cannot be Empty")
        else:
            try:
                price=float(formdata.get('bookprice'))
                if price<=0:
                    errors.append("Book Price should not be Negative")
            except:
                errors.append("Invalid Salary")

        if errors:
            return render_template('addbook.html',emassage=errors)
        book=Book(id=formdata.get('bookid'),name=formdata.get('bookname'),language=formdata.get('booklanguage'),
                  category=formdata.get('bookcategory'),writter=formdata.get('bookwritter'),
                  publication=formdata.get('bookpublication'),quantity=formdata.get('bookquantity'),
                  weight=formdata.get('bookweight'),price=formdata.get('bookprice'))
        db.session.add(book)
        db.session.commit()
        return render_template('addbook.html',massage='Book Added Successfully')
    return render_template('addbook.html')


def update_book():
    pass

@app.route('/delete-book/<int:bookid>')
def delete_book(bookid):
    book = Book.query.filter_by(id=bookid).first()
    db.session.delete(book)
    db.session.commit()
    return render_template('listbook.html',blist = Book.query.all())

@app.route('/list-book')
def list_book():
    return render_template('listbook.html',blist = Book.query.all())


def search_book():
    pass


def book_price_range():
    pass



