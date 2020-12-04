from . import main
from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for,abort
# from ..models import User, Comment, Pitch, Like, Dislike
# from .forms import CommentForm, PitchForm, UpdateProfile
from .. import db, photos

@main.route('/')
def index():
    title="Shout out"
    return render_template('index.html', title = title)