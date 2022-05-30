from flask import Flask, Blueprint, render_template, url_for, abort, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager, login_required, current_user
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin





db = SQLAlchemy()
DB_NAME = "database.db"

class MicroBlogModelView(ModelView):
    edit_template = 'microblog_edit.html'
    create_template = 'microblog_create.html'
    list_template = 'microblog_list.html'
    details_template = 'microblog_details.html'
    edit_modal_template = 'microblog_edit_modal.html'
    create_modal_template = 'microblog_create_modal.html'
    details_modal_template = 'microblog_details_modal.html'

class MyView(BaseView):
     def is_visible(self):
         return False
     @expose('/')
     def index(self):
        return self.render('index.html')
        

class SecuredModelView(ModelView):
    column_labels = dict(firstname='Adı', lastname='Soyadı', password='Şifre(Hash256)')
    def is_accessible(self):
        if current_user.is_authenticated == True:
            if current_user.id == 1:
                return True
            else:
                abort(403)
        else:
            abort(403)



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Deucalion'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['FLASK_ADMIN_SWATCH'] = 'readable'
    db.init_app(app)

    admin = Admin(app, name='Yönetim', template_mode='bootstrap3')

    admin.add_view(SecuredModelView(user, db.session, name='Kullanıcılar'))
   


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    

   

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view ='auth.login'
    login_manager.login_message = ('Sayfayı görebilmek için giriş yapmalısınız.')
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return user.query.get(int(id))




    @app.errorhandler(403)
    def forbidden_access(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def forbidden_access(error):
        return render_template('404.html'), 404        





            




    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database oluşturuldu')


class user(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    password = db.Column(db.String(150))


class Crypto(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date(), unique=True)
    Open = db.Column(db.Float(50))
    High = db.Column(db.Float(50))
    Low = db.Column(db.Float(150))
    Close = db.Column(db.Float(150))
    Volume = db.Column(db.Float(150))
    Adj_Close = db.Column(db.Float(150))


    