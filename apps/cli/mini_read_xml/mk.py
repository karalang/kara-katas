"""Writes data/: the XML documents the jobs read, each shaped like a file
a pipeline meets (a central bank's rate feed, a shop's order export, an
ISO 20022 bank statement, an OpenStreetMap extract, a sitemap, an RSS
feed, a weather station's readings in latin-1, a large catalogue for
iterparse), the broken files people meet, and data/jobs.txt, one job
per line. oracle.py runs each job on pandas' read_xml and to_xml,
mini_read_xml.kara on its own port.

Every value is made up; the IBANs are the documentation examples with
their check digits broken.

Run: python3 -s -P -B mk.py"""
import gzip
import io
import os
import random
import shutil
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
shutil.rmtree(DATA, ignore_errors=True)
os.makedirs(DATA)
rnd = random.Random(20261029)


def put(name, data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(os.path.join(DATA, name), "wb") as f:
        f.write(data)


# 1. The ECB's euro reference rates, as eurofxref-hist-90d.xml is laid
#    out: a gesmes envelope, a default namespace, and every value in an
#    attribute, the day on one Cube and the rates on the Cubes inside it.
CUR = [("USD", 1.08), ("JPY", 161.2), ("GBP", 0.855), ("CHF", 0.953),
       ("PLN", 4.31), ("INR", 89.9)]
days = ["2024-03-%02d" % d for d in (1, 4, 5)]
x = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01" '
     'xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">',
     '\t<gesmes:subject>Reference rates</gesmes:subject>',
     '\t<gesmes:Sender>', '\t\t<gesmes:name>European Central Bank</gesmes:name>',
     '\t</gesmes:Sender>', '\t<Cube>']
for d in days:
    x.append(f"\t\t<Cube time='{d}'>")
    for c, base in CUR:
        r = base * (1 + rnd.uniform(-0.01, 0.01))
        digits = 4 if base < 10 else (2 if base > 100 else 3)
        x.append(f"\t\t\t<Cube currency='{c}' rate='{r:.{digits}f}'/>")
    x.append("\t\t</Cube>")
x += ["\t</Cube>", "</gesmes:Envelope>", ""]
put("ecb_rates.xml", "\n".join(x))

# 2. A shop's order export: attributes and child elements on each order,
#    a nested item list (whose text is only indentation), an empty
#    element, entity and character references, a CDATA note, a comment
#    between two children, and one order missing fields.
NAMES = ["Zoë Ångström", "Marc O'Neil", "Søren Kjær", "Ana-María Ruiz",
         "李 小龍", "Chloé & Théo Martin", "Priya <Ops> Nair", "Olu Adeyemi"]
o = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<!-- exported 2024-04-02T06:00:00Z by shopctl 3.2 -->',
     '<orders store="eu-west" count="8">']
for i in range(8):
    nm = NAMES[i].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    status = ["paid", "shipped", "refunded", "paid", "pending", "shipped", "paid", "cancelled"][i]
    o.append(f'  <order id="SO-{10420 + i * 7}" status="{status}">')
    o.append(f"    <customer>{nm}</customer>")
    o.append(f"    <placed>2024-03-{(i * 3) % 28 + 1:02d}T{(i * 5) % 24:02d}:{(i * 13) % 60:02d}:00</placed>")
    if i == 3:
        o.append("    <!-- total recomputed after a partial refund -->")
    if i != 6:
        o.append(f'    <total currency="EUR">{rnd.uniform(9, 900):.2f}</total>')
    o.append(f"    <items>")
    for j in range(1 + i % 3):
        o.append(f'      <item sku="SKU-{100 + i * 10 + j}" qty="{1 + (i + j) % 4}"/>')
    o.append(f"    </items>")
    if i == 2:
        o.append("    <note><![CDATA[Customer wrote: \"box arrived <crushed>\" & asked for refund]]></note>")
    elif i == 5:
        o.append("    <note>Leave at door &#8212; <!-- gate code changed --> code 4417&#x2009;B</note>")
    else:
        o.append("    <note/>")
    o.append(f"    <gift>{'true' if i % 4 == 1 else 'false'}</gift>")
    o.append("  </order>")
o += ["</orders>", ""]
put("orders.xml", "\n".join(o))

