title: API
order: 5

# HTTP API

All endpoints live under `/api/v1/` and speak JSON. Authenticate with a
bearer token from `harbor token create`.

## Packages {#packages}

### `GET /api/v1/packages`

Lists packages, 50 to a page. Query parameters:

| Name     | Type   | Meaning                               |
|----------|--------|---------------------------------------|
| `q`      | string | Substring of the name                 |
| `kind`   | string | `pypi`, `npm` or `file`               |
| `cursor` | string | From the previous page's `next` field |

Response:

```json
{"items": [{"name": "widgets", "kind": "pypi", "latest": "1.4.0"}],
 "next": null}
```

## Releases {#releases}

### `POST /api/v1/releases/{ns}/{name}/{version}/yank`

Marks a release yanked. Idempotent: yanking twice is not an error.

### `DELETE /api/v1/releases/{ns}/{name}/{version}`

Deletes the release and its files. *This cannot be undone.* Mirrors that
already fetched the files keep them.

## Errors

Errors are `{"error": "<code>", "detail": "<text>"}` with an HTTP status:

* `400` -- `bad_request`: the body did not parse.
* `401` -- `unauthorized`: no token, or an expired one.
* `403` -- `forbidden`: the token's team does not own the namespace.
* `404` -- `not_found`.
* `409` -- `conflict`: the version already exists.

<details>
<summary>Retry advice</summary>
Retry `429` and `503` with backoff; never retry a `409`.
</details>
