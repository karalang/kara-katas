# Writes data/: the feeds, HTML snippets and date strings, plus jobs.txt and
# files.txt. Run as: python3 -s -P -B mk.py
import os

D = 'data'
os.makedirs(D + '/feeds', exist_ok=True)
files = []


def put(name, data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    with open(D + '/feeds/' + name, 'wb') as f:
        f.write(data)
    files.append('feeds/' + name)


put('rss20_blog.xml', '''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:wfw="http://wellformedweb.org/commentAPI/">
<channel>
  <title>Field Notes</title>
  <link>https://notes.example.org/</link>
  <description>Short posts about &lt;b&gt;gardening&lt;/b&gt; and tools</description>
  <language>en-gb</language>
  <copyright>Copyright 2024 Field Notes</copyright>
  <lastBuildDate>Tue, 05 Mar 2024 10:15:00 +0000</lastBuildDate>
  <generator>Hugo -- gohugo.io</generator>
  <managingEditor>editor@notes.example.org (Sam Rivera)</managingEditor>
  <webMaster>web@notes.example.org</webMaster>
  <ttl>60</ttl>
  <cloud domain="rpc.example.org" port="80" path="/RPC2" registerProcedure="ping" protocol="xml-rpc"/>
  <image>
    <url>https://notes.example.org/logo.png</url>
    <title>Field Notes</title>
    <link>https://notes.example.org/</link>
    <width>88</width>
    <height>thirty</height>
  </image>
  <item>
    <title>Pruning the &lt;em&gt;apple&lt;/em&gt; trees</title>
    <link>https://notes.example.org/2024/03/pruning/</link>
    <description>&lt;p&gt;Late winter is the time. &lt;a href="/tools/"&gt;Tools&lt;/a&gt; I use.&lt;/p&gt;&lt;script&gt;alert(1)&lt;/script&gt;</description>
    <pubDate>Tue, 05 Mar 2024 09:00:00 GMT</pubDate>
    <guid isPermaLink="true">https://notes.example.org/2024/03/pruning/</guid>
    <dc:creator>Sam Rivera</dc:creator>
    <category domain="https://notes.example.org/tags">orchard</category>
    <category>winter</category>
    <comments>https://notes.example.org/2024/03/pruning/#comments</comments>
    <wfw:commentRss>https://notes.example.org/2024/03/pruning/feed/</wfw:commentRss>
    <content:encoded><![CDATA[<p style="color: red; position: absolute">Cut <b>above</b> the bud.</p>
<img src="/img/cut.jpg" alt="cut" onerror="steal()"><br/>
<iframe src="https://evil.example.com/"></iframe><p>Done &amp; dusted.</p>]]></content:encoded>
  </item>
  <item>
    <title>Seed swap on Saturday</title>
    <link>https://notes.example.org/2024/02/seed-swap/</link>
    <description>Bring seeds, take seeds.</description>
    <pubDate>Sat, 24 Feb 2024 18:30:00 -0500</pubDate>
    <guid isPermaLink="false">tag:notes.example.org,2024:seed-swap</guid>
    <enclosure url="https://notes.example.org/media/swap.mp3" length="1234567" type="audio/mpeg"/>
    <author>sam@notes.example.org (Sam Rivera)</author>
  </item>
  <item>
    <title>Untitled note</title>
    <description>A note without a link, dated in an odd way.</description>
    <pubDate>24 Feb 24 07:05 EST</pubDate>
  </item>
</channel>
</rss>
''')

put('atom10_news.xml', '''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-US" xml:base="https://news.example.com/">
  <title type="text">Example News</title>
  <subtitle type="html">All the &lt;i&gt;news&lt;/i&gt; that fits</subtitle>
  <link rel="alternate" type="text/html" href="/"/>
  <link rel="self" href="https://news.example.com/feed.atom"/>
  <id>urn:uuid:60a76c80-d399-11d9-b93c-0003939e0af6</id>
  <updated>2024-03-06T08:30:00Z</updated>
  <rights>(c) 2024 Example News</rights>
  <generator uri="/gen/" version="2.1">NewsGen</generator>
  <icon>/favicon.ico</icon>
  <logo>/logo.svg</logo>
  <author>
    <name>Desk Editor</name>
    <email>desk@news.example.com</email>
    <uri>/staff/desk</uri>
  </author>
  <entry>
    <title type="html">Council approves &lt;b&gt;new&lt;/b&gt; bridge</title>
    <link rel="alternate" type="text/html" href="2024/03/bridge"/>
    <link rel="enclosure" type="image/jpeg" length="40960" href="/img/bridge.jpg"/>
    <id>tag:news.example.com,2024:bridge</id>
    <published>2024-03-05T17:00:00-08:00</published>
    <updated>2024-03-06T01:15:30+01:00</updated>
    <author><name>Ana Lima</name></author>
    <contributor><name>Raj Patel</name><email>raj@news.example.com</email></contributor>
    <category term="local" scheme="https://news.example.com/sections" label="Local"/>
    <category term="transport"/>
    <summary type="html">The vote was &lt;b&gt;7 to 2&lt;/b&gt;. &lt;a href="/votes/123"&gt;Details&lt;/a&gt;</summary>
    <content type="xhtml" xml:base="https://news.example.com/2024/03/">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <p>Construction starts in <em>June</em>. See <a href="plan.pdf">the plan</a>.</p>
        <p>Cost: 5 &lt; 6 million &amp; rising.</p>
      </div>
    </content>
  </entry>
  <entry xml:lang="fr">
    <title>Marché du samedi</title>
    <link href="https://news.example.com/fr/marche"/>
    <id>tag:news.example.com,2024:marche</id>
    <updated>2024-03-02</updated>
    <summary>Les producteurs locaux reviennent.</summary>
    <content type="text/plain">Ouvert de 8h à 13h.</content>
    <source>
      <id>tag:partner.example.net,2024:feed</id>
      <title>Partner Wire</title>
      <updated>2024-03-01T12:00:00Z</updated>
    </source>
  </entry>
  <entry>
    <title type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml">Weather <b>warning</b></div></title>
    <id>tag:news.example.com,2024:weather</id>
    <updated>2024-03-06T23:59:59Z</updated>
    <content type="html">&lt;p onclick="x()"&gt;High winds &lt;u&gt;tonight&lt;/u&gt;.&lt;/p&gt;&lt;style&gt;p{}&lt;/style&gt;</content>
  </entry>
</feed>
''')

put('rss10_rdf.xml', '''<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns="http://purl.org/rss/1.0/"
         xmlns:dc="http://purl.org/dc/elements/1.1/"
         xmlns:sy="http://purl.org/rss/1.0/modules/syndication/">
  <channel rdf:about="https://lib.example.edu/new.rdf">
    <title>Library New Arrivals</title>
    <link>https://lib.example.edu/new</link>
    <description>Books added this week</description>
    <dc:language>en</dc:language>
    <dc:publisher>City Library</dc:publisher>
    <dc:rights>CC0</dc:rights>
    <dc:date>2024-03-04T06:00:00+00:00</dc:date>
    <sy:updatePeriod>weekly</sy:updatePeriod>
    <items><rdf:Seq><rdf:li rdf:resource="https://lib.example.edu/b/1"/></rdf:Seq></items>
    <textinput rdf:resource="https://lib.example.edu/search"/>
  </channel>
  <item rdf:about="https://lib.example.edu/b/1">
    <title>The Soil Book</title>
    <link>https://lib.example.edu/b/1</link>
    <description>A practical guide.</description>
    <dc:subject>Gardening</dc:subject>
    <dc:creator>J. Okafor</dc:creator>
    <dc:date>2024-03-03</dc:date>
    <dc:contributor>M. Chen</dc:contributor>
  </item>
  <item rdf:about="https://lib.example.edu/b/2">
    <title>Rivers of the North</title>
    <link>https://lib.example.edu/b/2</link>
    <dc:subject>Geography</dc:subject>
    <dc:date>2024-03-02T15:20:00-03:30</dc:date>
  </item>
  <textinput rdf:about="https://lib.example.edu/search">
    <title>Search</title>
    <description>Search the catalogue</description>
    <name>q</name>
    <link>https://lib.example.edu/search</link>
  </textinput>
</rdf:RDF>
''')

put('rss091n.xml', '''<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN"
 "http://my.netscape.com/publish/formats/rss-0.91.dtd">
<rss version="0.91">
<channel>
<title>Caf\xe9 Bulletin</title>
<link>http://cafe.example.org/</link>
<description>Daily specials at the caf\xe9</description>
<language>fr-ca</language>
<item>
<title>Cr\xeapes today</title>
<link>http://cafe.example.org/crepes</link>
<description>With maple syrup &amp; berries.</description>
</item>
</channel>
</rss>
'''.encode('latin-1'))

put('rss092.xml', '''<rss version="0.92"><channel><title>Plain 0.92</title>
<link>http://old.example.org/</link><description>no declaration at all</description>
<item><title>First</title><description>one &amp;amp; two</description>
<enclosure url="http://old.example.org/a.ogg" length="10" type="audio/ogg"/></item>
</channel></rss>
''')

put('podcast.xml', '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
<channel>
  <title>Workshop Talk</title>
  <link>https://pod.example.fm/</link>
  <description>Conversations about making things.</description>
  <itunes:author>Workshop Collective</itunes:author>
  <itunes:owner><itunes:name>Lee Park</itunes:name><itunes:email>lee@pod.example.fm</itunes:email></itunes:owner>
  <itunes:image href="https://pod.example.fm/cover.jpg"/>
  <itunes:category text="Arts"><itunes:category text="Design"/></itunes:category>
  <itunes:explicit>clean</itunes:explicit>
  <itunes:keywords>wood, metal, ,craft</itunes:keywords>
  <itunes:block>Yes</itunes:block>
  <item>
    <title>Episode 12: Joinery</title>
    <itunes:subtitle>Dovetails and more</itunes:subtitle>
    <itunes:summary>We talk about &lt;b&gt;hand-cut&lt;/b&gt; joints.</itunes:summary>
    <itunes:duration>45:10</itunes:duration>
    <itunes:explicit>yes</itunes:explicit>
    <enclosure url="https://pod.example.fm/ep12.mp3" length="43200000" type="audio/mpeg"/>
    <guid>https://pod.example.fm/ep12</guid>
    <pubDate>Mon, 04 Mar 2024 05:00:00 PST</pubDate>
  </item>
  <item>
    <title>Episode 11: Finishes</title>
    <itunes:explicit>no</itunes:explicit>
    <enclosure url="https://pod.example.fm/ep11.mp3" length="40000000" type="audio/mpeg"/>
    <guid isPermaLink="false">pod-ep11</guid>
    <pubDate>Mon, 26 Feb 2024 05:00:00 PST</pubDate>
  </item>
</channel>
</rss>
''')

put('atom03.xml', '''<?xml version="1.0" encoding="utf-8"?>
<feed version="0.3" xmlns="http://purl.org/atom/ns#">
  <title mode="escaped">Old &amp;lt;Atom&amp;gt;</title>
  <tagline>An Atom 0.3 feed</tagline>
  <link rel="alternate" type="text/html" href="http://old.example.net/"/>
  <modified>2003-12-13T18:30:02Z</modified>
  <author><name>Mark</name><url>http://old.example.net/mark</url></author>
  <entry>
    <title>Atom-Powered Robots Run Amok</title>
    <link rel="alternate" type="text/html" href="http://old.example.net/2003/12/13/atom03"/>
    <id>tag:old.example.net,2003:3.2397</id>
    <issued>2003-12-13T08:29:29-04:00</issued>
    <modified>2003-12-13T18:30:02Z</modified>
    <created>2003-12-13T08:29:29-04:00</created>
    <summary type="text/plain">Some text with &lt;br&gt; inside.</summary>
    <content type="text/html" mode="escaped">&lt;p&gt;Hello &lt;img src="robot.png"&gt;&lt;/p&gt;</content>
  </entry>
</feed>
''')

put('latin1_declared.xml', '''<?xml version="1.0" encoding="iso-8859-1"?>
<rss version="2.0"><channel><title>Gr\xfc\xdfe aus K\xf6ln</title>
<link>http://koeln.example.de/</link><description>\xbfQu\xe9 tal?</description>
<item><title>Stra\xdfenfest</title><link>http://koeln.example.de/fest</link></item>
</channel></rss>
'''.encode('latin-1'))

put('cp1252_mislabeled.xml', '''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel><title>Smart \x93quotes\x94 \x96 dash</title>
<link>http://quotes.example.com/</link><description>Saved by an old editor \x85</description>
<item><title>Caf\xe9 \x80 prices</title></item>
</channel></rss>
'''.encode('latin-1'))

put('utf8_bom.xml', b'\xef\xbb\xbf' + '''<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>BOM \u2713 feed</title>
<id>urn:x:bom</id><updated>2024-01-01T00:00:00Z</updated>
<entry><title>\u65e5\u672c\u8a9e</title><id>urn:x:bom:1</id><updated>2024-01-01T00:00:00Z</updated></entry>
</feed>
'''.encode('utf-8'))

put('bad_entity.xml', '''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>
<title>Tom&apos;s Hardware &nbsp;Deals</title>
<link>http://deals.example.com/</link>
<description>Prices &copy; 2024 &mdash; updated hourly</description>
<item>
<title>SSD &amp; RAM bundle</title>
<link>http://deals.example.com/?id=5&amp;ref=rss</link>
<description><![CDATA[<b>Save</b> 20%]]></description>
<pubDate>Wed, 06 Mar 2024 12:00:00 Z</pubDate>
</item>
</channel>
</rss>
''')

put('bare_ampersand.xml', '''<?xml version="1.0"?>
<rss version="2.0"><channel>
<title>AT&T Customer News</title>
<link>http://att.example.com/?a=1&b=2</link>
<description>News & offers</description>
<item><title>Q&A session</title><link>http://att.example.com/qa</link>
<description>Ask us &lt;i&gt;anything&lt;/i&gt;</description></item>
</channel></rss>
''')

put('truncated.xml', '''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Cut short</title>
  <entry>
    <title>Only entry</title>
    <id>urn:cut:1</id>
    <summary>The connection dropped
''')

put('mismatched.xml', '''<rss version="2.0">
<channel>
<title>Sloppy <b>Feed</title>
<item><title>One</title><description>first</description></item>
</channel>
</rss>
''')

put('unbound_prefix.xml', '''<?xml version="1.0"?>
<rss version="2.0"><channel><title>Prefix trouble</title>
<item><title>Uses media</title><ext:thumb url="http://x.example/t.jpg"/></item>
</channel></rss>
''')

put('relative.xml', '''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel><title>Relative links</title>
<link>/home</link>
<description>&lt;a href="about.html"&gt;About&lt;/a&gt; &lt;img src="//cdn.example.net/x.png"&gt; &lt;a href="javascript:evil()"&gt;bad&lt;/a&gt;</description>
<item><title>Post</title><link>posts/1</link><guid>posts/1</guid>
<description>&lt;blockquote cite="../q"&gt;quoted&lt;/blockquote&gt; &lt;a href="mailto:me@example.org"&gt;mail&lt;/a&gt;</description></item>
</channel></rss>
''')

put('junk_after.xml', '''<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>Twice</title></feed>
<feed xmlns="http://www.w3.org/2005/Atom"><title>Again</title></feed>
''')

put('html_page.xml', '''<html><head><title>Not a feed</title></head>
<body><p>Hello<br>world</p></body></html>
''')

# Feeds for the reader programs.
for i, (name, stamp, lang) in enumerate([
        ('Morning Brief', 'Mon, 04 Mar 2024 07:00:00 +0000', 'en'),
        ('Evening Edition', 'Mon, 04 Mar 2024 19:00:00 +0100', 'en'),
        ('Weekend Reads', 'Sat, 02 Mar 2024 10:00:00 -0800', 'en-us')]):
    items = []
    for k in range(3):
        items.append('<item><title>%s story %d</title><link>http://r%d.example.com/s%d</link>'
                     '<description>Story &lt;b&gt;%d&lt;/b&gt; of %s</description>'
                     '<pubDate>%s</pubDate><category>%s</category></item>'
                     % (name, k + 1, i, k, k + 1, name, stamp.replace('00:00', '%02d:00' % (k * 7)),
                        ('world', 'tech', 'world')[k]))
    put('reader_%d.xml' % i, '<?xml version="1.0"?><rss version="2.0"><channel><title>%s</title>'
        '<link>http://r%d.example.com/</link><language>%s</language>%s</channel></rss>\n'
        % (name, i, lang, ''.join(items)))

dates = [
    'Tue, 05 Mar 2024 09:00:00 GMT', 'Sat, 24 Feb 2024 18:30:00 -0500', '24 Feb 24 07:05 EST',
    'Mar 05 2024 09:00:00 +0530', 'Thu, 29 Feb 2024 23:59:59 +02:00', '05 Mar 1989 1:2:3 PDT',
    'Wed, 06 Mar 2024 12:00:00 Z', 'Wed, 06 Mar 2024 12:00:00 Etc/GMT+1', 'Mon, 01 Jan 2024 00:00:00 GMT-05:00',
    '2024-03-05T17:00:00-08:00', '2024-03-06T01:15:30+01:00', '2024-03-02', '2024-03', '2024',
    '2003-12-13T18:30:02Z', '2003-12-13 18:30:02', 
    '2024-03-05T10:20:30.75+05:45', '2024-03-05t10:20z',
    'Sun, 31 Dec 2023 23:00:00 -0100', 'Fri, 13 Sep 2024 25:00:00 GMT', 'yesterday', '',
    'Mon, 04 Mar 2024 05:00:00 PST', 'Tue, 5 Mar 2024 9:00 MET', '2024-03-05T10:00:00 +0200',
]
with open(D + '/dates.txt', 'w') as f:
    f.write('\n'.join(dates) + '\n')
files.append('dates.txt')

snippets = [
    '<p>Hello <b>world</b></p>',
    '<script>alert("x")</script><p>after</p>',
    '<a href="javascript:alert(1)" title="t">link</a>',
    '<a href="http://ok.example.com/" target="_blank" rel="Nofollow">ok</a>',
    '<div style="color: blue; background: url(http://x/y.png) red; margin: 0 auto">styled</div>',
    '<span style="font-weight: bold; behavior: url(x.htc)">b</span>',
    '<img src="x.png" onerror="evil()" width="10">',
    '<!-- a comment --><p>text</p><?php echo 1 ?>',
    '<table><tr><td colspan="2">cell</td></tr></table>',
    '<p>5 &lt; 6 &amp;&amp; 7 &gt; 3 &nbsp; &bogus; &#169; &#x41; &#150;</p>',
    '<object data="movie.swf"><param name="a" value="b"></object>text',
    '<br/><hr/><p/>end',
    '<style>body{display:none}</style>visible',
    '<p>unclosed <b>bold <i>italic',
    '<A HREF="/Upper" CLASS="x">CAPS</A>',
    '<form action="/f"><input type="TEXT" name="q"></form>',
    '<p title=\'single\' id=plain>attrs</p>',
    '<applet code="x"></applet>after applet',
    '<p>line one\r\nline two</p>',
    '<![CDATA[raw]]> and <!-- unterminated',
]
with open(D + '/snippets.txt', 'w') as f:
    for s in snippets:
        f.write(s.replace('\\', '\\\\').replace('\r', '\\r').replace('\n', '\\n') + '\n')
files.append('snippets.txt')

jobs = []
for fn in files:
    if fn.startswith('feeds/') and not fn.startswith('feeds/reader_'):
        jobs.append('parse ' + fn)
jobs.append('parse feeds/relative.xml http://site.example.org/blog/feed.xml')
jobs.append('parse feeds/rss20_blog.xml https://notes.example.org/feed/')
jobs.append('!dates dates.txt')
jobs.append('!sanitize snippets.txt')
jobs.append('!resolve snippets.txt http://site.example.org/a/b/')
jobs.append('!digest feeds/reader_0.xml feeds/reader_1.xml feeds/reader_2.xml feeds/rss20_blog.xml feeds/atom10_news.xml')
jobs.append('!tags feeds/reader_0.xml feeds/reader_1.xml feeds/reader_2.xml feeds/rss20_blog.xml feeds/atom10_news.xml feeds/podcast.xml')
jobs.append('!opml feeds/rss20_blog.xml feeds/atom10_news.xml feeds/rss10_rdf.xml feeds/podcast.xml feeds/bad_entity.xml feeds/html_page.xml')
jobs.append('!health ' + ' '.join(fn for fn in files if fn.startswith('feeds/') and not fn.startswith('feeds/reader_')))
with open(D + '/jobs.txt', 'w') as f:
    f.write('\n'.join(jobs) + '\n')
with open(D + '/files.txt', 'w') as f:
    f.write('\n'.join(files) + '\n')
print(len(files), 'files,', len(jobs), 'jobs')
