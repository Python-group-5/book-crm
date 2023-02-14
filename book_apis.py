from models import *
from flask import json
from flask import request


@app.route('/api/book', methods=['POST'])    #http://localhost:5000/api/book -->endpoint
def add_book():
    jsondata = request.get_json()
    all_parameter_names = jsondata.keys()
    required_parameter=["BOOK_NAME","BOOK_LANGUAGE","BOOK_CATEGORY","BOOK_WRITTER",
                        "BOOK_PUBLICATION","BOOK_QUANTITY","BOOK_WEIGHT","BOOK_PRICE"]

    for parameter in required_parameter:
        if parameter not in all_parameter_names:
            return json.dumps({"ERROR":"{} Parameter Is Required".format(parameter)})

    qty=jsondata.get("BOOK_QUANTITY")
    try:
        qty = int(qty)
        if qty<=0:
            return json.dumps({"ERROR":"INVALID BOOK QUANTITY"})
    except:
        return json.dumps({"ERROR":"BOOK QUANTITY SHOULD BE INTEGER"})

    wgt=jsondata.get("BOOK_WEIGHT")
    try:
        wgt=int(wgt)
        if wgt<=0:
            return json.dumps({"ERROR":"INVALID BOOK WEIGHT"})
    except:
        return json.dumps({"ERROR":"BOOK WEIGHT SHOULD BE INTEGER"})

    prc=jsondata.get("BOOK_PRICE")
    try:
        prc=int(prc)
        if prc<=0:
            return json.dumps({"ERROR":"INVALID BOOK PRICE"})
    except:
        return json.dumps({"ERROR":"BOOK PRICE SHOULD BE INTEGER"})

    book=Book(name=jsondata.get("BOOK_NAME"),language=jsondata.get("BOOK_LANGUAGE"),
            category=jsondata.get("BOOK_CATEGORY"),writter=jsondata.get("BOOK_WRITTER"),
            publication=jsondata.get("BOOK_PUBLICATION"),quantity=jsondata.get("BOOK_QUANTITY"),
            weight=jsondata.get("BOOK_WEIGHT"),price=jsondata.get("BOOK_PRICE"))
    db.session.add(book)
    db.session.commit()

    return json.dumps({"SUCCESS":"BOOK IS ADDED SUCCESSFULLY {}".format(book.id)})


@app.route('/api/book',methods=['GET'])
def list_book():
    book=Book.query.filter().all()
    if book:
        list_book = []
        for record in book:
            bk = ({"BOOK_ID": record.id,
                   "BOOK_NAME": record.name,
                   "BOOK_LANGUAGE": record.language,
                   "BOOK_CATEGORY": record.category,
                   "BOOK_WRITTER": record.writter,
                   "BOOK_PUBLICATION": record.publication,
                   "BOOK_QUANTITY": record.quantity,
                   "BOOK_WEIGHT": record.weight,
                   "BOOK_PRICE": record.price
                   })
            list_book.append(bk)
        return json.dumps(list_book, indent=4, sort_keys=False)
    else:
        return json.dumps({"ERROR": "NO BOOKS AVAILABLE"})



@app.route('/api/book/update/<int:bid>',methods=['POST'])
def update_book(bid):
    book=Book.query.filter_by(id=bid).first()
    if book:
        jsondata=request.get_json()
        book.name = jsondata.get("BOOK_NAME")
        book.price = jsondata.get("BOOK_PRICE")
        book.publication = jsondata.get("BOOK_PUBLICATION")
        book.writter = jsondata.get("BOOK_WRITTER")
        book.weight = jsondata.get("BOOK_WEIGHT")
        book.language = jsondata.get("BOOK_LANGUAGE")
        book.category = jsondata.get("BOOK_CATEGORY")
        book.quantity = jsondata.get("BOOK_QUANTITY")
        db.session.commit()
        return json.dumps({"SUCCESS":"BOOK IS UPDATED WITH GIVEN ID {}".format(bid)})

