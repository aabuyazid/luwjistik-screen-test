import json
from flask import Flask, Request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


# Creating an API using a Flask Application
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}), views={views}, likes={likes})"


# Run this line once        
# db.create_all()

debug = True

names = {
    "arkan":    {"age": 23, "gender": "male"},
    "bill":     {"age": 12, "gender": "male"}     
}

# Instantiating the argument parser for video put request
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f'Could not find video with id {video_id}')
        return result
        
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        
        if VideoModel.query.filter_by(id=video_id).first():
            abort(409, message='Video id taken')

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f'Could not find video with id {video_id}')

        for k in args:
            if args[k]:
                setattr(result, k, args[k])

        db.session.commit()

        return result

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f'Could not find video with id {video_id}')
        VideoModel.query.filter_by(id=video_id).delete()
        db.session.commit()
        return '', 204

# Defining resource
class HelloWorld(Resource):
    def get(self, name):
        return names[name]

    def post(self):
        return {"data": "posted"}


# Adding resource to the API accessible at "/helloworld"
# Angle brackes "<>" allows parameter passing
api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:video_id>")


        
if __name__ == "__main__":
    app.run(debug=debug)
