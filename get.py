from flask import send_file
from io import BytesIO
from flask import Flask, request
import pymysql.cursors
import base64
import json

app = Flask(__name__)

@app.route('/getInfo', methods=['GET'])
def getInfo():
    id = request.args.get("id")
    picture = request.args.get("picture")
    confidence = request.args.get("confidence")

    # Connect to the database
    connection = pymysql.connect(host='192.168.56.222',
                                 user='root',
                                 password='root4321',
                                 db='fire',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            if id:
                cursor.execute("SELECT * FROM fire_information WHERE id=%s", (id,))
            elif picture:
                cursor.execute("SELECT * FROM fire_information WHERE picture=%s", (picture,))
            elif confidence:
                cursor.execute("SELECT * FROM fire_information WHERE confidence=%s", (confidence,))

            result = cursor.fetchone()
            if result and 'picture' in result and result['picture']:
                # Replace the picture data with a URL to the picture
                result['picture'] = 'http://localhost:8080/getImage?id=' + str(id)
                connection.commit()
            return json.dumps(result, ensure_ascii=False)

    finally:
        connection.close()

@app.route('/getImage', methods=['GET'])
def getImage():
    id = request.args.get("id")

    # Connect to the database
    connection = pymysql.connect(host='192.168.56.222',
                                 user='root',
                                 password='root4321',
                                 db='fire',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT picture FROM fire_information WHERE id=%s", (id,))
            result = cursor.fetchone()
            if result and 'picture' in result and result['picture']:
                img = base64.b64decode(result['picture'])
                return send_file(BytesIO(img), mimetype='image/jpg')
            else:
                return 'No image found', 404

    finally:
        connection.close()
