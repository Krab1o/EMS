FROM python:3.11 AS builder

WORKDIR /app

RUN \
  --mount=type=cache,target=/var/lib/apt/lists \
  --mount=type=cache,target=/var/cache/apt/archives \
  apt-get update \
  && apt-get install -y --no-install-recommends build-essential

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"
RUN curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 \
                                       RYE_INSTALL_OPTION="--yes" \
                                       RYE_TOOLCHAIN_VERSION=3.11 \
                                       bash

COPY pyproject.toml .python-version ./
RUN rye sync --no-dev

FROM python:3.11-slim as final

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/src:$PYTHONPATH"
ENV RYE_HOME="/opt/rye"
ENV PATH="/app/.venv/bin:$RYE_HOME/shims:$PATH"

COPY --from=builder /opt/rye /opt/rye
COPY --from=builder /app/.venv .venv
COPY entrypoint.sh /entrypoint.sh
COPY src src

RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
