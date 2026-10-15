# Writes the XML documents and the queries into data/.
import os
os.makedirs("data/bad", exist_ok=True)
docs = {}
docs["feed.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<!-- the release feed -->
<?xml-stylesheet type="text/xsl" href="feed.xsl"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Kara Releases</title>
    <link>https://example.org/releases</link>
    <atom:link href="https://example.org/feed.xml" rel="self" type="application/rss+xml"/>
    <description>News &amp; releases from the Kara project &#8212; weekly</description>
    <item>
      <title>Version 0.9 &#x2014; &quot;MIR everywhere&quot;</title>
      <link>https://example.org/releases/0.9</link>
      <dc:creator>Gowtham</dc:creator>
      <category>compiler</category>
      <category>release</category>
      <pubDate>Wed, 14 Oct 2026 09:00:00 GMT</pubDate>
      <description><![CDATA[<p>The <b>MIR</b> backend is now the default & legacy is frozen.</p>]]></description>
    </item>
    <item>
      <title>Version 0.8</title>
      <link>https://example.org/releases/0.8</link>
      <dc:creator>Release bot</dc:creator>
      <category>release</category>
      <pubDate>Mon, 05 Oct 2026 09:00:00 GMT</pubDate>
      <description>Bugs fixed: 41. It&apos;s <!-- not shown -->faster.</description>
      <enclosure url="https://example.org/kara-0.8.tar.gz" length="1048576" type="application/gzip"/>
    </item>
    <item>
      <title>Security notice</title>
      <link>https://example.org/notices/1</link>
      <category>security</category>
      <description>Upgrade to 0.8.1 if you use &lt;TaskGroup&gt;.</description>
    </item>
  </channel>
</rss>
"""
docs["pom.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.example</groupId>
  <artifactId>orders-service</artifactId>
  <version>2.3.1-SNAPSHOT</version>
  <properties>
    <java.version>21</java.version>
    <jackson.version>2.17.2</jackson.version>
  </properties>
  <dependencies>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>${jackson.version}</version>
    </dependency>
    <dependency>
      <groupId>org.postgresql</groupId>
      <artifactId>postgresql</artifactId>
      <version>42.7.4</version>
      <scope>runtime</scope>
    </dependency>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.11.0</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>
"""
docs["icon.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="64" height="64" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff6a00"/><stop offset="1" stop-color="#ee0979"/></linearGradient>
  </defs>
  <g id="layer1" transform="translate(4 4)">
    <circle cx="28" cy="28" r="26" fill="url(#g1)"/>
    <path d="M16 40 L28 14 L40 40 Z" fill="none" stroke="white" stroke-width="3"/>
    <use xlink:href="#g1" x="2"/>
    <text x="32" y="60" font-size="8" text-anchor="middle">k&#257;ra</text>
  </g>
</svg>
"""
docs["config.xml"] = """<?xml version="1.0"?>
<!DOCTYPE config [
  <!ENTITY company "Acme &amp; Sons">
  <!ENTITY env "production">
]>
<config env="&env;" owner='&company;'>
  <server host="0.0.0.0" port="8443" tls="on">
    <timeout unit="s">30</timeout>
    <limits connections="1024"
            requests-per-second="250"/>
  </server>
  <database url="postgres://db:5432/orders" pool="20">primary</database>
  <database url="postgres://replica:5432/orders" pool="5" readonly="true">replica</database>
  <feature name="beta-ui" enabled="false"/>
  <feature name="new-pricing" enabled="true">rollout 25%</feature>
  <banner>Welcome to &company;.	Tabs and
new lines are kept.</banner>
  <note attr="line one
line two&#10;three	tab"/>
</config>
"""
docs["sitemap.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.org/</loc><lastmod>2026-10-01</lastmod><priority>1.0</priority></url>
  <url><loc>https://example.org/docs/</loc><lastmod>2026-10-12</lastmod><priority>0.8</priority></url>
  <url><loc>https://example.org/docs/ownership</loc><lastmod>2026-09-30</lastmod></url>
  <url><loc>https://example.org/blog/?page=2&amp;sort=new</loc><priority>0.3</priority></url>
</urlset>
"""
bad = {
    "mismatch.xml": "<a><b></a></b>\n",
    "unclosed.xml": "<root>\n  <child>text</child>\n",
    "empty.xml": "",
    "junk.xml": "<a/>\n<b/>\n",
    "entity.xml": "<a>&nosuch;</a>\n",
    "dupattr.xml": '<a x="1" x="2"/>\n',
    "badtoken.xml": "<a>1 < 2</a>\n",
    "badname.xml": "<1a/>\n",
    "prefix.xml": "<x:a/>\n",
    "charref.xml": "<a>&#0;</a>\n",
    "decl.xml": '\n<?xml version="1.0"?><a/>\n',
    "attrlt.xml": '<a x="<"/>\n',
    "noquote.xml": "<a x=1/>\n",
    "amp.xml": "<a>fish & chips</a>\n",
    "unterminated.xml": "<a><!-- comment</a>\n",
    "text.xml": "just text\n",
    "cdata.xml": "<a>]]></a>\n",
    "close.xml": "<a></a >\n<b></b\n",
}
for name, text in docs.items():
    open("data/" + name, "w", encoding="utf-8").write(text)
for name, text in bad.items():
    open("data/bad/" + name, "w", encoding="utf-8").write(text)
queries = """feed.xml|findtext|channel/title
feed.xml|findall|channel/item/title
feed.xml|findall|.//category
feed.xml|findall|.//item[category='release']/link
feed.xml|findall|channel/item[2]/title
feed.xml|findall|channel/item[last()]/title
feed.xml|findall|.//{http://purl.org/dc/elements/1.1/}creator
feed.xml|findall|.//item[{http://purl.org/dc/elements/1.1/}creator]/title
feed.xml|find|.//enclosure
feed.xml|findall|.//*[@href]
feed.xml|findall|.//*[@rel='self']
feed.xml|findtext|.//item/description
feed.xml|findtext|.//nothing
feed.xml|findtext|channel/item[2]/description
feed.xml|itertext|channel/item[3]
feed.xml|findall|channel/*
feed.xml|findall|channel/item/..
pom.xml|findtext|{http://maven.apache.org/POM/4.0.0}artifactId
pom.xml|findall|.//{http://maven.apache.org/POM/4.0.0}dependency/{http://maven.apache.org/POM/4.0.0}artifactId
pom.xml|findall|.//{http://maven.apache.org/POM/4.0.0}dependency[{http://maven.apache.org/POM/4.0.0}scope='test']/{http://maven.apache.org/POM/4.0.0}artifactId
pom.xml|findall|artifactId
pom.xml|findall|{*}properties/*
pom.xml|findall|.//{*}version
icon.svg|findall|.//{http://www.w3.org/2000/svg}stop
icon.svg|findall|.//*[@fill]
icon.svg|findall|{http://www.w3.org/2000/svg}g/*[3]
icon.svg|findtext|.//{http://www.w3.org/2000/svg}text
config.xml|findall|database
config.xml|findall|database[@readonly]
config.xml|findall|feature[@enabled='true']
config.xml|findtext|server/timeout
config.xml|findall|.//limits
config.xml|findtext|banner
config.xml|findall|*[.='replica']
sitemap.xml|findall|{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc
sitemap.xml|findall|{*}url[{*}priority]/{*}loc
sitemap.xml|findall|{*}url[1]/*
"""
open("data/queries.txt", "w").write(queries)