# 3. An ISO 20022 camt.053 bank-to-customer statement, as a bank's API
#    hands it over: a default namespace, entries (Ntry) with the amount's
#    currency in an attribute and the booking date nested one level down.
ns = "urn:iso:std:iso:20022:tech:xsd:camt.053.001.08"
c = ['<?xml version="1.0" encoding="UTF-8"?>',
     f'<Document xmlns="{ns}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">',
     "  <BkToCstmrStmt>", "    <GrpHdr><MsgId>STMT-2024-03-0042</MsgId>"
     "<CreDtTm>2024-04-01T05:12:44+02:00</CreDtTm></GrpHdr>",
     "    <Stmt>", "      <Id>2024-03-DE00-0000</Id>",
     "      <Acct><Id><IBAN>DE00123456780000000000</IBAN></Id><Ccy>EUR</Ccy></Acct>"]
CP = ["Stadtwerke Musterstadt", "ACME Logistics GmbH", "Payroll 03/2024", "Café Kränzchen",
      "Fake Insurance AG", "Card settlement", "Refund SO-10434", "Rent April"]
for i in range(8):
    cd = "CRDT" if i in (2, 6) else "DBIT"
    amt = rnd.uniform(5, 4000)
    c += ["      <Ntry>",
          f'        <Amt Ccy="EUR">{amt:.2f}</Amt>',
          f"        <CdtDbtInd>{cd}</CdtDbtInd>",
          f"        <Sts><Cd>{'BOOK' if i != 7 else 'PDNG'}</Cd></Sts>",
          f"        <BookgDt><Dt>2024-03-{2 + i * 3:02d}</Dt></BookgDt>",
          f"        <AcctSvcrRef>REF{880100 + i * 17}</AcctSvcrRef>",
          f"        <AddtlNtryInf>{CP[i]}</AddtlNtryInf>",
          "      </Ntry>"]
c += ["    </Stmt>", "  </BkToCstmrStmt>", "</Document>", ""]
put("camt053.xml", "\n".join(c))

# 4. An OpenStreetMap extract (the .osm a planet cut or the export
#    button gives): nodes whose data is all in attributes, with <tag k v>
#    children, and a way listing its nodes.
s = ["<?xml version='1.0' encoding='UTF-8'?>",
     '<osm version="0.6" generator="osmium/1.16.0">',
     '  <bounds minlat="48.1350" minlon="11.5600" maxlat="48.1420" maxlon="11.5800"/>']
AMEN = [("amenity", "cafe", "Café Frischhut"), ("amenity", "bicycle_parking", None),
        ("shop", "bakery", "Bäckerei Zöttl"), ("amenity", "drinking_water", None),
        ("tourism", "museum", "Stadtmuseum"), ("amenity", "pharmacy", "Rathaus-Apotheke"),
        ("highway", "bus_stop", "Marienplatz"), ("amenity", "bench", None)]
for i, (k, v, name) in enumerate(AMEN):
    lat = 48.1350 + rnd.uniform(0, 0.007)
    lon = 11.5600 + rnd.uniform(0, 0.02)
    attrs = (f'id="{240119000 + i * 31}" version="{1 + i % 4}" '
             f'timestamp="2023-{1 + i:02d}-1{i}T0{i}:15:00Z" lat="{lat:.7f}" lon="{lon:.7f}"')
    if i == 3:
        s.append(f"  <node {attrs}/>")
        continue
    s.append(f"  <node {attrs}>")
    s.append(f'    <tag k="{k}" v="{v}"/>')
    if name:
        s.append(f'    <tag k="name" v="{name}"/>')
    s.append("  </node>")
s += ['  <way id="38291002" version="7">',
      '    <nd ref="240119000"/>', '    <nd ref="240119031"/>',
      '    <tag k="highway" v="pedestrian"/>', "  </way>", "</osm>", ""]
put("munich.osm", "\n".join(s))

# 5. A sitemap with hreflang alternates (xhtml:link, the same local name
#    three times in a url), plain, gzipped as servers serve it, and zipped.
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
      'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
PAGES = ["", "pricing", "docs/getting-started", "blog/2024/03/release-4-2", "careers", "legal/privacy"]
for i, p in enumerate(PAGES):
    sm.append("  <url>")
    sm.append(f"    <loc>https://example.com/{p}</loc>")
    if i != 4:
        sm.append(f"    <lastmod>2024-0{1 + i % 3}-{10 + i:02d}</lastmod>")
    sm.append(f"    <changefreq>{['daily', 'weekly', 'monthly'][i % 3]}</changefreq>")
    sm.append(f"    <priority>{[1.0, 0.8, 0.6, 0.5, 0.3, 0.1][i]}</priority>")
    if i < 3:
        for lang in ("de", "fr"):
            sm.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" '
                      f'href="https://example.com/{lang}/{p}"/>')
    sm.append("  </url>")
