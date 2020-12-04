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

        new_blog = Blog(title=title, content=body, category = category, user = current_user)
        new_blog.save_blog()

        return redirect(url_for('main.index'))


    title = 'New blog | One Minute blog'
    return render_template('new_blog.html', title = title, blogform = blog_form)

@main.route('/blog/<int:blog_id>/comment',methods = ['GET', 'POST'])
@login_required
def comment(blog_id):
    '''
    View comments page function that returns the comment page and its data
    '''

    comment_form = CommentForm()
    blog = Blog.query.get(blog_id)
    if blog is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data

        new_comment = Comment(comment=comment, blog_id = blog_id, user = current_user)
        new_comment.save_comment()

        return redirect(url_for('.comment', blog_id=blog_id))

    comments = Comment.query.filter_by(blog_id=blog_id).all()
    title = 'Comments | One Min blog'

    return render_template('comment.html', title = title, blog=blog ,comment_form = comment_form, comments = comments )





@main.route('/blog/<int:blog_id>/like',methods = ['GET','POST'])
def like(blog_id):
    '''
    View like function that returns likes
    '''
    blog = blog.query.get(blog_id)

    likes = Like.query.filter_by(blog_id=blog_id)


    if Like.query.filter(Like.blog_id==blog_id).first():
        return  redirect(url_for('.index'))

    new_like = Like(blog_id=blog_id)
    new_like.save_likes()
    return redirect(url_for('main.index'))



@main.route('/blog/<int:blog_id>/dislike',methods = ['GET','POST'])
def dislike(blog_id):
    '''
    View dislike function that returns dislikes
    '''
    blog = blog.query.get(blog_id)

    blog_dislikes = Dislike.query.filter_by(blog_id=blog_id)

    if Dislike.query.filter(Dislike.blog_id==blog_id).first():
        return redirect(url_for('main.index'))

    new_dislike = Dislike(blog_id=blog_id)
    new_dislike.save_dislikes()
    return redirect(url_for('main.index')) 
