import magic
import os
import requests
import yara
import tempfile


from flask import Flask, request, jsonify, json
from flask import Response

app = Flask(__name__)

rules = yara.compile(filepaths={
    'pdf_rules': '/app/yararules/pdf_rules.yara'
    })

TYPE_LOOKUP = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/tiff",
}

with open(os.getenv(
    'CONFIG_PATH', '/app/config/config.json')) as config_data:
    config = json.load(config_data)

api_key = config["APIKEY"]

"""
  receives file, processes with YARA ruleset
"""
@app.route('/file-upload', methods=['POST'])
def upload_file():
    headers = request.headers
    auth = headers.get("X-Api-Key")

    if auth == api_key:
        if 'file' not in request.files:
                return Response(json.dumps({'message' : 'No file provided'}), status=400, mimetype='application/json')
        content = request.files['file'].read()

        if not content:
            return Response(json.dumps({'message' : 'No file provided'}), status=400, mimetype='application/json')

        # write file content to temp file
        temp = tempfile.NamedTemporaryFile(suffix='_suffix', prefix='prefix_', dir='/tmp')
        temp.write(content)

        mime = magic.Magic(mime=True)
        file_type = mime.from_file(temp.name)

        if file_type not in TYPE_LOOKUP:
            temp.close()
            return Response(json.dumps({'message' : 'Incorrect file type'}), status=400, mimetype='application/json')

        # check yara for malicious files
        matches = rules.match(data=open(temp.name,"rb").read())

        if matches:
            temp.close() # for now close, until we know what we want to do with them
            return Response(json.dumps({'message' : 'Malicious file detected'}), status=500, mimetype='application/json')

        if not matches:
            temp.close()
            return Response(json.dumps({'message' : 'File OK'}), status=200, mimetype='application/json')

    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
