# Writes data/: Java .properties files as projects ship them (a Spring
# Boot application.properties, resource bundles in UTF-8, ISO-8859-1 and
# native2ascii form, gradle.properties, log4j.properties, files with
# jproperties' metadata comments) and files that test each corner of the
# format, and jobs.tsv, the jobs oracle.py and mini_jproperties.kara run.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def put(rel, data):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


SPRING = """\
# Spring Boot settings for the billing service
! profiles are set by the deploy job

spring.application.name=billing-service
server.port = 8443
server.servlet.context-path : /api
spring.datasource.url=jdbc:postgresql://db.internal:5432/billing?sslmode=require
spring.datasource.username billing
spring.datasource.password=
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
management.endpoints.web.exposure.include=health,info,\\
    prometheus,\\
    metrics
logging.pattern.console=%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n
app.greeting=Grüße aus Köln
app.windows-path=C:\\\\billing\\\\data
app.regex=^\\\\d{3}-\\\\d{4}$
app.key\\ with\\ spaces=spaced key
app.equals\\=sign=value with = inside
app.colon\\:key=value: with colon
app.tab\\tkey=tab in key
server.port=9443
app.empty
  app.indented   =   leading spaces are dropped
app.trailing=trailing spaces kept   
app.unicode=caf\\u00e9 \\u263a \\uD83D\\uDE00
app.newline=first\\nsecond\\tthird\\rfourth\\fform
app.literal-backslash=\\q\\z
"""

GERMAN = """\
# Benutzeroberfläche
greeting=Grüß Gott
farewell=Auf Wiedersehen, bis später!
price=Preis: 12,50 €
"""

JAPANESE = """\
# native2ascii output
greeting=\\u3053\\u3093\\u306b\\u3061\\u306f
farewell=\\u3055\\u3088\\u3046\\u306a\\u3089
title=\\u8a2d\\u5b9a
"""

GRADLE = """\
org.gradle.jvmargs=-Xmx2g -XX:MaxMetaspaceSize=512m \\
    -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
android.useAndroidX=true
kotlin.code.style=official
"""

LOG4J = """\
log4j.rootLogger=INFO, stdout, R
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=%5p [%t] (%F:%L) - %m%n
log4j.appender.R=org.apache.log4j.RollingFileAppender
log4j.appender.R.File=/var/log/app/app.log
log4j.appender.R.MaxFileSize=100KB
log4j.appender.R.MaxBackupIndex=5
log4j.logger.com.example.db=DEBUG
"""

META = """\
#: owner=platform-team
#: since=2.4
feature.checkout.enabled=true
# documentation for the checkout flag
#   indented doc line
feature.search.enabled=false
#:deprecated=yes
#: replacement=feature.search.v2
feature.search.legacy=true
! a bang comment after the legacy flag
#: orphan=this metadata has no key after it
"""

EDGE = (
    "   \n"
    "\t\x0c\n"
    "key1\tvalue after tab\n"
    "key2\x0cvalue after form feed\n"
    "key3=\n"
    "key4\n"
    "=value with empty key\n"
    ":another empty key\n"
    "multi=one \\\n"
    "  two \\\n"
    "\n"
    "after=blank line ended the continuation\n"
    "continued\\\n"
    "  key = continued key\n"
    "crlf=line one \\\r\n"
    "   line two\r\n"
    "cronly=a\rnext=b\r"
    "dup=first\n"
    "dup=second\n"
    "hexquirks=\\u0x41\\u 42 \\u4_1a\\u+04a\\u0X_5\n"
    "bom=a\\uFEFFb\\uFFFEc\n"
    "backslash-eof=value\\"
)

ENDS = "no.newline.at.end=yes"

BROKEN = {
    "badunicode.properties": "a=ok\nb=\\u12g4\n",
    "shortunicode.properties": "a=\\u12",
    "highonly.properties": "a=\\uD83D and more\n",
    "highthenhigh.properties": "a=\\uD83D\\uD83D\n",
    "lowonly.properties": "a=\\uDE00\n",
    "highbad.properties": "a=\\uD83D\\uZZZZ\n",
    "emptymeta.properties": "#: =x\nkey=value\n",
    "keyunicode.properties": "k\\uXYZ1=v\n",
    "udecode.properties": "a=\\u00\xff1\n",
    "udecode2.properties": "a=\\uD83D\\uDE\xff\n",
}