@app.route('/api/book/<int:bid>',methods=['GET'])
def search_book_by_id(bid):
    if bid<=0:
        return json.dumps({"ERROR": "INVALID BOOK ID"})
    book=Book.query.filter_by(id=bid).first()
    if book:
        return json.dumps({"BOOK_NAME": book.name,"BOOK_LANGUAGE": book.language,"BOOK_CATEGORY": book.category,
                           "BOOK_WRITTER": book.writter,"BOOK_PUBLICATION": book.publication,
                           "BOOK_QUANTITY": book.quantity,"BOOK_WEIGHT": book.weight,"BOOK_PRICE": book.price})
    else:
        return json.dumps({"ERROR":"NO BOOK WITH GIVEN ID {}".format(bid)})


@app.route('/api/book/soft-delete/<int:bid>',methods=['DELETE'])
def soft_delete_book(bid):
    book = Book.query.filter_by(id=bid).first()
    if book:
        book.isactive='Y'
        db.session.commit()
        return json.dumps({"SUCCESS": "BOOK IS DELETED WITH GIVEN BOOK ID {}".format(bid)})
    else:
        return json.dumps({"ERROR": "INVALID BOOK ID {}".format(bid)})

@app.route('/api/book/hard-delete/<int:bid>',methods=['DELETE'])
def hard_delete_book(bid):
    book=Book.query.filter_by(id=bid).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return json.dumps({"SUCCESS":"BOOK IS DELETED WITH GIVEN BOOK ID {}".format(bid)})
    else:
        return json.dumps({"ERROR":"INVALID BOOK ID {}".format(bid)})
@app.route('/api/book/delete/<int:bid>', methods=['DELETE'])           #http://localhost:5000/api/book/{}  -->DELETE
def delete_book(bid):
    if type(bid) == int and bid>=0:
        book=Book.query.filter_by(id=bid).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return json.dumps({"SUCCESS":"BOOK ID IS DELETED"})
        else:
            return json.dumps({"ERROR": "No PRODUCT WITH GIVEN BOOK ID {}".format(bid)})
    else:
        return json.dumps({"EOOR":"BOOK ID SHOULD BE INTEGER AND NON ZERO"})


@app.route('/api/book/name/<name>',methods=['GET'])
def search_book_by_name(name):
    book = Book.query.filter(Book.name == name).all()
    if book:
        list_book = []
        for record in book:
            bk = ({"BOOK_ID": record.id,
                   "BOOK_NAME": record.name,
                   "BOOK_LANGUAGE": record.language,
                   "BOOK_CATEGORY": record.category,
                   "BOOK_WRITTER": record.writter,
                   "BOOK_PUBLICATION": record.publication,
                   "BOOK_QUANTITY": record.quantity,
                   "BOOK_WEIGHT": record.weight,
                   "BOOK_PRICE": record.price
                   })
            list_book.append(bk)
        return json.dumps(list_book, indent=4, sort_keys=False)
    else:
        return json.dumps({"ERROR": "NO BOOK WITH GIVEN BOOK NAME {}".format(name)})


@app.route('/api/book/category/<ctname>',methods=['GET'])
def list_book_by_category(ctname):
    book = Book.query.filter(Book.category == ctname).all()
    if book:
        list_book = []
        for record in book :
            bk=({"BOOK_ID":record.id,
                 "BOOK_NAME": record.name,
                 "BOOK_LANGUAGE": record.language,
                 "BOOK_CATEGORY": record.category,
                 "BOOK_WRITTER": record.writter,
                 "BOOK_PUBLICATION": record.publication,
                 "BOOK_QUANTITY": record.quantity,
                 "BOOK_WEIGHT": record.weight,
                 "BOOK_PRICE": record.price
                 })
            list_book.append(bk)
        return json.dumps(list_book,indent=4,sort_keys=False)
    else:
        return json.dumps({"ERROR": "NO BOOK WITH GIVEN BOOK CATEGORY {}".format(ctname)})


