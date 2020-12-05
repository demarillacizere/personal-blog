from . import main
from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for,abort,flash
from ..models import User, Comment, Blog, Like, Dislike, Mail_list
from .forms import CommentForm, BlogForm, UpdateProfile, SubscribeForm
from .. import db, photos
import markdown2
from ..requests import get_quote
from ..email import mail_message

quotes = get_quote()

@main.route('/',methods = ['GET','POST'])
def index():
    blogs=Blog.query.order_by(Blog.posted.desc()).all()
    if blogs is None:
        abort (404) 
    for blog in blogs:
        format_blog = markdown2.markdown(blog.content,extras=["code-friendly", "fenced-code-blocks"])
    mail_form = SubscribeForm()
    if mail_form.validate_on_submit():
        email = mail_form.email.data
        name = mail_form.name.data
        new_user = Mail_list(email=email, name = name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('.index'))

    title="Shout out"
    return render_template('index.html', title = title,blogs=blogs, quotes=quotes, mail_form=mail_form)

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
    global new_blog
    if blog_form.validate_on_submit():
        title = blog_form.title.data
        body = blog_form.content.data
        title = blog_form.title.data
        new_blog = Blog(title=title, content=body, user = current_user)
        new_blog.save_blog()
        users = Mail_list.query.all()
        for user in users:
            if user is None:
                abort (404) 
            mail_message("New Post","email/alert_user",user.email,user=user)
            return redirect(url_for('main.index'))


    title = 'New blog'
    return render_template('new_blog.html', title = title, blogform = blog_form, new_blog=new_blog)

@main.route('/blog/<int:id>',methods = ['GET','POST'])
def blog(id):
    blog=Blog.query.get(id)
    if blog is None:
        abort(404)
    format_blog = markdown2.markdown(blog.content,extras=["code-friendly", "fenced-code-blocks"])
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data

        new_comment = Comment(comment=comment, blog_id = id)
        new_comment.save_comment()
        return redirect(url_for('.blog',id=id))

    comments = Comment.query.filter_by(blog_id=id).all()
    title = 'Post'

    return render_template('blog.html',blog = blog,format_blog=format_blog,comment_form = comment_form, comments = comments,title=title)

@main.route('/blog/<int:blog_id>/update',methods = ['GET','POST'])
@login_required
def update_post(blog_id):
    blog = Blog.query.get(blog_id)
    form = BlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('.blog',id=blog.id))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content
    return render_template('profile/update.html',form =form)

@main.route('/blog/<int:blog_id>/delete',methods = ['GET','POST'])
def delete(blog_id):
    '''
    View like function that returns likes
    '''
    blog = Blog.query.get(blog_id)
    blog.delete_blog()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.profile',uname=current_user.username))


@main.route('/comment/<int:comment_id>/delete',methods = ['GET','POST'])
def delete_com(comment_id):
    '''
    View like function that returns likes
    '''
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.blog',id=comment.blog_id))



@main.route('/blog/<int:blog_id>/like',methods = ['GET','POST'])
def like(blog_id):
    '''
    View like function that returns likes
    '''
    blog = Blog.query.get(blog_id)

    likes = Like.query.filter_by(blog_id=blog_id)


    if Like.query.filter(Like.blog_id==blog_id).first():
        return  redirect(url_for('.index'))

    new_like = Like(blog_id=blog_id)
    new_like.save_likes()
    return redirect(url_for('main.blog',id=blog_id))



@main.route('/blog/<int:blog_id>/dislike',methods = ['GET','POST'])
def dislike(blog_id):
    '''
    View dislike function that returns dislikes
    '''
    blog = Blog.query.get(blog_id)

    blog_dislikes = Dislike.query.filter_by(blog_id=blog_id)

    if Dislike.query.filter(Dislike.blog_id==blog_id).first():
        return redirect(url_for('main.index'))

    new_dislike = Dislike(blog_id=blog_id)
    new_dislike.save_dislikes()
    return redirect(url_for('main.blog',id=blog_id)) 
