import os
from dotenv import load_dotenv
load_dotenv()

from news import app

if __name__ == '__main__':
    app.run(debug=True, host=os.getenv("FLASK_HOST"))