@app.route('/api/book/language/<lname>', methods=['GET'])
def list_book_by_language(lname):
    book = Book.query.filter(Book.language==lname).all()
    if book:
        list_book = []
        for record in book:
            bk=({"BOOK_ID":record.id,
                "BOOK_NAME": record.name,
                 "BOOK_LANGUAGE": record.language,
                 "BOOK_CATEGORY": record.category,
                 "BOOK_WRITTER": record.writter,
                 "BOOK_PUBLICATION": record.publication,
                 "BOOK_QUANTITY": record.quantity,
                 "BOOK_WEIGHT": record.weight,
                 "BOOK_PRICE": record.price
                 })
            list_book.append(bk)
        return json.dumps(list_book,sort_keys=False)
    else:
        return json.dumps({"ERROR":"NO BOOK WITH GIVEN BOOK LANGUAGE {}".format(lname)})


@app.route('/api/book/writter/<wname>',methods=['GET'])
def book_by_writter(wname):
    book=Book.query.filter(Book.writter==wname).all()
    if book:
        list_book=[]
        for record in book:
            bk=({"BOOK_ID":record.id,
                "BOOK_NAME": record.name,
                 "BOOK_LANGUAGE": record.language,
                 "BOOK_CATEGORY": record.category,
                 "BOOK_WRITTER": record.writter,
                 "BOOK_PUBLICATION": record.publication,
                 "BOOK_QUANTITY": record.quantity,
                 "BOOK_WEIGHT": record.weight,
                 "BOOK_PRICE": record.price
                 })
            list_book.append(bk)
        return json.dumps(list_book)
    else:
        return json.dumps({"ERROR":"NO BOOK WITH THIS BOOK WRITTER {}".format(wname)})



@app.route('/api/book/publication/<pubname>',methods=['GET'])
def search_by_publication(pubname):
    book=Book.query.filter(Book.publication==pubname)
    if book:
        list_book=[]
        for record in book:
            bk = ({"BOOK_ID": record.id,
                   "BOOK_NAME": record.name,
                   "BOOK_LANGUAGE": record.language,
                   "BOOK_CATEGORY": record.category,
                   "BOOK_WRITTER": record.writter,
                   "BOOK_PUBLICATION": record.publication,
                   "BOOK_QUANTITY": record.quantity,
                   "BOOK_WEIGHT": record.weight,
                   "BOOK_PRICE": record.price
                   })
            list_book.append(bk)
        return json.dumps(list_book)
    else:
        return json.dumps({"ERROR":"NO BOOK WITH THIS BOOK PUBLICATION {}".format(pubname)})


@app.route('/api/user',methods=['POST'])
def userinfo():
    jsondata=request.get_json()
    all_parameter=jsondata.keys()
    required_parameter=["USER_NAME","USER_PASSWORD","USER_EMAIL"]
    for parameter in required_parameter:
        if parameter not in all_parameter:
            return json.dumps({"ERROR":"INSUFFICIENT DATA"})
        user=Userinfo(username=jsondata.get("USER_NAME"),userpassword=jsondata.get("USER_PASSWORD"),
                      useremail=jsondata.get("USER_EMAIL"))
        db.session.add(user)
        db.session.commit()
        return json.dumps({"SUCCESS":"USERINFO IS ADDED SUCCESSFULLY{}".format(user.userid)})


@app.route('/api/user',methods=['GET'])
def list_userinfo():
    users=Userinfo.query.all()
    if users:
        list_user=[]
        for item in users:
            ui=({"USER_ID": item.userid,
                 "USER_NAME":item.username,
                 "USER_PASSWORD":item.userpassword,
                 "USER_EMAIL": item.useremail})
            list_user.append(ui)
        return json.dumps(list_user,sort_keys=False)
    else:
        return json.dumps({"ERROR":"USERINFO IS NOT AVAILABLE"})