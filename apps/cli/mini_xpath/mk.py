# Writes data/: the documents, the XPath queries over them and the
# xmlstarlet sel jobs. Run it from the app directory.
import os

DOCS = {}

DOCS["books.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<!-- A small shop's catalogue. -->
<catalog updated="2026-03-01">
  <book id="bk101" category="programming" lang="en">
    <title>Structure and Interpretation of Computer Programs</title>
    <author>Harold Abelson</author>
    <author>Gerald Jay Sussman</author>
    <year>1985</year>
    <price currency="EUR">45.50</price>
    <stock>3</stock>
  </book>
  <book id="bk102" category="programming" lang="en">
    <title>The C Programming Language</title>
    <author>Brian Kernighan</author>
    <author>Dennis Ritchie</author>
    <year>1978</year>
    <price currency="EUR">39.99</price>
    <stock>0</stock>
  </book>
  <book id="bk103" category="fiction" lang="fr">
    <title>L'Étranger</title>
    <author>Albert Camus</author>
    <year>1942</year>
    <price currency="EUR">8.90</price>
    <stock>12</stock>
  </book>
  <book id="bk104" category="fiction" lang="de">
    <title>Der Prozeß</title>
    <author>Franz Kafka</author>
    <year>1925</year>
    <price currency="CHF">11</price>
    <stock>5</stock>
    <!-- out of print in this edition -->
  </book>
  <book id="bk105" category="reference">
    <title>  The   Chicago Manual
      of Style  </title>
    <year>2017</year>
    <price currency="USD">n/a</price>
  </book>
  <magazine id="mg1" category="programming">
    <title>Linux Journal</title>
    <issue>2026-02</issue>
    <price currency="EUR">6.5</price>
  </magazine>
</catalog>
"""

DOCS["feed.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:media="http://search.yahoo.com/mrss/" xml:lang="en">
  <title type="text">Example Engineering Blog</title>
  <link rel="self" href="https://blog.example.org/feed.xml"/>
  <link rel="alternate" type="text/html" href="https://blog.example.org/"/>
  <updated>2026-03-02T09:00:00Z</updated>
  <entry>
    <title>Shipping a parser</title>
    <link href="https://blog.example.org/posts/parser"/>
    <id>tag:blog.example.org,2026:1</id>
    <dc:creator>Ana Lima</dc:creator>
    <dc:subject>compilers</dc:subject>
    <dc:subject>testing</dc:subject>
    <updated>2026-03-01T12:00:00Z</updated>
    <media:thumbnail url="https://cdn.example.org/1.png" width="320" height="180"/>
    <content type="html">&lt;p&gt;We rewrote the parser.&lt;/p&gt;</content>
  </entry>
  <entry xml:lang="pt-BR">
    <title>Notas de versão</title>
    <link href="https://blog.example.org/posts/notas"/>
    <id>tag:blog.example.org,2026:2</id>
    <dc:creator>João Silva</dc:creator>
    <dc:subject>releases</dc:subject>
    <updated>2026-02-20T08:30:00Z</updated>
    <media:thumbnail url="https://cdn.example.org/2.png" width="640" height="360"/>
  </entry>
  <entry>
    <title>On-call, a year later</title>
    <link href="https://blog.example.org/posts/oncall"/>
    <id>tag:blog.example.org,2026:3</id>
    <dc:creator>Ana Lima</dc:creator>
    <updated>2026-01-15T17:45:00Z</updated>
  </entry>
</feed>
"""

DOCS["page.xhtml"] = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <title>Status - Example Services</title>
  <meta name="description" content="Service status and incidents"/>
  <link rel="stylesheet" href="/static/site.css"/>
</head>
<body class="status page">
  <nav><a href="/">Home</a> | <a href="/incidents">Incidents</a> | <a href="https://docs.example.org/">Docs</a></nav>
  <h1>All systems <em>mostly</em> operational</h1>
  <table id="services">
    <tr><th>Service</th><th>Region</th><th>Uptime</th></tr>
    <tr class="ok"><td>api</td><td>eu-west</td><td>99.98</td></tr>
    <tr class="ok"><td>api</td><td>us-east</td><td>99.95</td></tr>
    <tr class="degraded"><td>search</td><td>eu-west</td><td>97.20</td></tr>
    <tr class="ok"><td>billing</td><td>eu-west</td><td>100</td></tr>
    <tr class="down"><td>reports</td><td>us-east</td><td>88.5</td></tr>
  </table>
  <form action="/subscribe" method="post">
    <input type="email" name="email" required="required"/>
    <input type="hidden" name="token" value="form-1234"/>
    <select name="freq"><option value="d">daily</option><option value="w" selected="selected">weekly</option></select>
    <button type="submit">Subscribe</button>
  </form>
  <p>Last checked <time datetime="2026-03-02T10:15:00Z">10:15</time>. <!-- generated --><?render cache="5m"?>See <a href="/history">history</a>.</p>
</body>
</html>
"""

DOCS["pom.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.example</groupId>
  <artifactId>orders-service</artifactId>
  <version>2.4.1-SNAPSHOT</version>
  <packaging>jar</packaging>
  <properties>
    <java.version>21</java.version>
    <jackson.version>2.17.0</jackson.version>
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
      <version>42.7.3</version>
      <scope>runtime</scope>
    </dependency>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.10.2</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.mockito</groupId>
      <artifactId>mockito-core</artifactId>
      <version>5.11.0</version>
      <scope>test</scope>
      <optional>true</optional>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.2.5</version>
        <configuration><skipTests>false</skipTests></configuration>
      </plugin>
    </plugins>
  </build>
</project>
"""

DOCS["inventory.xml"] = """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="report.xsl"?>
<inventory xmlns:w="urn:example:warehouse" w:site="DUB-2">
  <w:bin code="A-01" w:zone="cold">
    <item sku="MILK-1L" qty="40" unit-price="1.15"/>
    <item sku="YOG-500" qty="12" unit-price="2.4"/>
  </w:bin>
  <w:bin code="A-02" w:zone="cold">
    <item sku="BUT-250" qty="0" unit-price="2.95"/>
  </w:bin>
  <w:bin code="B-07" w:zone="dry">
    <item sku="RICE-5K" qty="7" unit-price="9.99"/>
    <item sku="OATS-1K" qty="25" unit-price="3"/>
    <item sku="SALT-1K" qty="-2" unit-price="0.5"/>
    <item sku="SUGAR-1K" unit-price="1.1"/>
  </w:bin>
  <note xml:lang="en">Counted on <date>2026-03-01</date>; recount B-07.</note>
</inventory>
"""

# Each section names a document, the namespace prefixes its queries use
# and the variables they can read.
QUERIES = [
    ("books.xml", {}, {"min": 10, "cat": "fiction", "flag": True}, [
        "/catalog/book/title",
        "//book[@category='fiction']/title/text()",
        "//book[price > 20]/@id",
        "//book[not(price > 20)]/@id",
        "//book[price != 11]/@id",
        "count(//book)",
        "count(//author)",
        "count(//*)",
        "count(//node())",
        "count(//text())",
        "sum(//book/stock)",
        "sum(//price)",
        "sum(//book[stock]/price)",
        "string(sum(//book[number(price) = number(price)]/price))",
        "//book[last()]/title",
        "//book[position() = last() - 1]/@id",
        "//book[2]",
        "(//author)[2]",
        "//book/author[2]",
        "//book[author[2]]/@id",
        "//book[count(author) = 1]/title",
        "//book[@lang]/@lang",
        "//book[not(@lang)]/@id",
        "//*[@category='programming'][self::magazine]/title",
        "//book[year < 1950][price < 10]/@id",
        "//book[year < 1950 and price < 10]/@id",
        "//book[year > 2000 or stock = 0]/@id",
        "//book[stock > 4 or not(stock)]/@id",
        "name(/*)",
        "local-name(//book[1]/@*[2])",
        "//book[1]/@*",
        "//title[contains(., 'Program')]",
        "//title[starts-with(., 'The')]/../@id",
        "normalize-space(//book[@id='bk105']/title)",
        "string-length(//book[@id='bk103']/title)",
        "substring-before(//book[1]/author[2], ' ')",
        "substring-after(//book[1]/author[2], ' ')",
        "substring(//book[2]/title, 5)",
        "substring(//book[2]/title, 5, 3)",
        "translate(//book[3]/title, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')",
        "concat(//book[1]/@id, ':', //book[1]/year, ':', //book[1]/price)",
        "//book[1]/year + 1",
        "//book[1]/year - //book[2]/year",
        "//book[1]/price * 2",
        "//book[1]/price div 4",
        "//book[1]/year mod 100",
        "-//book[1]/year",
        "//book[@id='bk105']/price * 1",
        "number(//book[@id='bk105']/price) = number(//book[@id='bk105']/price)",
        "//price[. = 39.99]/../@id",
        "//price[. = '6.5']/..",
        "//book/stock[. = 0] | //magazine/title",
        "//magazine | //book[1] | //book[1]/title",
        "//book[1]/following-sibling::book/@id",
        "//book[3]/preceding-sibling::*/@id",
        "//book[3]/preceding-sibling::*[1]/@id",
        "//book[3]/following-sibling::*[last()]/@id",
        "//year[. = 1942]/ancestor::*",
        "//year[. = 1942]/ancestor-or-self::*/@id",
        "//book[4]/descendant::node()",
        "//book[4]/descendant-or-self::comment()",
        "//comment()",
        "/comment()",
        "/node()",
        "//book[2]/price/following::title",
        "//book[4]/title/preceding::author",
        "//book[4]/title/preceding::author[1]",
        "//stock/parent::book/@id",
        "//title/..[self::magazine]/@id",
        "//book[1]/title/self::node()",
        "//book[1]/child::*[3]",
        "//book[1]/attribute::category",
        "boolean(//book[stock > 100])",
        "boolean(//book[stock > 10])",
        "not(//magazine)",
        "//book[@category = $cat]/@id",
        "//book[stock > $min]/@id",
        "$flag and $min > 5",
        "concat($cat, '-', $min)",
        "$missing",
        "//book[lang('en')]/@id",
        "//*[@id][position() mod 2 = 0]/@id",
        "//book[position() > 2 and position() < 5]/@id",
        "//book/@id[. = 'bk102' or . = 'bk104']",
        "count(//book[@category='programming']) * 10 div count(//book)",
        "round(//book[1]/price)",
        "floor(//book[1]/price)",
        "ceiling(//book[1]/price)",
        "round(-2.5)",
        "round(0.5)",
        "round(-0.4)",
        "1 div 3",
        "2 div 3",
        "string(1 div 3)",
        "string(100 div 7)",
        "string(2 div 3 * 1000000)",
        "string(123456789.123)",
        "string(1234567890)",
        "string(1234567890.5)",
        "string(12345678901234567)",
        "string(0.00001)",
        "string(0.000012345)",
        "string(0.000001)",
        "string(-0.25)",
        "string(3.0)",
        "string(-0)",
        "string(1 div 0)",
        "string(-1 div 0)",
        "string(0 div 0)",
        "1 div 0",
        "0 div 0",
        "-0",
        "number('  12  ')",
        "number('12px')",
        "number('-.5')",
        "number('')",
        "number(true())",
        "number(//book[1]/@id)",
        "string(true())",
        "string(//nothing)",
        "boolean('')",
        "boolean('0')",
        "boolean(0)",
        "boolean(0 div 0)",
        "true() = 'x'",
        "1 = '1.0'",
        "'1' = '1.0'",
        "//year = 1978",
        "//year != 1978",
        "//year > //stock",
        "//book[1]/author = //book[2]/author",
        "//book[1]/author != //book[1]/author",
        "//nothing = //nothing",
        "//nothing != 1",
        "not(//nothing = 1)",
        "1 < 2 < 3",
        "3 > 2 > 1",
        "2 = 2 = 1",
        "1 - - 1",
        "- - 3",
        "1 -1",
        "5 mod -3",
        "-5 mod 3",
        "5.5 mod 2",
        "7 div 2 * 2",
        "2 + 3 * 4 - 1",
        "(2 + 3) * 4",
        "concat('a', 1, true(), 1 div 0)",
        "translate('banana', 'an', 'A')",
        "translate('--x--', '-', '')",
        "substring('12345', 1.5, 2.6)",
        "substring('12345', 0, 3)",
        "substring('12345', 0 div 0, 3)",
        "substring('12345', 1, 0 div 0)",
        "substring('12345', -42, 1 div 0)",
        "substring('12345', -1 div 0, 1 div 0)",
        "substring('été', 2, 1)",
        "string-length('naïve')",
        "string-length()",
        "normalize-space()",
        "normalize-space('\t a \t b  ')",
        "starts-with('abc', '')",
        "contains('', '')",
        "substring-before('abc', '')",
        "substring-after('abc', '')",
        "substring-after('a=b=c', '=')",
        "name(//book[1]/title/text())",
        "name()",
        "local-name()",
        "namespace-uri()",
        "count(//book[1]/node())",
        "count(//book[1]/text())",
        "//book[1]/text()[1]",
        "//book[4]/comment()/preceding-sibling::text()[1]",
        "//title/text()[contains(., 'Style')]",
        "//*[text()[. = 'Franz Kafka']]",
        "//*[.='1985']",
        "//book[title = 'The C Programming Language']/author[last()]",
        "//book[.//price/@currency = 'CHF']/@id",
        "//price/@currency[. != 'EUR']",
        "//@currency[../../@lang = 'fr']",
        "//book//text()[normalize-space()][1]",
        ".",
        "..",
        "/",
        "/*/*[1]/@*[last()]",
        "*[2]/title",
        "book[@id='bk104']/descendant::*",
        "@updated",
        "./@updated",
        "id('bk101')",
        "count(1)",
        "//book[",
        "//book[@id='x']]",
        "1 +",
        "foo()",
        "count()",
        "concat('a')",
        "//x:book",
        "//book/@",
        "'unterminated",
        "//book[1]/title/nonsense::x",
        "2 ** 3",
        "//book[@id=\"bk101\"]/title",
        "//*[contains(name(), 'a')][1]",
    ]),
    ("feed.xml", {"a": "http://www.w3.org/2005/Atom", "dc": "http://purl.org/dc/elements/1.1/", "m": "http://search.yahoo.com/mrss/"}, {}, [
        "/a:feed/a:title",
        "string(/a:feed/a:title)",
        "/feed/title",
        "//a:entry/a:title/text()",
        "//a:entry[dc:creator = 'Ana Lima']/a:id/text()",
        "//a:entry[not(dc:subject)]/a:title/text()",
        "count(//dc:subject)",
        "//a:link[@rel='self']/@href",
        "//a:link[not(@rel)]/@href",
        "//a:entry[a:updated > '2026-02']/a:title/text()",
        "//a:entry[starts-with(a:updated, '2026-02')]/a:title/text()",
        "//m:thumbnail[@width > 400]/@url",
        "sum(//m:thumbnail/@width) div count(//m:thumbnail)",
        "//a:entry[lang('pt')]/a:id/text()",
        "//a:entry[lang('en')]/a:id/text()",
        "//a:entry[lang('EN')]/a:id/text()",
        "//dc:*",
        "//a:*[local-name() = 'id']/text()",
        "name(//dc:creator)",
        "local-name(//dc:creator)",
        "namespace-uri(//dc:creator)",
        "namespace-uri(/*)",
        "name(/*)",
        "//*[namespace-uri() = 'http://search.yahoo.com/mrss/']/@height",
        "//a:entry[1]/namespace::*",
        "count(/*/namespace::*)",
        "//a:content/text()",
        "string-length(//a:content)",
        "//@xml:lang",
        "//a:entry[@xml:lang]/a:title/text()",
        "//a:entry/a:title[../dc:subject = 'testing']/text()",
        "//a:entry[last()]/preceding-sibling::a:entry[1]/a:id/text()",
        "//a:entry[dc:creator = //a:entry[2]/dc:creator]/a:id/text()",
        "//a:entry[dc:creator = preceding-sibling::a:entry/dc:creator]/a:title/text()",
        "//xx:entry",
    ]),
    ("page.xhtml", {"h": "http://www.w3.org/1999/xhtml"}, {"region": "eu-west"}, [
        "string(//h:title)",
        "//h:meta[@name='description']/@content",
        "//h:a/@href",
        "//h:a[starts-with(@href, 'http')]/@href",
        "//h:a[not(starts-with(@href, 'http'))]/text()",
        "//h:nav/text()",
        "normalize-space(//h:h1)",
        "//h:h1/node()",
        "//h:tr[h:td]/h:td[1]/text()",
        "//h:tr[@class != 'ok']/h:td[1]/text()",
        "//h:tr[h:td[3] < 99]/h:td[1]/text()",
        "count(//h:tr[h:td[2] = $region])",
        "//h:tr[h:td[2] = $region][h:td[3] >= 99]/h:td[1]/text()",
        "sum(//h:tr/h:td[3]) div count(//h:tr/h:td[3])",
        "//h:td[. = 'api']/following-sibling::h:td[2]/text()",
        "//h:tr[last()]/h:td[position() > 1]/text()",
        "//h:th[2]/following-sibling::*",
        "//h:tr[2]/@class | //h:tr[4]/@class",
        "//h:body/@class",
        "//*[contains(concat(' ', normalize-space(@class), ' '), ' page ')]",
        "//h:input[@type='hidden']/@value",
        "//h:input[@required]/@name",
        "//h:option[@selected]/@value",
        "string(//h:option[@selected])",
        "//h:form/@*",
        "//h:p/node()",
        "//h:p/comment()",
        "//h:p/processing-instruction()",
        "//processing-instruction('render')",
        "string(//processing-instruction())",
        "name(//processing-instruction())",
        "//h:p/text()[2]",
        "//h:time/@datetime",
        "//h:p/h:a/preceding-sibling::node()[1]",
        "count(//h:p/node()[self::text()])",
        "//h:td[not(. = preceding::h:td)][parent::h:tr/h:td[1] = .]/text()",
        "count(//*)",
        "count(//@*)",
        "/h:html/@lang",
    ]),
    ("pom.xml", {"p": "http://maven.apache.org/POM/4.0.0", "xsi": "http://www.w3.org/2001/XMLSchema-instance"}, {}, [
        "concat(/p:project/p:groupId, ':', /p:project/p:artifactId, ':', /p:project/p:version)",
        "//p:dependency/p:artifactId/text()",
        "//p:dependency[p:scope = 'test']/p:artifactId/text()",
        "//p:dependency[not(p:scope)]/p:artifactId/text()",
        "//p:dependency[p:optional = 'true']/p:artifactId/text()",
        "count(//p:dependency)",
        "//p:dependency[starts-with(p:version, '${')]/p:version/text()",
        "//p:properties/*",
        "name(//p:properties/*[1])",
        "local-name(//p:properties/*[2])",
        "/p:project/@xsi:schemaLocation",
        "substring-before(/p:project/@xsi:schemaLocation, ' ')",
        "//p:plugin[p:artifactId = 'maven-surefire-plugin']/p:configuration/p:skipTests/text()",
        "contains(/p:project/p:version, 'SNAPSHOT')",
        "//p:dependency[p:version > 5]/p:artifactId/text()",
        "//p:dependency[number(substring-before(p:version, '.')) >= 5]/p:artifactId/text()",
        "//p:*[not(*)][normalize-space() = '']",
        "//p:version",
    ]),
    ("inventory.xml", {"w": "urn:example:warehouse"}, {"zone": "cold"}, [
        "//w:bin/@code",
        "//w:bin[@w:zone = $zone]/item/@sku",
        "sum(//item/@qty)",
        "sum(//w:bin[@w:zone='cold']/item/@qty)",
        "count(//item[@qty > 0])",
        "count(//item[not(@qty)])",
        "//item[@qty < 1]/@sku",
        "//item[@qty * @unit-price > 30]/@sku",
        "//item[not(@qty * @unit-price > 30)]/@sku",
        "//w:bin[sum(item/@qty) > 20]/@code",
        "//w:bin[count(item) = 1]/@code",
        "//w:bin[item[@qty = 0]]/@code",
        "//item[@sku = 'OATS-1K']/@unit-price * 2",
        "//item[@sku = 'SUGAR-1K']/@qty * 2",
        "sum(//item/@unit-price)",
        "round(sum(//item/@unit-price) * 100) div 100",
        "/processing-instruction()",
        "name(/processing-instruction())",
        "string(/processing-instruction('xml-stylesheet'))",
        "/inventory/@w:site",
        "//@w:*",
        "name(//@w:zone)",
        "//w:bin[1]/@*",
        "//note/text()",
        "//note/node()",
        "string(//note)",
        "//note[lang('en-US')]",
        "//note[lang('en')]/date/text()",
        "//date[lang('en')]",
        "//item[1]/namespace::w",
        "//*[@code = 'B-07']/item[last()]/@sku",
        "//item[@sku][@qty][2]/@sku",
        "(//item[@qty])[last()]/@sku",
        "//w:bin[2]/following-sibling::*/@code | //w:bin[2]/preceding-sibling::*/@code",
        "//item[@qty = //item/@qty[. > 30]]/@sku",
        "//item[@qty > //item[@sku='OATS-1K']/@qty]/@sku",
    ]),
]

# xmlstarlet sel: each job is a document and the arguments after it.
SEL = [
    ("books.xml", ["-t", "-m", "//book", "-v", "@id", "-o", ": ", "-v", "title", "-n"]),
    ("books.xml", ["-t", "-m", "//book", "-s", "D:N:-", "price", "-v", "price", "-o", " ", "-v", "@id", "-n"]),
    ("books.xml", ["-t", "-m", "//book", "-s", "A:T:-", "title", "-v", "position()", "-o", "/", "-v", "last()", "-o", " ", "-v", "normalize-space(title)", "-n"]),
    ("books.xml", ["-t", "-m", "//book[author]", "-v", "@id", "-o", ":", "-m", "author", "-o", " ", "-v", "position()", "-o", "=", "-v", ".", "-b", "-n"]),
    ("books.xml", ["-t", "-m", "//book", "-i", "stock = 0", "-v", "@id", "-o", " sold out", "-n", "-b", "-i", "not(stock)", "-v", "@id", "-o", " no stock line", "-n"]),
    ("books.xml", ["-t", "-v", "count(//book)", "-o", " books, ", "-v", "sum(//stock)", "-o", " copies", "-n"]),
    ("books.xml", ["-t", "-m", "//book", "-s", "A:T:-", "@category", "-s", "D:N:-", "year", "-v", "@category", "-o", " ", "-v", "year", "-n"]),
    ("books.xml", ["-t", "-c", "//book[1]/title", "-n", "-c", "//book[4]/comment()", "-n"]),
    ("feed.xml", ["-N", "a=http://www.w3.org/2005/Atom", "-N", "dc=http://purl.org/dc/elements/1.1/", "-t", "-m", "//a:entry", "-s", "A:T:-", "a:updated", "-v", "substring(a:updated, 1, 10)", "-o", " ", "-v", "a:title", "-o", " (", "-v", "count(dc:subject)", "-o", " tags)", "-n"]),
    ("feed.xml", ["-N", "a=http://www.w3.org/2005/Atom", "-t", "-m", "//a:entry[position() = last()]", "-v", "a:link/@href", "-n"]),
    ("page.xhtml", ["-N", "h=http://www.w3.org/1999/xhtml", "-t", "-m", "//h:tr[h:td]", "-s", "A:N:-", "h:td[3]", "-v", "h:td[1]", "-o", "@", "-v", "h:td[2]", "-o", " ", "-v", "h:td[3]", "-i", "@class != 'ok'", "-o", " !", "-b", "-n"]),
    ("page.xhtml", ["-N", "h=http://www.w3.org/1999/xhtml", "-t", "-m", "//h:a", "-v", "concat(position(), ' ', @href)", "-n"]),
    ("pom.xml", ["-N", "p=http://maven.apache.org/POM/4.0.0", "-t", "-m", "//p:dependency", "-s", "A:T:-", "p:scope", "-v", "p:groupId", "-o", ":", "-v", "p:artifactId", "-o", ":", "-v", "p:version", "-i", "p:scope", "-o", " [", "-v", "p:scope", "-o", "]", "-b", "-n"]),
    ("inventory.xml", ["-N", "w=urn:example:warehouse", "-t", "-m", "//w:bin", "-v", "@code", "-o", " ", "-v", "sum(item/@qty)", "-o", " units, value ", "-v", "round(sum(item/@qty) * 100) div 100", "-n", "-m", "item", "-s", "D:N:-", "@qty", "-o", "  ", "-v", "@sku", "-o", " x", "-v", "@qty", "-n"]),
]


def main():
    os.makedirs("data/docs", exist_ok=True)
    for name, text in DOCS.items():
        with open("data/docs/" + name, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    with open("data/queries.txt", "w", encoding="utf-8", newline="") as f:
        for doc, nss, vars_, qs in QUERIES:
            f.write("doc %s\n" % doc)
            for p, u in nss.items():
                f.write("ns %s %s\n" % (p, u))
            for k, v in vars_.items():
                kind = "bool" if isinstance(v, bool) else "num" if isinstance(v, (int, float)) else "str"
                f.write("var %s %s %s\n" % (kind, k, v))
            for q in qs:
                f.write("q %s\n" % q)
    with open("data/sel.tsv", "w", encoding="utf-8", newline="") as f:
        for doc, args in SEL:
            f.write("\t".join([doc] + args) + "\n")


main()
