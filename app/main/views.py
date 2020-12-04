from . import main
from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for,abort
from ..models import User, Comment, Blog, Like, Dislike
from .forms import CommentForm, BlogForm, UpdateProfile
from .. import db, photos

@main.route('/')
def index():
    title="Shout out"
    return render_template('index.html', title = title)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    title = f"{uname.capitalize()}"

    if user is None:
        abort (404) 

    return render_template("profile/profile.html", user = user, title=title)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))



@main.route('/blog/new',methods = ['GET','POST'])
@login_required
def new_blog():
    '''
    A function that saves the blog added
    '''
    blog_form = BlogForm()

    if blog_form.validate_on_submit():
        title = blog_form.title.data
        body = blog_form.content.data
        category = blog_form.category.data
        title = blog_form.title.data

        new_blog = blog(title=title, content=body, category = category, user = current_user)
        new_blog.save_blog()

        return redirect(url_for('main.index'))


    title = 'New blog | One Minute blog'
    return render_template('new_blog.html', title = title, blogform = blog_f