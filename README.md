# Stepik FastAPI course first final task
Implemented features:
* user registration and authentication via JWT;
* getting info about currencies

## Endpoints
API is based on currency service https://apilayer.com/.
1. `/auth/register` - user registration. Form params:
    * login
    * password
    * name
    * surname
2. `/auth/login/` - user login. Form params:
    * username (i.e. login)
    * password.
    Returns JWT-token
3. `/currency/list` - list of currencies. Available only after authentication (login). Params and response are based on https://apilayer.com/ API.
4. `/currency/exchange` - exchange rate of currencies. Available only after authentication (login). Body params (json):
    * from
    * to
    * amount
    * date
Params and response are based on https://apilayer.com/ API

## Info
You'd add  your own `.env` file to the root of the project  with corresponding secret variables or yo can get them from environmental variables in OS.

List of env-variables:
- APILAYER_URL=https://api.apilayer.com/currency_data - base url for getting currency data
- APILAYER_ACCESS_KEY - your personal access key from https://apilayer.com/
- DB_HOST
- DB_PORT
- DB_USER
- DB_PASS
- DB_NAME
- JWT_SECRET_KEY - a secret key to cypher jwt token data
- USER_PASSWORD_SALT - special key to append to raw user password before hashing