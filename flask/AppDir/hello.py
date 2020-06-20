from flask import Flask, url_for, request, render_template, make_response, redirect, abort, escape, session, flash, get_flashed_messages
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def fn1():
    return 'This is home page.'


@app.route('/user<username>')
def fn2(username):
    return "fn2 arg is: %s" % username


@app.route('/user<int:user_id>')
def fn3(user_id):
    return "fn3 arg is: {}".format(user_id)


@app.route('/user<uname>_<uid>', methods=['GET', 'POST'])
def fn4(uname, uid):
    print("request.method: {}".format(request.method))
    return "fn4 args are: {}, {}".format(uname, uid)


@app.route('/rend_temp')
@app.route('/rend_temp<name>')
def fn5(name=None):
    resp = make_response(render_template('hello.html', name=name))
    resp.set_cookie('ABC', 'XYZ')
    return resp


@app.route('/form_test<any:s>', methods=['GET'])
def fn6(s):
    return "FORM DATA by {} method: {}, {}".format(request.method, request.args.get('user_fname'), request.args.get('user_lname'))
    

@app.route('/form_test', methods=['POST'])
def fn7():
    return "FORM DATA by {} method: {}, {}".format(request.method, request.form['user_fname'], request.form['user_lname'])


@app.route('/upload_test', methods=['POST'])
def fn8():
    f = request.files['uploaded_file']
    upload_folder = '/home/shahed/ShdHomeData/MyDraftWorks/TestFolder/'
    f.save(upload_folder + secure_filename(f.filename))
    return 'fn8 is called.'


@app.route('/redirect_test')
def fn9():
    print("fn9 is redirecting to fn1.")
    return redirect(url_for('fn1'))


@app.route('/errr')
def fn10():
    print('fn10 is called.')
    abort(404)
    

@app.errorhandler(404)
def page_is_not_found(error):
    return render_template('page_not_found_customized.html'), 404


## Session test ****************************************
# @app.route('/index')
# def index():
#     if 'username' in session:
#         return "Logged in as %s" % escape(session['username'])
#     return 'You are not logged in.'


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form method='POST'>
#             <input type='text', name='username' />
#             <input type='submit' value='Submit' />
#         </form>
#     '''


# @app.route('/logout')
# def logout():
#     session.pop('username', )
#     return redirect(url_for('index'))

# app.secret_key = 'seckey'

## session test done *************************************


# # message flashing test ***************************************
# app.secret_key = 'seckey'

# @app.route('/a')
# def fn_a():
#     print('fn_a is called')
#     flash('This message is flashed.')
#     print('flash() done')
#     return '''
#         <a href="{}" target="_blank">Go to fn_b</a>
#     '''.format(url_for('fn_b'))


# @app.route('/b')
# def fn_b():
#     print('fn_b is called.')
#     print("flashed msg is: {}".format(get_flashed_messages()))
#     return '''
#         <a href="{}" target="_blank">Go to fn_c</a>
#     '''.format(url_for('fn_c'))


# @app.route('/c')
# def fn_c():
#     print('fn_c is called.')
#     print("flashed msg is: {}".format(get_flashed_messages()))
#     return 'done.'

# # Message flashing test done *******************************


# with app.test_request_context():
#     print( url_for('fn1') )
#     print( url_for('fn1', v='xyz') )
#     print( url_for('fn2', username='abcdef') )
#     print( url_for('fn3', user_id=147))
#     print( url_for('fn4', uname='SHAHED', uid=777) )
#     print( url_for('static', filename='style.css') )


with app.test_request_context('/userSHAHED_777', method='POST'):
    assert request.path == '/userSHAHED_777'
    assert request.method == 'POST'
    print("Well done all assertions.")