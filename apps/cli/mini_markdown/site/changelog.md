title: Changelog
order: 7

# Changelog

## 0.9.2 -- 2026-09-30

* Fixed: an npm tarball with a `+` in its version was stored under the
  wrong key ([#212][212]).
* Fixed: `harbor gc` no longer follows symlinks out of `data_dir`.

## 0.9.0 -- 2026-08-14

* New: the S3 blob store (beta). See [[Configuration]].
* New: `harbor token list --expired`.
* Changed: the default `max_upload` is now 200 MiB (was 100 MiB).

## 0.8.0 -- 2026-06-02

* New: yanking, for both PyPI and npm releases.
* Removed: the `--legacy-paths` flag, deprecated since 0.6.

[212]: https://git.example.invalid/harbor/issues/212 "npm versions with build metadata"
