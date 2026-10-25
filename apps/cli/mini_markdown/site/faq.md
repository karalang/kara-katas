title: FAQ
order: 6

# Frequently asked questions

## Does Harbor proxy requests it cannot serve?

Yes. A request for a file Harbor does not have goes upstream once; the
answer is stored and every later request is served locally.

## Can I run two Harbors behind a load balancer?

Not yet. The metadata store takes a lock on `data_dir`, so a second
process on the same directory exits with:

    error: data_dir /var/lib/harbor is locked by pid 4242

## How big does `data_dir` get?

Roughly the size of everything ever installed through it, plus about 2%
for metadata. Run `harbor gc --dry-run` to see what a clean-up would
free.

## Why "Harbor"?

Because packages come in, get stored, and go out again. Also, the
author's previous project was called "Dock" and the joke wrote itself.
