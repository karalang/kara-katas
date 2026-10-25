title: Configuration
order: 3

# Configuration

Harbor reads `harbor.toml` from the working directory, or the file named
by `--config`. Every key has a default; the smallest useful file names
only `data_dir`.

## Keys

`data_dir`
:   Where the metadata store and the local blob store live. Required.

`listen`
:   The address to serve on. Default `127.0.0.1:7070`.

`upstream.pypi`
:   The index to mirror for Python packages. Default
    `https://pypi.org/simple/`. Set it to `""` to turn the mirror off.

`upstream.npm`
:   The registry to mirror for npm packages.

    Scoped packages (`@scope/name`) are mirrored too, unless the scope is
    listed in `private_scopes`.

## Blob stores

=== "Disk"
The default. Blobs are content-addressed files under `data_dir/blobs`.

<div markdown="1" class="callout">
**Tip:** put `data_dir` on its own volume, so a full disk stops uploads
but not the operating system.
</div>

### S3

```toml
[blobs]
kind = "s3"
bucket = "harbor-blobs"
region = "eu-west-1"
```

!!! danger "Credentials"
    Never write keys into `harbor.toml`. Harbor reads the usual
    `AWS_*` environment variables, or the instance role.

## Limits { data-toc-label="Upload limits" }

| Limit          | Default |
|----------------|---------|
| `max_upload`   | 200 MiB |
| `max_files`    | 64      |
| `rate_per_min` | 120     |
