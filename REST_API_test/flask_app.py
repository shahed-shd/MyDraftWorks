# Importing local modules.
import model

# Importing from python standard library.
import json
from http import HTTPStatus
import datetime

# Importing from flask
from flask import Flask, url_for, request, make_response

#Importing from apscheduler
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)


@app.route('/users', methods=['POST'])
def add_new_user():
    if request.method == 'POST':
        try:
            fname, lname, pw = request.form['firstName'], request.form['lastName'], request.form['password']
        except:
            return ('', HTTPStatus.BAD_REQUEST)

        try:
            new_user_id = model.add_user(fname, lname, pw)
            app.logger.debug('New user: {}, {}, {} with userid: {} added.'.format(fname, lname, pw, new_user_id))

            s = json.dumps({ "id": new_user_id })
            return (s, HTTPStatus.CREATED)
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        return HTTPStatus.METHOD_NOT_ALLOWED


@app.route('/users/<int:userid>', methods=['GET'])
def get_user_name_by_id(userid):
    if request.method == 'GET':
        name = model.get_user_name(userid)
        if name == None:
            return ('', HTTPStatus.NOT_FOUND)
        s = json.dumps({"id": userid, "name": name[0]+name[1]}, sort_keys=True, indent=4)
        return (s, HTTPStatus.OK)
    else:
        return HTTPStatus.METHOD_NOT_ALLOWED


@app.route('/users/<int:userid>/tags', methods=['POST'])
def add_tags(userid):
    if request.method == 'POST':
        json_obj = request.get_json()

        try:
            tag_list = json_obj['tags']
            expiry = json_obj['expiry']
        except:
            return ('', HTTPStatus.BAD_REQUEST)

        if type(tag_list) != list or type(expiry) != int:
            return ('', HTTPStatus.BAD_REQUEST)

        try:
            if model.add_tag(userid, tag_list, expiry):
                return ('', HTTPStatus.CREATED)
            else:
                return ('', HTTPStatus.INTERNAL_SERVER_ERROR)
        except:
            return ('', HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
        return ('', HTTPStatus.METHOD_NOT_ALLOWED)


@app.route('/users', methods=['GET'])
def get_users_by_tags():
    if request.method == 'GET':
        tags = request.args.get('tags')
        tag_list = tags.split(sep=',') if tags else []

        userid_list = model.get_userid_by_tags(tag_list)
        user_info_list = model.get_user_info_by_userids(userid_list)

        L = [{"id": userid, "name": fname+lname, "tags": tag_list} for userid, fname, lname, tag_list in user_info_list]
        s = json.dumps({"users": L}, sort_keys=True, indent=4)

        return (s, HTTPStatus.OK)
    else:
        return ('', HTTPStatus.METHOD_NOT_ALLOWED)


def periodically_do():
    '''It's called in a regular interval which is defined in scheduler.
    The duration of interval can be modified in scheduler.add_job().'''

    model.delete_expired_tags()


def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodically_do, 'interval', seconds=2*60*60)     # interval of 2 hours.

    scheduler.start()   # Now, expired tags will be checked and deleted in the regular interval.
    app.logger.debug("Scheduler started.")

    app.run(debug=True)

    scheduler.shutdown()
    app.logger.debug("Scheduler shutdown done.")


if __name__ == '__main__':
    main()
