import os
import os.path as op
#Function to get all env variables and exception cause if that env var is not set for some reason.
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

# VALUES FOR POSTGRES SETUP
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")
TRACK_MODIFICATIONS = False

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

#Key
SECRET_KEY= get_env_variable('SECRET_KEY')

image_path = op.join(op.dirname(__file__), "static/images")