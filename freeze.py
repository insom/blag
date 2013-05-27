from flask.ext.frozen import Freezer
from blag.app import create_app

app = create_app()

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