def main():
    shutil.rmtree(DATA, ignore_errors=True)
    put("application.properties", SPRING.encode("utf-8"))
    put("messages_de.properties", GERMAN.encode("iso-8859-1", errors="strict").replace(b"\x80", b"") if False else GERMAN.replace("€", "EUR").encode("iso-8859-1"))
    put("messages_de_utf8.properties", GERMAN.encode("utf-8"))
    put("messages_ja.properties", JAPANESE.encode("ascii"))
    put("gradle.properties", GRADLE.encode("ascii"))
    put("log4j.properties", LOG4J.encode("ascii"))
    put("meta.properties", META.encode("ascii"))
    put("edge.properties", EDGE.encode("ascii"))
    put("noeol.properties", ENDS.encode("ascii"))
    put("empty.properties", b"")
    put("truncated.properties", "name=caf\u00e9".encode("utf-8")[:-1])
    put("badbyte.properties", b"name=ok\nbad=\xff\n")
    for name, text in BROKEN.items():
        put("broken/" + name, text.encode("latin-1"))

    good = ["application.properties", "messages_de_utf8.properties", "messages_ja.properties",
            "gradle.properties", "log4j.properties", "meta.properties", "edge.properties",
            "noeol.properties", "empty.properties", "truncated.properties"]
    jobs = []
    for g in good:
        jobs.append(["load", g, "utf-8"])
    jobs += [
        ["load", "messages_de.properties", "iso-8859-1"],
        ["load", "messages_de.properties", "utf-8"],
        ["load", "messages_de_utf8.properties", "iso-8859-1"],
        ["load", "badbyte.properties", "utf-8"],
        ["load", "badbyte.properties", "ascii"],
        ["load", "application.properties", "utf-8", "noescape"],
        ["load", "edge.properties", "utf-8", "noescape"],
        ["load", "meta.properties", "utf-8", "metadoc"],
    ]
    for name in sorted(BROKEN):
        jobs.append(["load", "broken/" + name, "utf-8"])
    for g in ["application.properties", "edge.properties", "meta.properties", "messages_ja.properties"]:
        jobs.append(["store", g, "utf-8", "iso-8859-1", "strict"])
        jobs.append(["store", g, "utf-8", "utf-8", "loose"])
    jobs += [
        ["store", "application.properties", "utf-8", "ascii", "loose"],
        ["store", "application.properties", "utf-8", "iso-8859-1", "loose"],
        ["store", "application.properties", "utf-8", "utf-8", "loose", "noescape"],
        ["store", "edge.properties", "utf-8", "utf-8", "strict", "noescape"],
        ["store", "meta.properties", "utf-8", "utf-8", "loose", "meta"],
        ["store", "meta.properties", "utf-8", "utf-8", "loose", "meta", "metadoc"],
        ["store", "gradle.properties", "utf-8", "utf-8", "loose", "comments=Built by CI\\r\\nDo not edit\\n#keep\\n:colon line\\r!bang"],
        ["store", "log4j.properties", "utf-8", "latin-1", "strict", "comments=Logging für Prod"],
        ["edit", "application.properties", "set:server.port=10443", "set:new.key=new value", "del:app.empty",
         "set:app.empty=back", "set:  spaced=  two leading", "meta:server.port:owner=ops,__runtime=hidden"],
        ["edit", "meta.properties", "del:feature.search.legacy", "del:missing.key"],
        ["edit", "empty.properties", "set:z=last", "set:a=first", "set:m=middle"],
        ["tool", "application.properties"],
        ["tool", "messages_de.properties", "iso-8859-1", "ascii"],
        ["tool", "messages_ja.properties", "utf-8", "iso-8859-1"],
        ["tool", "edge.properties", "utf-8", "utf-8", "false"],
        ["tool", "broken/highonly.properties"],
        ["tool", "badbyte.properties"],
        ["tool", "gradle.properties", "nope"],
        ["tool", "gradle.properties", "utf-8", "nope"],
        ["tool", "missing.properties"],
        ["tool", "-h"],
        ["tool"],
    ]
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as f:
        for j in jobs:
            f.write("\t".join(j) + "\n")


main()