sm += ["</urlset>", ""]
sitemap = "\n".join(sm).encode("utf-8")
put("sitemap.xml", sitemap)
put("sitemap.xml.gz", gzip.compress(sitemap, mtime=1711929600))
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
    zi = zipfile.ZipInfo("sitemap.xml", (2024, 4, 1, 0, 0, 0))
    zi.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(zi, sitemap)
put("sitemap.zip", buf.getvalue())

# 6. An RSS 2.0 feed with the dc, content and media namespaces.
r = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/" '
     'xmlns:content="http://purl.org/rss/1.0/modules/content/" '
     'xmlns:media="http://search.yahoo.com/mrss/">',
     "<channel>", "  <title>Example Engineering</title>",
     "  <link>https://example.com/blog</link>",
     "  <description>Notes from the platform team</description>"]
POSTS = [("Release 4.2: faster joins", "Mei Chen", "Mon, 04 Mar 2024 09:00:00 +0000", 1840),
         ("Why we moved our queue to Postgres", "Tomás Ortega", "Thu, 14 Mar 2024 16:30:00 +0000", 2210),
         ("Incident review: 12 March", "Ada Obi", "Fri, 22 Mar 2024 11:05:00 +0000", None),
         ("Hiring: SRE (Berlin)", "Mei Chen", "Tue, 02 Apr 2024 08:00:00 +0000", 640)]
for i, (t, a, d, words) in enumerate(POSTS):
    r += ["  <item>", f"    <title>{t}</title>",
          f"    <link>https://example.com/blog/{i + 1}</link>",
          f"    <dc:creator>{a}</dc:creator>", f"    <pubDate>{d}</pubDate>",
          f'    <guid isPermaLink="false">post-{900 + i}</guid>',
          f"    <content:encoded><![CDATA[<p>{t}.</p>]]></content:encoded>"]
    if words:
        r.append(f'    <media:content url="https://cdn.example.com/{i}.jpg" medium="image" width="{words}"/>')
    r.append("  </item>")
r += ["</channel>", "</rss>", ""]
put("blog.rss", "\n".join(r))

# 7. A weather station's daily log, written by an old logger in latin-1,
#    with its encoding declared, readings in attributes and text, missing
#    values written three ways, and a processing instruction.
w = ['<?xml version="1.0" encoding="ISO-8859-1"?>',
     '<?xml-stylesheet type="text/xsl" href="log.xsl"?>',
     '<station id="DWD-01262" name="München-Flughafen" unit="°C">']
for i in range(7):
    temp = ["4.8", "6.1", "", "-0.4", "NA", "3.3", "n/a"][i]
    w.append(f'  <day date="2024-02-{12 + i:02d}" qc="{[1, 1, 3, 1, 2, 1, 1][i]}">'
             f"<tmax>{temp}</tmax><tmin>{-2.5 + i * 0.5:.1f}</tmin>"
             f"<rain>{[0, 1.2, 0.0, 7.75, 0.1, 0, 2][i]}</rain>"
             f"<wx>{['Schnee', 'Regen', 'Nebel', 'Graupel', 'heiter', 'Föhn', 'trüb'][i]}</wx></day>")
w += ["</station>", ""]
put("station_log.xml", "\n".join(w).encode("latin-1"))

# 8. A product catalogue large enough that a pipeline would iterparse it.
cat = ['<?xml version="1.0" encoding="UTF-8"?>', "<catalog>"]
for i in range(400):
    price = round(rnd.uniform(1, 500), 2)
    cat.append(f'  <product sku="P{i:05d}" active="{"yes" if i % 9 else "no"}">'
               f"<name>Part {i}</name><price>{price}</price>"
               f"<stock>{(i * 37) % 120}</stock>"
               f"<dims><w>{i % 50}</w><h>{(i * 3) % 40}</h></dims></product>")
cat += ["</catalog>", ""]
put("catalog.xml", "\n".join(cat))

# 9. The broken files people meet.
put("truncated.xml", "\n".join(o)[:1200])
put("mismatch.xml", "<data>\n  <row><a>1</a><b>2</a></row>\n</data>\n")
put("export.csv", "id,name\n1,Ana\n2,Ben\n")
put("empty.xml", "")
put("flat.xml", "<?xml version='1.0'?>\n<data><row/><row/></data>\n")

