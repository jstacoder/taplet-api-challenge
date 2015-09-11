import flask
import os
import gevent
import redis
import json
from markdown import markdown as md
from flask import views
from db import Photo

from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

redis = redis.Redis() if os.environ.get('REDIS_URL',None) is None else redis.from_url(os.environ.get('REDIS_URL'))

def event_stream(item_id=None):
    channel = 'list_view' if item_id is None else 'list_view_{0}'.format(item_id)
    pubsub = redis.pubsub()
    pubsub.subscribe(channel)

    for itm in pubsub.listen():
        yield itm




api = flask.Blueprint('api',__name__,url_prefix='/api/v1')

def api_index():
    return flask.make_response(md(open('README.md','r').read()))

api.add_url_rule('/','index',view_func=api_index)

class UploadView(views.MethodView):
    def post(self):
        data = dict(flask.request.form.items())
        user_id = data.get('user_id',None)
        group_id = data.get('group_id',None)
        image_url = data.get('image_url',None)

        photo = Photo(image_url=image_url,user_id=user_id,group_id=group_id).save()

        redis.publish('list_view',photo.to_json())
        redis.publish('list_view_{0}'.format(group_id),photo.to_json())

        rtn = flask.make_response(
                json.dumps(
                    dict(
                        image_url = photo.image_url,       
                        user_id = photo.user_id,
                        group_id = photo.group_id,
                        views = photo.views,
                    )
                )
        )
        rtn.headers['Content-type'] = 'application/json'
        return rtn

class StreamView(views.MethodView):
    def get(self,item_id=None):
        return flask.Response(event_stream(item_id),mimetype='text/event-stream')

class ListView(views.MethodView):
    def get(self,item_id=None):
        if item_id is None:
            # list entire table
            rtn = [x.to_json() for x in Photo.get_all()]
            for itm in rtn:
                redis.publish('list_view',itm)
        else:
            rtn = [x.to_json() for x in Photo.get_all() if x.group_id == item_id]
            for itm in rtn:
                redis.publish('list_view_{0}'.format(item_id),itm)
        res = flask.make_response(json.dumps(rtn))
        res.headers['Content-Type'] = 'application/json'
        return res

class ViewView(views.MethodView):
    def get(self,item_id):
        photo = Photo.get(item_id)
        if photo is not None:
            photo.add_view()            
            rtn = flask.make_response(json.dumps(photo.to_json()))
        rtn = flask.make_response(json.dumps(dict(error='photo with id:{0} was not found'.format(item_id))))
        rtn.headers['Content-Type'] = 'application/json'
        return rtn

api.add_url_rule('/upload','upload',view_func=UploadView.as_view('upload'))
api.add_url_rule('/upload/','upload2',view_func=UploadView.as_view('upload'))
api.add_url_rule('/list','list2',view_func=ListView.as_view('list'))
api.add_url_rule('/list/','list',view_func=ListView.as_view('list'))
api.add_url_rule('/list/<int:item_id>','list_group2',ListView.as_view('list_group'))
api.add_url_rule('/list/<int:item_id>/','list_group',ListView.as_view('list_group'))
api.add_url_rule('/view/<int:item_id>','view_item2',view_func=ViewView.as_view('view_item'))
api.add_url_rule('/view/<int:item_id>/','view_item',view_func=ViewView.as_view('view_item'))
api.add_url_rule('/stream/<int:item_id>','stream_view',view_func=StreamView.as_view('stream_view'))
api.add_url_rule('/stream/<int:item_id>/','stream_view2',view_func=StreamView.as_view('stream_view2'))
api.add_url_rule('/stream','stream',view_func=StreamView.as_view('stream'))
api.add_url_rule('/stream/','stream2',view_func=StreamView.as_view('stream'))

app = flask.Flask(__name__)
app.register_blueprint(api)

def index():
    return flask.render_template('index.html')

app.add_url_rule('/','index',view_func=index)

if __name__ == "__main__":
    port = int(os.environ.get('PORT') or 5555)
    #app.run(debug=True,host='0.0.0.0',port=port)
    WSGIServer(('0.0.0.0', port), app).serve_forever()
