
from config import db,app

class Book(db.Model):
    id = db.Column('book_id',db.Integer(),primary_key=True)
    name = db.Column('book_name',db.String(50))
    language = db.Column('book_language',db.String(50))
    category = db.Column('book_category',db.String(50))
    writter = db.Column('book_writter',db.String(50))
    publication = db. Column('book_publication',db.String(50))
    quantity = db.Column('book_quantity',db.Integer())
    weight = db.Column('book_weight',db.Float())
    price = db.Column('book_price',db.Float())
    isactive=db.Column('is_deleted',db.String(255),default='N')
class Userinfo(db.Model):
    userid = db.Column('user_id',db.Integer(),primary_key=True)
    username = db.Column('User_name',db.String(50))
    userpassword = db.Column('user_password',db.String(50))
    useremail = db.Column('user_email',db.String(50),unique=True)
    userref = db.Column('u_id',db.ForeignKey('book.book_id'),unique=True)

    
with app.app_context():
    print('Create a Table')
    db.create_all()