JOBS = """\
read ecb_rates.xml
read ecb_rates.xml xpath=//doc:Cube[@currency] namespaces=doc=http://www.ecb.int/vocabulary/2002-08-01/eurofxref
read ecb_rates.xml parser=etree xpath=.//doc:Cube[@currency] namespaces=doc=http://www.ecb.int/vocabulary/2002-08-01/eurofxref
read ecb_rates.xml xpath=//doc:Cube[@time] namespaces=doc=http://www.ecb.int/vocabulary/2002-08-01/eurofxref attrs_only=True parse_dates=time
read ecb_rates.xml xpath=//doc:Cube[@currency='USD'] namespaces=doc=http://www.ecb.int/vocabulary/2002-08-01/eurofxref
read ecb_rates.xml xpath=//Cube
read ecb_rates.xml xpath=//doc:Cube[@currency] namespaces=x=http://www.ecb.int/vocabulary/2002-08-01/eurofxref
read ecb_rates.xml parser=etree xpath=.//doc:Cube namespaces=x=http://www.ecb.int/vocabulary/2002-08-01/eurofxref
read ecb_rates.xml xpath=//*[local-name()='Cube'][@rate>100]
write ecb_rates.xml xpath=//doc:Cube[@currency='USD'] namespaces=doc=http://www.ecb.int/vocabulary/2002-08-01/eurofxref | index=False
write ecb_rates.xml xpath=//doc:Cube[@currency='CHF'] namespaces=doc=http://www.ecb.int/vocabulary/2002-08-01/eurofxref | parser=etree attr_cols=currency,rate
read orders.xml
read orders.xml parser=etree
read orders.xml elems_only=True
read orders.xml attrs_only=True
read orders.xml elems_only=True attrs_only=True
read orders.xml names=order_id,state,cust,placed,total,items,note,gift
read orders.xml parser=etree names=a,b,c
read orders.xml dtype=gift:str,total:float64 parse_dates=placed
read orders.xml xpath=//item
read orders.xml xpath=//order[gift='true']
read orders.xml parser=etree xpath=.//order[gift='true']
read orders.xml xpath=//order[position()>6]
read orders.xml parser=etree xpath=.//order[last()]
read orders.xml xpath=//order/@id
read orders.xml xpath=count(//order)
read orders.xml xpath=boolean(//order)
read blog.rss xpath=string(//title)
read orders.xml xpath=//order[1]/@id|//order[2]
read orders.xml xpath=//items elems_only=True names=x,y
read orders.xml parser=etree xpath=//order
read orders.xml xpath=//order[
read orders.xml parser=etree xpath=.//order[@id=
read orders.xml xpath=//invoice
read orders.xml iterparse=order:id,status,customer,total,sku
read orders.xml parser=etree iterparse=order:id,status,customer,total,qty
read orders.xml iterparse=order:customer,customer,id names=a,b,c
read orders.xml parser=lexml
write orders.xml | attr_cols=id,status elem_cols=customer,total
write orders.xml | parser=etree attr_cols=id,status elem_cols=customer,total
write orders.xml dtype=gift:str parse_dates=placed | index=False root_name=export row_name=sale
write orders.xml | parser=etree
write orders.xml | parser=etree xml_declaration=False elem_cols=note
write orders.xml | parser=etree pretty_print=False xml_declaration=False
write orders.xml | pretty_print=False
write orders.xml | na_rep=- elem_cols=customer,note
write orders.xml | parser=etree na_rep=- elem_cols=customer,note
write orders.xml | na_rep=n/a elem_cols=total attr_cols=id
write orders.xml | attr_cols=id,missing
write orders.xml | namespaces=s=https://example.com/s prefix=s elem_cols=customer
write orders.xml | parser=etree namespaces=s=https://example.com/s prefix=s elem_cols=customer
write orders.xml | parser=etree namespaces=s=https://example.com/s prefix=t
write orders.xml | namespaces==https://example.com/d elem_cols=customer index=False
write orders.xml | parser=etree namespaces==https://example.com/d elem_cols=customer index=False
write orders.xml | encoding=latin-1 elem_cols=customer index=False
write orders.xml | parser=etree encoding=ascii elem_cols=customer index=False
write orders.xml | encoding=ascii elem_cols=customer index=False
write orders.xml | parser=etree encoding=ascii attr_cols=customer index=False
write orders.xml | parser=etree pretty_print=False elem_cols=customer index=False
write orders.xml xpath=//order[position()>6] | na_rep=x
write orders.xml names=a,b,c,d,e,f,g,h | parser=etree index=False elem_cols=a,h
write munich.osm xpath=//node attrs_only=True parse_dates=timestamp | parser=etree elem_cols=timestamp index=False
read camt053.xml xpath=//doc:Ntry namespaces=doc=urn:iso:std:iso:20022:tech:xsd:camt.053.001.08
read camt053.xml xpath=//doc:Ntry namespaces=doc=urn:iso:std:iso:20022:tech:xsd:camt.053.001.08 elems_only=True dtype=AcctSvcrRef:str
read camt053.xml xpath=//doc:Ntry/doc:BookgDt namespaces=doc=urn:iso:std:iso:20022:tech:xsd:camt.053.001.08 parse_dates=Dt
read camt053.xml parser=etree xpath=.//doc:Ntry namespaces=doc=urn:iso:std:iso:20022:tech:xsd:camt.053.001.08
read camt053.xml xpath=//Ntry
read camt053.xml xpath=//doc:Ntry[doc:CdtDbtInd='CRDT'] namespaces=doc=urn:iso:std:iso:20022:tech:xsd:camt.053.001.08
write camt053.xml xpath=//doc:Ntry namespaces=doc=urn:iso:std:iso:20022:tech:xsd:camt.053.001.08 | index=False row_name=entry
read munich.osm xpath=//node attrs_only=True
read munich.osm parser=etree xpath=./node
read munich.osm xpath=//node[tag/@k='amenity']/tag
read munich.osm xpath=//tag[@k='name']
read munich.osm iterparse=node:id,lat,lon,k,v
read munich.osm parser=etree iterparse=node:id,lat,lon,v
read munich.osm xpath=//bounds
read munich.osm xpath=//node attrs_only=True parse_dates=timestamp
write munich.osm xpath=//node attrs_only=True | attr_cols=id,lat,lon elem_cols=timestamp
write munich.osm xpath=//node attrs_only=True | parser=etree attr_cols=id,lat,lon index=False
read sitemap.xml xpath=//s:url namespaces=s=http://www.sitemaps.org/schemas/sitemap/0.9
read sitemap.xml xpath=//s:url namespaces=s=http://www.sitemaps.org/schemas/sitemap/0.9 parse_dates=lastmod
read sitemap.xml.gz xpath=//s:url namespaces=s=http://www.sitemaps.org/schemas/sitemap/0.9 elems_only=True
read sitemap.zip parser=etree xpath=.//s:url namespaces=s=http://www.sitemaps.org/schemas/sitemap/0.9
read sitemap.xml xpath=//x:link namespaces=x=http://www.w3.org/1999/xhtml
read sitemap.xml.gz iterparse=url:loc,lastmod
read sitemap.xml xpath=//s:url namespaces=s=http://www.sitemaps.org/schemas/sitemap/0.9 compression=gzip
read blog.rss xpath=//item
read blog.rss parser=etree xpath=./channel/item
read blog.rss xpath=//item dtype=guid:str elems_only=True
read blog.rss xpath=//media:content namespaces=media=http://search.yahoo.com/mrss/
read blog.rss xpath=//channel
write blog.rss xpath=//item elems_only=True | index=False pretty_print=False
read station_log.xml
read station_log.xml encoding=ISO-8859-1
read station_log.xml encoding=latin-1
read station_log.xml parser=etree encoding=latin-1
read station_log.xml parser=etree encoding=cp1252 dtype=qc:float64
read station_log.xml encoding=ISO-8859-1 xpath=/station attrs_only=True
read station_log.xml encoding=ISO-8859-1 dtype=tmax:float64
read station_log.xml encoding=ISO-8859-1 dtype=wx:int64
read station_log.xml iterparse=day:date,tmax,wx
read station_log.xml parser=etree iterparse=day:date,tmax,tmax names=date,t1,t2
write station_log.xml encoding=ISO-8859-1 | encoding=ISO-8859-1 index=False
read catalog.xml iterparse=product:sku,active,price,stock,w head=5
read catalog.xml parser=etree iterparse=product:sku,price head=3
read catalog.xml xpath=//product[price>490] elems_only=True
read catalog.xml xpath=//product[stock=0]
read catalog.xml iterparse=product
read catalog.xml iterparse=products:sku
read truncated.xml parser=etree
read mismatch.xml parser=etree
read export.csv parser=etree
read empty.xml parser=etree
read flat.xml
read flat.xml parser=etree
read missing.xml
"""
put("jobs.txt", JOBS)
