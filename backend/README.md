## Run with docker
- If you want to run docker you need to [install docker](https://docs.docker.com/engine/install/)

- Create .env from .env.example
```bash
cp .env.example .dev.env
```
- Fill .dev.env with data you want for your postgresql. Docker will use these data to create the database for you

- Run docker
```bash
docker-compose up -d --build
```
or
```bash
docker compose up -d --build
```
## Run Without docker
- Start your Postgresql server and create a database, user.
- Create .env file like above, then fill in with postgres data you configured above
- Add Postgresql config to alembic/env.py and src/core/config.py
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.
```bash
pip install -r requirements.txt
```
- Run app with start.sh. It will do migrate migrations then run app 
```bash
chmod 755 start.sh
sh start.sh
```


```bash
alembic -x db_url="postgresql+asyncpg://greenaden:test@127.0.0.1/greenaden" revision --autogenerate
```