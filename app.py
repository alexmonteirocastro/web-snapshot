from flask import Flask, render_template, make_response, request, jsonify, send_file
from flask_expects_json import expects_json
from jsonschema import ValidationError
from web_snapshot import get_web_snapshot

app = Flask(__name__)

schema = {
  "type": "object",
  "properties": {
    "url": {
        "type": "string",
        "minLength": 1,
        "pattern": "^(http[s]?:\\/\\/(www\\.)?|ftp:\\/\\/(www\\.)?|www\\.){1}([0-9A-Za-z-\\.@:%_\+~#=]+)+((\\.[a-zA-Z]{2,3})+)(/(.)*)?(\\?(.)*)?"
    },
  },
  "required": ["url"]
}

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/<name>")
def hello(name):
    return render_template('index.html', name=name)


@app.get('/web-snapshot/<string:url>')
def get_snapshot(url):
    return render_template('index.html', url=url)


@app.post('/web-snapshot/')
@expects_json(schema)
def make_snapshot():
    request_data = request.get_json()
    page = request_data['url']
    snapshot = get_web_snapshot(page)
    print(snapshot)
    if snapshot is None:
        return make_response(jsonify({
            'error': 'Not possible to generate snapshot. Make sure you provide a valid URL.'
        }), 400)

    if '.png' not in snapshot:
        err: 'Nope'
        return make_response(jsonify({
            'error': snapshot
        }), 400)

    return send_file(snapshot, mimetype='image/gif')


@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    # handle other "Bad Request"-errors
    return error


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)

