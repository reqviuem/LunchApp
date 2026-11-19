# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /LunchApp

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser \
    && chown appuser:appuser /LunchApp

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


FROM base AS dev

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=bind,source=requirements-dev.txt,target=requirements-dev.txt \
    python -m pip install -r requirements-dev.txt

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM base AS production

COPY --chown=appuser:appuser . .

RUN DJANGO_SECRET_KEY=build-only POSTGRES_DB=build POSTGRES_USER=build POSTGRES_PASSWORD=build \
    python manage.py collectstatic --noinput \
    && chown -R appuser:appuser /LunchApp/staticfiles

USER appuser

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
