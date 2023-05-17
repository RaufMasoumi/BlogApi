FROM python:3.10.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR blogapi/
COPY Pipfile Pipfile.lock ./
RUN python -m pip install pipenv && pipenv install --system
COPY . .
EXPOSE 8000
CMD ["gunicorn", "django_project.wsgi", "-b", "0.0.0.0:8000"]
