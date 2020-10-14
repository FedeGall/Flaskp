# import os
# from datetime import datetime
# from dotenv import load_dotenv
# from redis import Redis
# from slugify import slugify

# from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
# from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
# from wtforms.widgets import TextArea
# from wtforms.validators import DataRequired, Length, Email
# from flask_wtf.csrf import CSRFProtect
# from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
# from flask_sslify import SSLify
# from flask_admin import Admin, AdminIndexView
# from flask_admin.contrib import rediscli
# from flask_admin.contrib.sqla import ModelView
# from flask_admin.menu import MenuLink
# from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
# from flask_migrate import Migrate
# from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
# from werkzeug.security import generate_password_hash, check_password_hash

# load_dotenv()

# app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['FLASK_APP'] = os.getenv("FLASK_APP")
# app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['FLASK_ADMIN_SWATCH'] = "simplex"
# app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flasky.sqlite')
# app.config['IFRAMELY_API_KEY'] = os.getenv('IFRAMELY_API_KEY')
# app.config['CKEDITOR_ENABLE_CSRF'] = True
# app.config['CKEDITOR_FILE_UPLOADER'] = "upload"
# app.config['UPLOADED_PATH'] = os.path.join(basedir, 'uploads')

# bootstrap = Bootstrap(app)
# moment = Moment(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# ckeditor = CKEditor(app)
# csrf = CSRFProtect(app)
# sslify = SSLify(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class User(UserMixin, db.Model):
#     __tablename__ = 'Users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.Unicode(64), unique=True, index=True)
#     email = db.Column(db.Unicode(64))
#     password_hash = db.Column(db.String(128))
#     created_at = db.Column(db.DateTime, default=datetime.now)
#     role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'))
#     post_author_id = db.relationship('Post', backref='post_author', lazy='dynamic')
#     project_author_id = db.relationship('Project', backref='project_author', lazy='dynamic')

#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')

#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def __unicode__(self):
#         return self.username
    
#     def __repr__(self):
#         return self.username

# class Role(db.Model):
#     __tablename__ = 'Roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Unicode(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')

#     def __unicode__(self):
#         return self.name
    
#     def __repr__(self):
#         return self.name

# class Post(db.Model):
#     __tablename__ = 'Posts'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.Unicode(64))
#     body = db.Column(db.UnicodeText)
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     post_author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
#     slug = db.Column(db.String(80), unique=True)

#     def __unicode__(self):
#         return self.title

# class Project(db.Model):
#     __tablename__ = 'Projects'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.Unicode(64))
#     body = db.Column(db.UnicodeText)
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     project_author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
#     slug = db.Column(db.String(80), unique=True)

#     def __unicode__(self):
#         return self.title

# class PostView(ModelView):
#     form_overrides = dict(body=CKEditorField)
#     create_template = 'edit_page.html'
#     edit_template = 'edit_page.html'
#     can_export = True
#     column_default_sort = ('timestamp', True)

#     def on_model_change(self, form, model, is_created):
#         if is_created and not model.slug:
#             model.slug = slugify(model.title)

#     def is_accessible(self):
#         return current_user.is_authenticated

# class ProjectView(ModelView):
#     form_overrides = dict(body=CKEditorField)
#     create_template = 'edit_page.html'
#     edit_template = 'edit_page.html'
#     can_export = True
#     column_default_sort = ('timestamp', True)

#     def on_model_change(self, form, model, is_created):
#         if is_created and not model.slug:
#             model.slug = slugify(model.title)

#     def is_accessible(self):
#         return current_user.is_authenticated

# class CustomModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated

# class CustomAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.is_authenticated

#     def inaccessible_callback(self, username, **kwargs):
#         return redirect(url_for('login'))

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Keep me logged in')
#     submit = SubmitField('Login')

# admin = Admin(app, name='Flasky ADM', template_mode='bootstrap4', index_view=CustomAdminIndexView())
# admin.add_view(CustomModelView(User, db.session))
# admin.add_view(CustomModelView(Role, db.session))
# admin.add_view(PostView(Post, db.session, name="Post", endpoint="post"))
# admin.add_view(ProjectView(Project, db.session, name="Project", endpoint="project"))
# # admin.add_view(rediscli.RedisCli(Redis()))
# admin.add_link(MenuLink(name='Home', url='/', category='Live Site'))
# admin.add_link(MenuLink(name='About', url='/about', category='Live Site'))
# admin.add_link(MenuLink(name='Blog', url='/blog', category='Live Site'))
# admin.add_link(MenuLink(name='Projects', url='/projects', category='Live Site'))

# @app.route('/')
# def index():
#     return render_template('index.html', current_time=datetime.utcnow())

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/blog')
# def blog():
#     page = request.args.get('page', 1, type=int)
#     pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=5)
#     posts = pagination.items
#     return render_template('blog.html', posts=posts, pagination=pagination)

# @app.route('/blog/<slug>')
# def post(slug):
#     post = Post.query.filter_by(slug=slug).first()
#     post_edit_url = url_for('post.edit_view', id=post.id)
#     if post:
#         return render_template("post.html", post=post, post_edit_url=post_edit_url)

# @app.route('/projects')
# def projects():
#     page = request.args.get('page', 1, type=int)
#     pagination = Project.query.order_by(Project.timestamp.desc()).paginate(page, per_page=5)
#     projects = pagination.items
#     return render_template('projects.html', projects=projects, pagination=pagination)

# @app.route('/projects/<slug>')
# def project(slug):
#     project = Project.query.filter_by(slug=slug).first()
#     project_edit_url = url_for('project.edit_view', id=project.id)
#     if post:
#         return render_template("project.html", project=project, project_edit_url=project_edit_url)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is not None and user.verify_password(form.password.data):
#             login_user(user, form.remember_me.data)
#             next = request.args.get('next')
#             if next is None or not next.startswith('/'):
#                 next = url_for('index')
#             return redirect(next)
#         flash('Invalid username or password.')
#     return render_template('login.html', form=form)

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('You have been logged out.')
#     return redirect(url_for('index'))

# @app.route('/files/<filename>')
# def uploaded_files(filename):
#     path = app.config['UPLOADED_PATH']
#     return send_from_directory(path, filename)

# @app.route('/upload', methods=['POST'])
# def upload():
#     f = request.files.get('upload')
#     extension = f.filename.split('.')[-1].lower()
#     if extension not in ['jpg', 'gif', 'png', 'jpeg']:
#         return upload_fail(message='Image only!')
#     f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
#     url = url_for('uploaded_files', filename=f.filename)
#     return upload_success(url=url)

# @app.errorhandler(403)
# def forbidden(e):
#     return render_template('403.html'), 403

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500

# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Role=Role, Post=Post, Project=Project)

# @app.cli.command("test")
# def test():
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)

# if __name__ == '__main__':
#     app.run(debug=True)
