FROM python:3.13-slim

WORKDIR /winipyside

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY README.md LICENSE pyproject.toml uv.lock ./

RUN useradd -m -u 1000 appuser

RUN chown -R appuser:appuser .

USER appuser

COPY --chown=appuser:appuser winipyside winipyside

RUN uv sync --no-group dev

RUN rm README.md LICENSE pyproject.toml uv.lock

ENTRYPOINT ["uv", "run", "winipyside"]

CMD ["main"]