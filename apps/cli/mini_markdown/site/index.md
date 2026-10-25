title: Harbor
order: 1
summary: A self-hosted package registry for small teams.

# Harbor

Harbor is a self-hosted package registry for teams that want their own
mirror of the public indexes and a private place for internal packages.
It speaks the Python *simple* index, the npm registry protocol and a
plain HTTP file layout, so `pip`, `npm` and `curl` all work against it.

[TOC]

## Why Harbor

* **One binary.** No database server: metadata lives in an embedded
  store under `data_dir`, and blobs on disk or in an S3 bucket.
* **Mirrors that keep working.** A package you have installed once stays
  available when the upstream index is down -- or when the author yanks it.
* **Private packages.** Publish with the tools you already use; see
  [[Publishing]].

!!! note
    Harbor is not a build system. It stores what you give it and serves
    it back, byte for byte.

## Quick start

1. Install the binary (see [Installation](install.md)).
2. Write a two-line config:

    ```toml
    data_dir = "/var/lib/harbor"
    listen = "127.0.0.1:7070"
    ```

3. Run `harbor serve` and point `pip` at it:

        pip install --index-url http://127.0.0.1:7070/pypi/simple/ requests

## Status

| Feature           | Status      | Since |
|:------------------|:-----------:|------:|
| PyPI mirror       | stable      | 0.4   |
| npm mirror        | stable      | 0.6   |
| Private uploads   | stable      | 0.7   |
| S3 blob store     | beta        | 0.9   |
| OCI images        | not planned |       |

Harbor's licence is the "MIT" licence[^lic]. It's been "production ready"
since '23 -- or so the changelog says...

[^lic]: See the `LICENSE` file in the source tree.
