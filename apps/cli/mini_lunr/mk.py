"""Writes data/docs.txt and data/queries.txt for mini_lunr: the pages of a
made-up command-line tool's documentation site (harbor, a container
registry client) and the searches its readers type.

docs.txt is one page a line: ref|boost|title|tags|body. queries.txt is
one search a line.

Run: python3 -s -P -B mk.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MASK32 = 4294967295


def hash32(a):
    h = a & MASK32
    h = (((h >> 16) ^ h) * 73244475) & MASK32
    h = (((h >> 16) ^ h) * 73244475) & MASK32
    return (h >> 16) ^ h


def mix(seed, i, salt):
    return hash32(seed * 1000003 + i * 104729 + salt * 15485863)


TOPICS = [
    ("guide/install", "Installing harbor", "install setup"),
    ("guide/quickstart", "Quickstart: push your first image", "start tutorial"),
    ("guide/configure", "Configuring the client", "config setup"),
    ("guide/auth", "Authentication and tokens", "auth security"),
    ("guide/proxy", "Running behind a proxy", "network config"),
    ("guide/mirrors", "Registry mirrors and caching", "network cache"),
    ("guide/signing", "Signing and verifying images", "security signing"),
    ("guide/retention", "Retention policies", "storage policy"),
    ("guide/replication", "Replicating between registries", "network replication"),
    ("guide/webhooks", "Webhooks and notifications", "events integration"),
    ("guide/quotas", "Project quotas", "storage policy"),
    ("guide/scanning", "Vulnerability scanning", "security scan"),
    ("guide/ci", "Using harbor in CI pipelines", "integration automation"),
    ("guide/troubleshooting", "Troubleshooting connection errors", "network errors"),
    ("guide/upgrading", "Upgrading from version 1", "install upgrade"),
    ("guide/garbage", "Garbage collection", "storage cleanup"),
    ("ref/cli/push", "harbor push", "cli command"),
    ("ref/cli/pull", "harbor pull", "cli command"),
    ("ref/cli/login", "harbor login", "cli command auth"),
    ("ref/cli/logout", "harbor logout", "cli command auth"),
    ("ref/cli/tag", "harbor tag", "cli command"),
    ("ref/cli/inspect", "harbor inspect", "cli command"),
    ("ref/cli/copy", "harbor copy", "cli command replication"),
    ("ref/cli/delete", "harbor delete", "cli command storage"),
    ("ref/cli/list", "harbor list", "cli command"),
    ("ref/cli/sign", "harbor sign", "cli command signing"),
    ("ref/cli/verify", "harbor verify", "cli command signing"),
    ("ref/cli/scan", "harbor scan", "cli command scan"),
    ("ref/cli/prune", "harbor prune", "cli command cleanup"),
    ("ref/cli/config", "harbor config", "cli command config"),
    ("ref/config/file", "The configuration file", "config reference"),
    ("ref/config/env", "Environment variables", "config reference"),
    ("ref/config/credentials", "Credential helpers", "config auth"),
    ("ref/config/retries", "Retries and timeouts", "config network"),
    ("ref/api/repositories", "Repositories API", "api reference"),
    ("ref/api/artifacts", "Artifacts API", "api reference"),
    ("ref/api/projects", "Projects API", "api reference"),
    ("ref/api/users", "Users API", "api reference auth"),
    ("ref/api/errors", "Error codes", "api errors"),
    ("ref/api/pagination", "Pagination", "api reference"),
    ("ref/api/rate-limits", "Rate limits", "api network"),
    ("faq/slow-pulls", "Why are my pulls slow?", "faq network"),
    ("faq/denied", "Why is my push denied?", "faq auth errors"),
    ("faq/disk", "The registry disk is full", "faq storage"),
    ("faq/manifest", "Manifest unknown errors", "faq errors"),
    ("faq/tags", "Can a tag point at two images?", "faq"),
    ("blog/2026-05-release", "Release notes: harbor 2.4", "release"),
    ("blog/2026-08-release", "Release notes: harbor 2.5", "release"),
    ("blog/zero-downtime", "Zero-downtime registry upgrades", "upgrade operations"),
    ("blog/sbom", "Shipping SBOMs with every image", "security"),
]

WORDS = (
    "image images registry registries repository repositories tag tags tagged tagging "
    "push pushes pushed pushing pull pulls pulled pulling layer layers manifest manifests "
    "digest digests token tokens credential credentials login logout password user users "
    "project projects quota quotas storage disk blob blobs cache cached caching mirror mirrors "
    "proxy proxies network connection connections timeout timeouts retry retries retrying "
    "configure configured configuring configuration configurations config file files "
    "environment variable variables setting settings default defaults option options "
    "sign signed signing signature signatures verify verified verifying verification key keys "
    "scan scanned scanning scanner vulnerability vulnerabilities report reports policy policies "
    "retention delete deleted deleting deletion prune pruned pruning garbage collection "
    "replicate replicated replicating replication webhook webhooks event events notification "
    "notifications pipeline pipelines build builds automation automated error errors denied "
    "unauthorized forbidden unknown missing upgrade upgraded upgrading version versions release "
    "releases client server request requests response responses header headers page pages "
    "limit limits rate rates slow fast faster quickly install installed installing package "
    "packages binary binaries platform platforms linux macos windows architecture architectures "
    "run running runs command commands flag flags output format json table verbose quiet "
    "the a an of to in for with on by from that this it is are be can will must should not "
    "you your when if then each every all any more most only also before after"
).split()

STOPPERS = ["the", "a", "an", "of", "to", "in", "for", "with", "on", "by", "from", "that",
            "this", "it", "is", "are", "be", "can", "will", "must", "should", "not", "you",
            "your", "when", "if", "then", "each", "every", "all", "any", "more", "most",
            "only", "also", "before", "after"]

EXTRAS = ["(see", "below)", "e.g.", "don't", "can't", "--force", "--insecure", "max_retries",
          "HARBOR_TOKEN", "v2.4", "v2.5", "8443", "443", "self-signed", "TLS", "x509:",
          "sha256:3f2a", "harbor.example.com", "ci/cd", "...", "it's", "'latest'", "UTF-8",
          "kubernetes", "OCI", "S3", "re-run", "per-project", "rate-limited", "--all-tags"]


def sentence(seed, i, n):
    out = []
    length = 6 + mix(seed, i, n) % 12
    for w in range(length):
        r = mix(seed, i * 31 + n, w)
        if r % 17 == 0:
            word = EXTRAS[r // 17 % len(EXTRAS)]
        elif r % 3 == 0:
            word = STOPPERS[r // 3 % len(STOPPERS)]
        else:
            word = WORDS[r // 7 % len(WORDS)]
        out.append(word)
    out[0] = out[0][:1].upper() + out[0][1:]
    end = ["." , ".", ".", "?", "!", ":"][mix(seed, i, n + 99) % 6]
    if mix(seed, i, n + 7) % 4 == 0:
        k = 1 + mix(seed, i, n + 8) % (len(out) - 1)
        out[k - 1] += ","
    return " ".join(out) + end


def body_for(i, ref, title):
    seed = 7001
    words = title.lower().replace(":", "").replace("?", "").split()
    first = "This page covers " + " ".join(words) + "."
    sentences = [first]
    for n in range(4 + mix(seed, i, 500) % 12):
        sentences.append(sentence(seed, i, n))
    if ref.startswith("ref/cli/"):
        cmd = ref.split("/")[-1]
        sentences.append("Usage: harbor %s [flags] image." % cmd)
    return " ".join(sentences)


def main():
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    lines = []
    for i, (ref, title, tags) in enumerate(TOPICS):
        boost = 2 if ref in ("guide/quickstart", "guide/install", "faq/denied") else 1
        lines.append("%s|%d|%s|%s|%s" % (ref, boost, title, tags, body_for(i, ref, title)))
    text = "\n".join(lines) + "\n"
    for bad in '"\\{}':
        assert bad not in text
    with open(os.path.join(HERE, "data", "docs.txt"), "w") as f:
        f.write(text)

    queries = [
        "push", "pushing images", "harbor push", "image", "images registry", "the",
        "title:push", "body:retention", "tags:security", "title:harbor body:denied",
        "+push +denied", "+signing -verify", "-scan", "-scan -sign", "+mirror cache",
        "push^10 pull", "pull^0", "token^2 credential", "config*", "*tion", "re*ion",
        "sign*", "*", "harb*", "conf*~1", "regstry~1", "repositry~2", "pushd~1", "tken~1",
        "imgaes~2", "replcation~1", "slow pulls", "why are my pulls slow", "disk full",
        "manifest unknown", "x509", "tls", "max_retries", "harbor_token", "e.g.",
        "don't", "v2.4", "8443", "oci", "s3", "kubernetes", "upgrade", "upgrading",
        "upgraded", "upgrades", "zero downtime", "release notes", "sbom", "sboms",
        "rate limits", "rate-limited", "per-project", "self-signed", "ci/cd", "--force",
        "force", "insecure", "all tags", "latest", "garbage collection", "prune",
        "quota", "quotas policy", "retention policies", "webhook event", "notifications",
        "users api", "pagination", "error codes", "unauthorized", "forbidden",
        "credential helpers", "environment variables", "configuration file",
        "title:configuring", "title:config*", "body:conf*", "tags:cli +title:harbor",
        "+tags:faq", "-tags:cli", "tags:api -body:error", "+body:verify +body:signature",
        "+zzzz", "+zzzz push", "zzzz", "-zzzz", "push -zzzz", "a", "an image",
        "title:", "nosuchfield:push", "push~", "push^", "push^x", "push~a", "+", "-",
        ":push", "title:+push", "push title:", "foo\\:bar", "foo\\\\bar", "push\\",
        "\\-scan", "push  pull", "  push  ", "PUSH", "Push Pull", "pu*sh", "p*", "*s",
        "~1", "^2", "push~1^5", "push^5~1", "title:push~1^3", "+title:pull -body:push",
        "sign verify signature signing", "verification", "verified", "scanning scanner",
        "vulnerabilities", "vulnerability report", "linux macos windows", "architecture",
        "json output", "verbose quiet", "install package binary", "proxy connection timeout",
        "retry retries retrying", "mirror~1", "caching~2", "cach*", "*ing", "*ed",
        "replicat*", "web*", "page*", "header headers", "request response",
    ]
    for q in queries:
        for bad in '"{}|':
            assert bad not in q
    with open(os.path.join(HERE, "data", "queries.txt"), "w") as f:
        f.write("\n".join(queries) + "\n")
    print("%d pages, %d queries" % (len(lines), len(queries)))


main()
