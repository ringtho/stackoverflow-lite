import os
from stackoverflow.routes import app
from dotenv import load_dotenv
load_dotenv()

debug=os.environ.get('DEBUG')

if __name__ == '__main__':
    app.run(debug=True, port=5000)