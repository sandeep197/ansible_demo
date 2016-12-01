from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
# This is a demo, so a hard coded username and password is okay.
# This isn't something to do in production.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://appuser:94nfsUl7@localhost/appdata'
db = SQLAlchemy(app)


class Greeting(db.Model):
    """ A simple class to represent a greeting """

    gid = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(80), unique=True)

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return '<Greeting %r>' % self.message

    @classmethod
    def get_or_create(cls, message):
        """ Gets or creates a Greeting """
        record = cls.query(cls).filter(cls.message == message).first()

        if record:
            return record

        record = cls(message=message)
        db.add(record)
        db.flush()

        return record

@app.route("/")
def main():
    """ The index.html route """
    return render_template('index.html')

# Make sure the tables exist
db.create_all()

# Create some records.
Greeting.get_or_create("Hello!")
Greeting.get_or_create("Hola!")
Greeting.get_or_create("Ciao!")


if __name__ == "__main__":
    app.run()
