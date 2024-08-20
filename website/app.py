from flask import Flask
from views import views, view2

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
app.register_blueprint(view2, name="view2", url_prefix="/")


if __name__ == '__main__':
    app.run(debug=True, port=8000)