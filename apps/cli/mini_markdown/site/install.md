title: Installation
order: 2

# Installation {#install}

Harbor ships as a single static binary for Linux and macOS, and as a
container image.

## From a release

Download the archive for your platform, check it, and put the binary on
your `PATH`:

```bash
curl -LO https://downloads.example.invalid/harbor/0.9.2/harbor-linux-x86_64.tar.gz
sha256sum -c harbor-0.9.2.sha256
tar xzf harbor-linux-x86_64.tar.gz
sudo install harbor /usr/local/bin/
```

!!! warning "Check the signature"
    The checksum file is signed. A checksum you downloaded from the same
    place as the archive proves nothing on its own.

## With a container

    docker run -p 7070:7070 -v harbor-data:/data harbor/harbor:0.9.2

The image runs as user `harbor` (uid 10001) and keeps everything under
`/data`.

## From source { .advanced }

You need a recent toolchain and `make`:

~~~ {.shell #build-steps}
git clone https://git.example.invalid/harbor.git
cd harbor && make release
~~~

*[PATH]: The list of directories the shell searches for commands
*[uid]: User identifier
