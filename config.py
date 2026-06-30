class Config:
    # Flask
    SECRET_KEY = "skilltrack_secret_key"

    # Database
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/skilltrack"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT — access tokens expire after 1 day
    JWT_SECRET_KEY = "skilltrack_jwt_secret_key"
    JWT_ACCESS_TOKEN_EXPIRES = 86400   # seconds
