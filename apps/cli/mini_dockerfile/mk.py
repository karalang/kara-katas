# Writes data/: Dockerfiles as people write them (a multi-stage Go
# service, a Python web app, a Windows image with the backtick escape, a
# legacy file with lowercase instructions, a CRLF file) and files that
# test each corner of the parser, and jobs.tsv, the jobs oracle.py and
# mini_dockerfile.kara run.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def put(rel, text, newline="\n"):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.replace("\n", newline).encode("utf-8"))


GO_SERVICE = """\
# syntax=docker/dockerfile:1.4
ARG GO_VERSION=1.22
ARG BASE=alpine:3.19
FROM --platform=$BUILDPLATFORM golang:${GO_VERSION} AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
ARG VERSION=dev
RUN CGO_ENABLED=0 go build \\
    -ldflags "-X main.version=${VERSION}" \\
    -o /out/app ./cmd/app

FROM ${BASE}
ARG VERSION
ARG BASE
LABEL org.opencontainers.image.title="billing api" \\
      org.opencontainers.image.version=$VERSION maintainer=ops@example.com
ENV APP_HOME=/srv/app PATH=/srv/app/bin:$PATH
COPY --from=build /out/app $APP_HOME/bin/app
EXPOSE 8080
USER 65534
HEALTHCHECK --interval=30s CMD wget -qO- http://localhost:8080/health || exit 1
CMD ["app", "--port", "8080"]
"""

PYTHON_APP = """\
FROM python:3.12-slim

LABEL description="Order service" version="2.1.0"
LABEL "com.example.vendor"="ACME Inc." owner='Data Team'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off \\
    APP_DIR=/app
ENV GREETING hello world from $APP_DIR

WORKDIR $APP_DIR
COPY requirements.txt .
RUN pip install -r requirements.txt \\
    # pinned in requirements.txt
    && rm -rf /root/.cache

COPY . .
EXPOSE 8000
ENTRYPOINT ["gunicorn"]
CMD ["-b", "0.0.0.0:8000", "app:wsgi"]
"""

WINDOWS = """\
# escape=`
FROM mcr.microsoft.com/windows/servercore:ltsc2022
SHELL ["powershell", "-Command"]
ENV TOOLS_DIR C:\\tools
RUN New-Item -ItemType Directory -Path $env:TOOLS_DIR ; `
    Invoke-WebRequest https://example.com/tool.zip -OutFile tool.zip
COPY app\\ C:\\app\\
WORKDIR C:\\app
CMD ["C:\\\\app\\\\server.exe"]
"""

LEGACY = """\
from ubuntu:22.04
maintainer Jane Doe <jane@example.com>
run apt-get update && \\
    apt-get install -y curl

env DEBIAN_FRONTEND noninteractive
label release="2019.10" stage=old
Expose 22
cmd /usr/sbin/sshd -D
"""

STAGES = """\
ARG PYTHON=3.11
ARG REGISTRY=registry.example.com
FROM $REGISTRY/python:$PYTHON AS deps
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ARG PYTHON
RUN pip wheel -r requirements.txt -w /wheels
CMD ["deps"]

FROM scratch AS assets
COPY static /static

FROM $REGISTRY/python:$PYTHON-slim
ARG PYTHON
ARG EXTRA
LABEL python=$PYTHON extra=${EXTRA}
COPY --from=deps /wheels /wheels
COPY --from=assets /static /srv/static
CMD python -m app
"""

ESCAPES = """\
FROM busybox
ENV A=one B="two words" C='single $A' D=\\$A E=${A}-${B} F=$A$B G=${MISSING}x
ENV H="say \\"hi\\"" I=back\\\\slash J=tab\\ sep K=${A
LABEL "quoted key"=v1 plain=a\\ b
ENV NAME first value
ENV LONG  spaced   value
RUN echo $A
"""

CONTINUATION = """\
FROM alpine
RUN apk add --no-cache \\
    curl \\

    git
RUN echo one \\
# a comment inside
    two
RUN echo trailing \\
    spaces
LABEL a=1 \\
      b=2
"""

EDGE = """\
FROM
RUN

  WORKDIR   /tmp
#comment without space
   # indented comment
ENTRYPOINT ["sh"]
FROM --platform=linux/amd64
FROM --platform=linux/arm64 debian:12 AS base
FROM debian:12 as lower
CMD last"""

LABEL_FIRST = """\
LABEL first=yes
FROM alpine
LABEL second=yes
"""

BAD_LABEL = """\
FROM alpine
LABEL a=1 b
"""

NO_FROM = """\
# just notes
RUN echo hi
"""

EMPTY = ""

CRLF = """\
FROM node:20
WORKDIR /app
COPY package.json .
RUN npm ci \\
    --omit=dev
CMD ["node", "server.js"]
"""

UNICODE = """\
FROM alpine
LABEL title="café ☕" author=Zoë
ENV GREETING=héllo
"""

FILES = {
    "go.Dockerfile": GO_SERVICE,
    "python.Dockerfile": PYTHON_APP,
    "windows.Dockerfile": WINDOWS,
    "legacy.Dockerfile": LEGACY,
    "stages.Dockerfile": STAGES,
    "escapes.Dockerfile": ESCAPES,
    "continuation.Dockerfile": CONTINUATION,
    "edge.Dockerfile": EDGE,
    "labelfirst.Dockerfile": LABEL_FIRST,
    "badlabel.Dockerfile": BAD_LABEL,
    "nofrom.Dockerfile": NO_FROM,
    "empty.Dockerfile": EMPTY,
    "unicode.Dockerfile": UNICODE,
}

