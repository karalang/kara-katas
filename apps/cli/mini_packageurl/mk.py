#!/usr/bin/env python3
"""Writes data/jobs.tsv: parse / canonicalize / build Package-URL jobs that
both oracle.py and the Kara port run through packageurl-python.

One tab-separated line per job; field 0 names the kind:

  parse <purl>                              from_string -> components + canonical
  build <type> <ns> <name> <ver> <q> <sub>  PackageURL(...).to_string()

A `parse` job prints the six components (type / namespace / name / version /
qualifiers / subpath, `-` for an absent one, qualifiers as sorted key=value
joined by &) and the canonical string, or `err=<message>` with the library's
exact ValueError text. A `build` job prints `str=<purl>` or `err=<message>`;
its `-` fields are passed as None.

The parse set is the package-url/purl-spec test suite (the copy vendored with
the library), covering type/namespace/name lowercasing per type, npm's `@`
namespace, golang subpaths, docker's colon version, percent-encoded names,
qualifier sorting and case-folding, the slash-stripped `pkg:/`, `pkg://` and
`pkg:///` forms, and every error path. The build set exercises the component
constructor and the per-type name rules (pypi `_`->`-`, hackage, pub, cpan,
mlflow) and percent-encoding on output.
"""
import os

os.makedirs("data", exist_ok=True)

# field 0 = kind; a literal "-" means None. Tab-separated.
JOBS = [
    # ---- parse: the purl-spec test suite ----
    ["parse", "pkg:maven/org.apache.commons/io@1.3.4"],
    ["parse", "pkg:maven/org.apache.commons/io"],
    ["parse", "pkg:GOLANG/google.golang.org/genproto#/googleapis/api/annotations/"],
    ["parse", "pkg:GOLANG/google.golang.org/genproto@abcdedf#/googleapis/api/annotations/"],
    ["parse", "pkg:golang/github.com/nats-io/nats-server/v2/server@v1.2.9"],
    ["parse", "pkg:bitbucket/birKenfeld/pyGments-main@244fd47e07d1014f0aed9c"],
    ["parse", "pkg:github/Package-url/purl-Spec@244fd47e07d1004f0aed9c"],
    ["parse", "pkg:deb/debian/curl@7.50.3-1?arch=i386&distro=jessie"],
    ["parse", "pkg:docker/customer/dockerimage@sha256:244fd47e07d1004f0aed9c?repository_url=gcr.io"],
    ["parse", "pkg:gem/jruby-launcher@1.1.2?Platform=java"],
    ["parse", "pkg:Maven/org.apache.xmlgraphics/batik-anim@1.9.1?repositorY_url=repo.spring.io/release&classifier=sources"],
    ["parse", "pkg:Maven/org.apache.xmlgraphics/batik-anim@1.9.1?repositorY_url=repo.spring.io/release&extension=pom"],
    ["parse", "pkg:Maven/net.sf.jacob-project/jacob@1.14.3?type=dll&classifier=x86"],
    ["parse", "pkg:npm/%40angular/animation@12.3.1"],
    ["parse", "pkg:Nuget/EnterpriseLibrary.Common@6.0.1304"],
    ["parse", "pkg:PYPI/Django_package@1.11.1.dev1"],
    ["parse", "pkg:composer/guzzlehttp/promises@2.0.2"],
    ["parse", "pkg:Rpm/fedora/curl@7.50.3-1.fc25?Arch=i386&Distro=fedora-25"],
    ["parse", "pkg:/maven/org.apache.commons/io"],
    ["parse", "pkg://maven/org.apache.commons/io"],
    ["parse", "pkg:///maven/org.apache.commons/io"],
    ["parse", "pkg:maven/HTTPClient/HTTPClient@0.3-3"],
    ["parse", "pkg:maven/mygroup/myartifact@1.0.0%20Final?mykey=my%20value"],
    ["parse", "pkg:npm/@babel/core#/googleapis/api/annotations/"],
    ["parse", "pkg:npm/@babel/core@1.0.2#/googleapis/api/annotations/"],
    ["parse", "pkg:npm/core@1.0.2#/googleapis/api/annotations/"],
    ["parse", "pkg:npm/core#/googleapis/api/annotations/"],
    ["parse", "pkg:NPM/core#/googleapis/api/annotations/"],
    # ---- parse: error paths ----
    ["parse", "EnterpriseLibrary.Common@6.0.1304"],
    ["parse", "pkg:EnterpriseLibrary.Common@6.0.1304"],
    ["parse", "pkg:maven/@1.3.4"],
    ["parse", "pkg:npm/myartifact@1.0.0?in%20production=true"],
    ["parse", "   "],
    # ---- parse: extra real-world ----
    ["parse", "pkg:pypi/requests@2.31.0"],
    ["parse", "pkg:cargo/serde@1.0.197"],
    ["parse", "pkg:golang/golang.org/x/text@v0.3.7"],
    ["parse", "pkg:generic/openssl@1.1.10g?download_url=https://openssl.org/source/openssl-1.1.10g.tar.gz&checksum=sha256:de4d501267da"],
    ["parse", "pkg:deb/ubuntu/libncurses5@6.1?arch=amd64"],
    ["parse", "pkg:huggingface/distilbert-base-uncased@043235d6088ecd3dd5fb5ca3592b6913fd516027"],
    ["parse", "pkg:oci/debian@sha256%3A244fd47e07d10?repository_url=docker.io/library/debian&tag=bullseye"],
    # ---- build: from components ----
    ["build", "maven", "org.apache.commons", "io", "1.3.4", "-", "-"],
    ["build", "npm", "@angular", "animation", "12.3.1", "-", "-"],
    ["build", "pypi", "-", "Django_Package", "1.11.1.dev1", "-", "-"],
    ["build", "hackage", "-", "AC_Vector_Space", "1.0", "-", "-"],
    ["build", "cpan", "DROLSKY", "DateTime", "1.55", "-", "-"],
    ["build", "pub", "-", "Flutter Package!", "2.0", "-", "-"],
    ["build", "maven", "mygroup", "myartifact", "1.0.0 Final", "mykey=my value", "-"],
    ["build", "golang", "google.golang.org", "genproto", "-", "-", "googleapis/api/annotations"],
    ["build", "deb", "debian", "curl", "7.50.3-1", "distro=jessie&arch=i386", "-"],
    ["build", "docker", "customer", "dockerimage", "sha256:244fd47e07d1004f0aed9c", "repository_url=gcr.io", "-"],
    ["build", "mlflow", "-", "TraceClassifier", "1", "repository_url=https://adb-1234.azuredatabricks.net", "-"],
    ["build", "mlflow", "-", "TraceClassifier", "1", "repository_url=https://westus.api.azureml.ms", "-"],
    ["build", "-", "ns", "name", "1.0", "-", "-"],
    ["build", "generic", "-", "-", "1.0", "-", "-"],
    ["build", "nuget", "-", "EnterpriseLibrary.Common", "6.0.1304", "-", "-"],
]

with open("data/jobs.tsv", "w") as f:
    for row in JOBS:
        f.write("\t".join(row) + "\n")

print("jobs:", len(JOBS))
