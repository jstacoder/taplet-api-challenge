import flask
from flask import views
from .db import Photo

api = flask.Blueprint('api',__name__,url_prefix='/api/v1')

class UploadView(views.MethodView):
    def post(self):
        data = flask.request.form.items()
        user_id = data.get('user_id',None)
        group_id = data.get('group_id',None)
        image_url = data.get('image_url',None)

        photo = Photo(image_url=image_url,user_id=user_id,group_id=group_id).save()
        return flask.jsonify(
            result = flask.json.dumps( 
                image_url = photo.image_url,       
                user_id = photo.user_id,
                group_id = photo.group_id,
                views = 0,
            )
        )

class ListView(views.MethodView):
    def get(self,item_id=None):
        pass

class ViewView(views.MethodView):
    def get(self,item_id=None):
        pass

api.add_url_rule('/upload','upload',view_func=UploadView.as_view('upload'))
api.add_url_rule('/list/','list',view_func=ListView.as_view('list'))
api.add_url_rule('/list/<int:item_id>/','list_group',ListView.as_view('list_group'))
api.add_url_rule('/view/','view',view_func=ViewView.as_view('view'))
api.add_url_rule('/view/<int:item_id>/','view_item',view_func=ViewView.as_view('view_item'))


if __name__ == "__main__":
    app = flask.Flask(__name__)
    app.register_blueprint(api)
    port = int(os.environ.get('PORT') or 5555)
    app.run(debug=True,host='0.0.0.0',port=port)


        