READ_ONLY = ["structure", "json", "info", "context"]

JOBS = [
    ["info", "go.Dockerfile", "--build-arg", "VERSION=1.4.2", "--build-arg", "BASE=gcr.io/distroless/static"],
    ["info", "go.Dockerfile", "--no-env-replace"],
    ["context", "go.Dockerfile", "--build-arg", "VERSION=1.4.2"],
    ["info", "python.Dockerfile", "--parent-env", "PATH=/usr/local/bin", "--parent-env", "APP_DIR=/srv"],
    ["context", "python.Dockerfile"],
    ["info", "stages.Dockerfile", "--build-arg", "PYTHON=3.12", "--build-arg", "EXTRA=gpu"],
    ["context", "stages.Dockerfile", "--build-arg", "PYTHON=3.12"],
    ["info", "escapes.Dockerfile"],
    ["context", "escapes.Dockerfile", "--no-env-replace"],
    ["info", "unicode.Dockerfile"],
    ["baseimage", "go.Dockerfile", "alpine:3.20"],
    ["parents", "go.Dockerfile", "golang:1.23", "alpine:3.20"],
    ["parents", "go.Dockerfile", "golang:1.22", "${BASE}"],
    ["parents", "go.Dockerfile", "only-one"],
    ["parents", "stages.Dockerfile", "a", "b", "c", "d"],
    ["parents", "edge.Dockerfile", "x", "y", "z", "w"],
    ["baseimage", "nofrom.Dockerfile", "alpine"],
    ["cmd", "go.Dockerfile", '["app", "--port", "9090"]'],
    ["cmd", "stages.Dockerfile", "python -m app --debug"],
    ["cmd", "nofrom.Dockerfile", "echo bye"],
    ["cmd", "legacy.Dockerfile", "/bin/bash"],
    ["labels", "python.Dockerfile", "description=Order service", "team=payments", "com.example.vendor=ACME Inc."],
    ["labels", "go.Dockerfile"],
    ["labels", "stages.Dockerfile", "python=3.12", "extra="],
    ["labels", "labelfirst.Dockerfile", "first=no"],
    ["envs", "python.Dockerfile", "APP_DIR=/srv/app", "NEW=it's new"],
    ["envs", "windows.Dockerfile", "TOOLS_DIR=D:\\tools"],
    ["args", "stages.Dockerfile", "PYTHON=3.12"],
    ["label", "python.Dockerfile", "version", "2.2.0"],
    ["label", "legacy.Dockerfile", "release", "2020 final"],
    ["label", "empty.Dockerfile", "a", "b"],
    ["unlabel", "python.Dockerfile", "owner"],
    ["unlabel", "python.Dockerfile", "missing"],
    ["unlabel", "continuation.Dockerfile", "a"],
    ["add", "go.Dockerfile", "--", "USER root", "RUN apk add curl   "],
    ["add", "go.Dockerfile", "all_stages", "--", "LABEL stage=yes"],
    ["add", "stages.Dockerfile", "all_stages", "skip_scratch", "--", "ENV TZ=UTC"],
    ["add", "stages.Dockerfile", "all_stages", "at_start", "--", "ARG CACHE_BUST"],
    ["add", "nofrom.Dockerfile", "at_start", "--", "FROM alpine"],
    ["add", "empty.Dockerfile", "--", "FROM alpine"],
    ["add", "edge.Dockerfile", "--", "RUN true"],
    ["add-at", "python.Dockerfile", "line", "2", "--", "ARG BUILD_DATE"],
    ["add-at", "python.Dockerfile", "line", "2", "replace", "--", "LABEL replaced=yes"],
    ["add-at", "python.Dockerfile", "line", "40", "--", "RUN false"],
    ["add-at", "python.Dockerfile", "insn", "7", "after", "--", "RUN echo after"],
    ["add-at", "python.Dockerfile", "insn", "7", "replace", "--", "RUN pip install -r requirements.txt", "RUN rm -rf /root/.cache"],
    ["add-at", "go.Dockerfile", "text", "EXPOSE 8080", "after", "--", "EXPOSE 9090"],
    ["add-at", "go.Dockerfile", "text", "COPY . .", "replace", "--", "COPY src/ ."],
    ["add-at", "go.Dockerfile", "text", "EXPOSE 1", "--", "EXPOSE 2"],
    ["delete", "go.Dockerfile", "COPY"],
    ["delete", "go.Dockerfile", "RUN", "go mod download"],
    ["delete", "python.Dockerfile", "LABEL", "owner"],
    ["delete", "python.Dockerfile", "ENV", "PIP_NO_CACHE_DIR"],
    ["delete", "stages.Dockerfile", "ARG", "PYTHON"],
    ["delete", "legacy.Dockerfile", "MAINTAINER"],
    ["delete", "legacy.Dockerfile", "COMMENT"],
]


def main():
    shutil.rmtree(DATA, ignore_errors=True)
    for name, text in FILES.items():
        put(name, text)
    put("crlf.Dockerfile", CRLF, newline="\r\n")
    names = sorted(list(FILES) + ["crlf.Dockerfile"])
    jobs = []
    for op in READ_ONLY:
        for n in names:
            jobs.append([op, n])
    jobs += JOBS
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as f:
        for j in jobs:
            f.write("\t".join(j) + "\n")


main()
