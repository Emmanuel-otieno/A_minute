 
from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Pitch,Comment
from .. import db,photos
from .forms import UpdateProfile,PitchForm,CommentForm
from flask_login import login_required,current_user
import datetime

@main.route('/')
def index():

    title = 'Welcome to Pitches Site'
    interview_piches = Pitch.get_pitches('interview')
    product_piches = Pitch.get_pitches('product')
    promotion_pitches = Pitch.get_pitches('promotion')

    return render_template('index.html',title = title, interview = interview_piches, product = product_piches, promotion = promotion_pitches)

@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    pitches_count = Pitch.count_pitches(name)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,pitches = pitches_count,date = user_joined)

@main.route('/user/<name>/update',methods = ['GET','POST'])
@login_required
def update_profile(name):
    user = User.query.filter_by(username = name).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',name=user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',name=name))

@main.route('/pitch/new', methods = ['GET','POST'])
@login_required
def add_pitch():
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        pitch = pitch_form.text.data
        category = pitch_form.category.data
        new_pitch = Pitch(pitch_title=title,pitch_content=pitch,category=category,user=current_user,likes=0,dislikes=0)
        new_pitch.save_pitch()
        return redirect(url_for('main.index'))
    return render_template('new_pitch.html',title = title,pitch_form=pitch_form )

@main.route('/pitches/present_pitches')
def interview():

    pitches = Pitch.get_pitches('present')

    return render_template("present.html", pitches = pitches)

@main.route('/pitches/product_pitches')
def product():

    pitches = Pitch.get_pitches('product')

    return render_template("product.html", pitches = pitches)

@main.route('/pitches/advert_pitches')
def promotion():

    pitches = Pitch.get_pitches('advert')

    return render_template("advert.html", pitches = pitches)

@main.route('/pitch/<int:id>', methods = ['GET','POST'])
def pitch(id):
    pitch = Pitch.get_pitch(id)
    posted_date = pitch.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        pitch.likes = pitch.likes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("dislike"):
        pitch.dislikes = pitch.dislikes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,pitch_id = pitch)

        new_comment.save_comment()


    comments = Comment.get_comments(pitch)

    return render_template("pitch.html", pitch = pitch, comment_form = comment_form, comments = comments, date = posted_date)

@main.route('/user/<name>/pitches')
def user_pitches(name):
    user = User.query.filter_by(username=name).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    
    return render_template("profile/pitches.html", user=user,pitches=pitches)
