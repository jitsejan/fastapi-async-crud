# fastapi-postgres-crud-vuejs
An experiment with FastAPI based on different blogposts.

## Frontend
- VueJS
- Axios

```bash
$ cd frontend
$ npm install
$ npm run serve
```

## Backend
- FastAPI
- SQLAlchemy

```bash
$ cd backend
$ pipenv install
$ pipenv shell
$ uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
```

## Sources
- https://fastapi.tiangolo.com/tutorial/sql-databases/
- https://testdriven.io/blog/fastapi-crud/
- https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs
- https://bezkoder.com/vue-js-crud-app/
- https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs
