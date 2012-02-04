__author__ = 'rbastian'

from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash
from flaskr import app
from models import Post
from google.appengine.api import users

@app.route('/')
def show_entries():
    user = users.get_current_user()
    if user:
        session['logged_in'] = True

    posts = Post.all()
    return render_template('show_entries.html', entries=posts)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    user = users.get_current_user()
    post = Post(email = user.email(), title=request.form['title'], content=request.form['text'])
    post.put()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # This is where I need to make changes...
    user = users.get_current_user()
    if user:
        session['logged_in'] = True
        flash('User is logged in: %s' % user.email())
        return redirect(url_for('show_entries'))
    else:
        return redirect(users.create_login_url("/"))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(users.create_logout_url(url_for('show_entries')))