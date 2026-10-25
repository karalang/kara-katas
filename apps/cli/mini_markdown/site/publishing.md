title: Publishing
order: 4

# Publishing private packages

Private packages live under a *namespace*. A namespace belongs to a team,
and only that team's tokens may upload to it.

## Python

Build as usual, then upload with `twine`:

```shell hl_lines="2"
python -m build
twine upload --repository-url http://harbor.internal:7070/pypi/legacy/ dist/*
```

The first upload of a name **claims** it for the namespace. After that, an
upload from another team gets `403 Forbidden`.

## npm

Point a scope at Harbor in `.npmrc`:

    @acme:registry=http://harbor.internal:7070/npm/

and run `npm publish`. Unscoped private packages are not supported: an
unscoped name could shadow a public one.

## Yanking

A yanked release stays downloadable by exact version, but `pip` and `npm`
will not pick it for a range. To yank:

1. Open the release page, or
2. call the API:

    ```http
    POST /api/v1/releases/acme/widgets/1.4.0/yank HTTP/1.1
    Authorization: Bearer <token>
    ```

> Yanking is for mistakes. To remove a release that leaked something,
> **delete** it and rotate whatever leaked.

See also [[Configuration]] and [the API reference](api.md#releases).
