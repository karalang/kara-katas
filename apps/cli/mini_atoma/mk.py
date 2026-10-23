"""Write data/jobs.tsv and the feeds the jobs read.

atoma is the feed parser behind several Python feed readers and
aggregators: it reads RSS 2.0, Atom 1.0, JSON Feed and OPML into plain
objects, and its `simple` module turns any of the three feed formats into
one Feed of Articles. The feeds below are the kind a reader meets: a blog
in RSS with every channel field, a podcast with enclosures, an Atom blog
with HTML titles and enclosure links, an aggregated Atom feed whose entries
carry their source, JSON Feeds (a blog, a podcast, a feed with a byte-order
mark, one that is not UTF-8), OPML subscription lists, and the broken and
hostile ones: unclosed tags, undefined entities, a "billion laughs" DTD and
an external entity, which the parser refuses as defusedxml does.

data/cache holds the feeds an OPML file subscribes to, as a feed reader's
HTTP cache would, with data/cache/urls.tsv mapping each URL to its file.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

FILES = {}

FILES["feeds/rss/scripting-news.xml"] = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Scripting News</title>
    <link>http://scripting.example.com/</link>
    <description>A weblog about scripting and stuff like that.</description>
    <language>en-us</language>
    <copyright>Copyright 1997-2024 Dave Example</copyright>
    <managingEditor>dave@example.com (Dave)</managingEditor>
    <webMaster>ops@example.com</webMaster>
    <pubDate>Mon, 30 Sep 2024 04:00:00 GMT</pubDate>
    <lastBuildDate>Mon, 30 Sep 2024 09:41:01 EDT</lastBuildDate>
    <category>Scripting</category>
    <category domain="http://www.example.com/cats">Web/RSS</category>
    <category/>
    <generator>Radio UserLand v8.2.1</generator>
    <docs>https://www.rssboard.org/rss-specification</docs>
    <ttl>60</ttl>
    <image>
      <url>http://scripting.example.com/gifs/tinyScriptingNews.gif</url>
      <title>Scripting News</title>
      <link>http://scripting.example.com/</link>
      <width>144</width>
      <height>40</height>
      <description>Click to visit</description>
    </image>
    <item>
      <title>Why RSS still matters</title>
      <link>http://scripting.example.com/2024/09/30/rss.html</link>
      <description>&lt;p&gt;Feeds are the web&amp;#39;s open plumbing.&lt;/p&gt;</description>
      <author>dave@example.com (Dave)</author>
      <category>RSS</category>
      <category>Open web</category>
      <comments>http://scripting.example.com/2024/09/30/rss.html#comments</comments>
      <guid>http://scripting.example.com/2024/09/30/rss.html</guid>
      <pubDate>Mon, 30 Sep 2024 08:15:00 -0400</pubDate>
      <source url="http://feeds.example.org/rss-matters.xml">RSS Matters</source>
      <content:encoded><![CDATA[<p>Feeds are the web's <em>open</em> plumbing.</p>]]></content:encoded>
    </item>
    <item>
      <title>   Whitespace around a title   </title>
      <guid isPermaLink="true">http://scripting.example.com/2024/09/29/ws.html</guid>
      <pubDate>Sun, 29 Sep 2024 23:59:59 PDT</pubDate>
      <dc:creator>Dave</dc:creator>
    </item>
    <item>
      <description>An item with only a description, as RSS 2.0 allows.</description>
      <guid isPermaLink="false">tag:scripting.example.com,2024:item-3</guid>
    </item>
    <item>
      <title>Caf\u00e9 \u2014 \u201cquoted\u201d \u65e5\u672c\u8a9e</title>
      <link>http://scripting.example.com/2024/09/28/unicode.html</link>
      <pubDate>Sat, 28 Sep 2024 12:00:00 +0900</pubDate>
    </item>
  </channel>
</rss>
"""

FILES["feeds/rss/podcast.xml"] = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>The Changelog-ish</title>
    <link>https://podcast.example.com</link>
    <description>Conversations with the hackers, leaders and innovators of software.</description>
    <itunes:author>Example Media</itunes:author>
    <ttl>1440</ttl>
    <image>
      <url>https://podcast.example.com/cover.png</url>
      <link>https://podcast.example.com</link>
      <width>0</width>
    </image>
    <item>
      <title>Episode 3: Compilers all the way down</title>
      <guid isPermaLink="false">podcast-ep-3</guid>
      <pubDate>Wed, 02 Oct 2024 10:00:00 CST</pubDate>
      <enclosure url="https://cdn.example.com/media/ep3.mp3?source=rss#t=0" length="48213504" type="audio/mpeg"/>
      <itunes:duration>01:06:58</itunes:duration>
    </item>
    <item>
      <title>Episode 2: Feeds and fediverse</title>
      <guid isPermaLink="true">https://podcast.example.com/2</guid>
      <pubDate>Wed, 25 Sep 2024 10:00:00 CDT</pubDate>
      <enclosure url="https://cdn.example.com/media/ep2.mp3" length="" type="audio/mpeg"/>
      <enclosure url="https://cdn.example.com/media/ep2-transcript.txt" length="-5" type="text/plain"/>
    </item>
    <item>
      <title>Episode 1: Hello</title>
      <link>https://podcast.example.com/1</link>
      <pubDate>Wed, 18 Sep 2024 10:00:00 MST</pubDate>
      <enclosure url="https://cdn.example.com/media/ep1;v=2" length="12,345"/>
      <enclosure url="https://cdn.example.com/media/" length="1024" type="audio/mpeg"/>
    </item>
    <item>
      <title>Trailer</title>
      <pubDate>Wed, 11 Sep 2024 10:00:00 MDT</pubDate>
      <enclosure url="https://cdn.example.com/media/trailer.m4a" length=" 2048 " type="audio/x-m4a"/>
    </item>
  </channel>
</rss>
"""

DATES = [
    "Tue, 10 Jun 2003 04:00:00 GMT",
    "Tue, 10 Jun 2003 04:00:00 UT",
    "Tue, 10 Jun 2003 04:00:00 EST",
    "Tue, 10 Jun 2003 04:00:00 EDT",
    "Tue, 10 Jun 2003 04:00:00 PST",
    "Tue, 10 Jun 2003 04:00:00 +0530",
    "Tue, 10 Jun 2003 04:00:00 CET",
    "Tue, 10 Jun 03 04:00:00 GMT",
    "Thu, 10 Jun 1999 04:00 GMT",
    "Mon, 10 Jun 2003 04:00:00 GMT",
    "10 Jun 2003",
    "2003-06-10T04:00:00Z",
    "2003-06-10T04:00:00.25-07:00",
    "2003-06-10 04:00:00 GMT+3",
    "June 10, 2003 4:00 PM",
    "Posted on Tuesday, June 10th, 2003 at 4pm UTC",
    "Tue, 31 Jun 2003 04:00:00 GMT",
    "not a date",
    "   ",
    "",
]

_items = []
for _d in DATES:
    _date = "<pubDate>%s</pubDate>" % _d if _d else "<pubDate/>"
    _items.append("    <item><title>%s</title>%s</item>\n" % (_d.strip() or "(blank)", _date))
FILES["feeds/rss/dates.xml"] = (
    '<rss version="2.0"><channel><title>Dates</title>\n' + "".join(_items)
    + "</channel></rss>\n")

FILES["feeds/rss/link-only.xml"] = """\
<rss version="2.0"><channel>
  <link>https://link-only.example.com/</link>
  <item><title>First</title><link>https://link-only.example.com/1</link></item>
</channel></rss>
"""

FILES["feeds/rss/no-title-no-link.xml"] = """\
<rss version="2.0"><channel>
  <description>Neither a title nor a link</description>
</channel></rss>
"""

FILES["feeds/rss/v091.xml"] = """\
<?xml version="1.0"?>
<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd">
<rss version="0.91"><channel><title>Old</title><link>http://old.example.com/</link></channel></rss>
"""

FILES["feeds/rss/no-channel.xml"] = '<rss version="2.0"><title>No channel</title></rss>\n'
FILES["feeds/rss/bad-ttl.xml"] = '<rss version="2.0"><channel><title>T</title><ttl>sixty</ttl></channel></rss>\n'
FILES["feeds/rss/ttl-spaces.xml"] = '<rss version="2.0"><channel><title>T</title><ttl> +1_440 </ttl></channel></rss>\n'
FILES["feeds/rss/image-no-url.xml"] = '<rss version="2.0"><channel><title>T</title><image><link>http://x.example/</link></image></channel></rss>\n'
FILES["feeds/rss/enclosure-no-url.xml"] = '<rss version="2.0"><channel><title>T</title><item><enclosure length="1"/></item></channel></rss>\n'
FILES["feeds/rss/empty-source.xml"] = '<rss version="2.0"><channel><title>T</title><item><source url="http://x.example/"/></item></channel></rss>\n'
FILES["feeds/rss/required-empty.xml"] = '<rss version="2.0"><channel><title>T</title><image><url/><link>l</link></image></channel></rss>\n'

ATOM = "http://www.w3.org/2005/Atom"

FILES["feeds/atom/blog.xml"] = """\
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">
  <title type="text">dive into mark</title>
  <subtitle type="html">A &lt;em&gt;lot&lt;/em&gt; of effort went into making this effortless</subtitle>
  <updated>2005-07-31T12:29:29Z</updated>
  <id>tag:example.org,2003:3</id>
  <link rel="alternate" type="text/html" hreflang="en" href="http://example.org/"/>
  <link rel="self" type="application/atom+xml" href="http://example.org/feed.atom"/>
  <rights>Copyright (c) 2003, Mark Pilgrim</rights>
  <generator uri="http://www.example.com/" version="1.0">  Example Toolkit  </generator>
  <icon>http://example.org/favicon.ico</icon>
  <logo> http://example.org/logo.png </logo>
  <author>
    <name>Mark Pilgrim</name>
    <uri>http://example.org/</uri>
    <email>f8dy@example.com</email>
  </author>
  <author/>
  <author>   </author>
  <author><email>no-name@example.com</email></author>
  <contributor><name>Sam Ruby</name></contributor>
  <contributor><name>Joe Gregorio</name><uri>http://bitworking.example/</uri></contributor>
  <category term="web" scheme="http://example.org/cats" label="The Web"/>
  <category term="python"/>
  <entry>
    <title type="html">AT&amp;amp;T &lt;b&gt;bold&lt;/b&gt; move  </title>
    <link rel="alternate" type="text/html" href="http://example.org/2005/04/02/atom"/>
    <link href="http://example.org/2005/04/02/atom-again"/>
    <link rel="enclosure" type="audio/mpeg" length="1337" href="http://example.org/audio/ph34r_my_podcast.mp3"/>
    <link rel="enclosure" type="video/mp4" length="nope" title="The video" href="http://example.org/video/clip.mp4"/>
    <link rel="related" href="http://example.org/related"/>
    <id>tag:example.org,2003:3.2397</id>
    <updated>2005-07-31T12:29:29Z</updated>
    <published>2003-12-13T08:29:29-04:00</published>
    <author><name>Mark Pilgrim</name></author>
    <contributor><name>Sam Ruby</name></contributor>
    <contributor/>
    <category term="atom" label="Atom"/>
    <rights type="html">&lt;p&gt;Copyright 2005&lt;/p&gt;</rights>
    <summary>  A summary with   inner   spaces.  </summary>
    <content type="xhtml" xml:lang="en" xml:base="http://diveintomark.org/">
      <div xmlns="http://www.w3.org/1999/xhtml"><p><i>[Update: The Atom draft is finished.]</i></p></div>
    </content>
  </entry>
  <entry>
    <title type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml">An <b>xhtml</b> title</div></title>
    <id>tag:example.org,2003:3.2398</id>
    <updated>2005-07-30T10:00:00+02:00</updated>
    <author/>
    <summary type="html">&lt;p&gt;Only a summary, &amp;eacute;t&amp;eacute; &amp;amp; more&lt;/p&gt;</summary>
  </entry>
  <entry>
    <title type="html">&amp;lt;not a tag&amp;gt; &amp;copy; 2005 &amp;notit; &amp;#x263A; &amp;#128512;</title>
    <id>tag:example.org,2003:3.2399</id>
    <published>2005-07-29T09:00:00Z</published>
    <content type="html">&lt;p&gt;Body&lt;/p&gt;</content>
  </entry>
  <entry>
    <title></title>
    <updated>not even close</updated>
    <content>Plain text body</content>
  </entry>
</feed>
"""

FILES["feeds/atom/aggregated.xml"] = """\
<feed xmlns="http://www.w3.org/2005/Atom">
  <id>urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>
  <updated>2024-10-01T00:00:00Z</updated>
  <link rel="alternate" href="https://planet.example.org/"/>
  <entry>
    <title>From a source with authors</title>
    <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
    <updated>2024-09-30T18:30:02Z</updated>
    <source>
      <id>tag:blog.example.net,2024:feed</id>
      <title>Someone's blog</title>
      <author><name>Ada</name><email>ada@example.net</email></author>
      <author><name>Grace</name></author>
    </source>
  </entry>
  <entry>
    <title>A source without an id</title>
    <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6b</id>
    <updated>2024-09-29T18:30:02Z</updated>
    <source><title>No id here</title><author><name>Nobody</name></author></source>
  </entry>
  <entry>
    <title>Its own author wins</title>
    <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6c</id>
    <published>2024-09-28T18:30:02Z</published>
    <author><name>Linus</name></author>
    <source><id>s</id><author><name>Ignored</name></author></source>
  </entry>
</feed>
"""

FILES["feeds/atom/no-id.xml"] = '<feed xmlns="http://www.w3.org/2005/Atom"><title>No id</title></feed>\n'
FILES["feeds/atom/bad-type.xml"] = '<feed xmlns="http://www.w3.org/2005/Atom"><id>x</id><title type="text/plain">T</title></feed>\n'
FILES["feeds/atom/link-no-href.xml"] = '<feed xmlns="http://www.w3.org/2005/Atom"><id>x</id><link rel="self"/></feed>\n'
FILES["feeds/atom/category-no-term.xml"] = '<feed xmlns="http://www.w3.org/2005/Atom"><id>x</id><category label="L"/></feed>\n'
FILES["feeds/atom/empty-generator.xml"] = '<feed xmlns="http://www.w3.org/2005/Atom"><id>x</id><generator uri="u"/></feed>\n'
FILES["feeds/atom/empty-id.xml"] = '<feed xmlns="http://www.w3.org/2005/Atom"><id></id></feed>\n'
FILES["feeds/atom/prefixed.xml"] = """\
<a:feed xmlns:a="http://www.w3.org/2005/Atom" xmlns="http://example.com/other">
  <a:id>prefixed</a:id>
  <title>Not Atom's title</title>
  <a:title>Atom's title</a:title>
  <a:entry><a:id>e1</a:id><a:title>Entry</a:title><a:link href="https://example.com/e1"/></a:entry>
</a:feed>
"""
FILES["feeds/atom/old-namespace.xml"] = '<feed xmlns="http://purl.org/atom/ns#" version="0.3"><id>x</id><title>Atom 0.3</title></feed>\n'

FILES["feeds/json/blog.json"] = """\
{
  "version": "https://jsonfeed.org/version/1.1",
  "title": "My Example Feed",
  "home_page_url": "https://example.org/",
  "feed_url": "https://example.org/feed.json",
  "description": "A blog about JSON Feed \\u2014 and \\"quotes\\"",
  "user_comment": "This feed allows you to read the posts from this site in any feed reader that supports the JSON Feed format.",
  "next_url": "https://example.org/feed.json?page=2",
  "icon": "https://example.org/icon.png",
  "favicon": "https://example.org/favicon.ico",
  "author": {"name": "Brent", "url": "https://example.org/brent", "avatar": "https://example.org/b.png"},
  "expired": false,
  "items": [
    {
      "id": "2",
      "content_text": "This is a second item.",
      "url": "https://example.org/second-item",
      "title": "Second",
      "date_published": "2024-10-01T09:30:00-07:00",
      "date_modified": "2024-10-02T10:00:00Z",
      "tags": ["json", 7, "feeds", null, "web"],
      "author": {"name": null, "url": null},
      "summary": "Two",
      "image": "https://example.org/2.png",
      "banner_image": "https://example.org/2-banner.png",
      "external_url": "https://elsewhere.example.com/2"
    },
    {
      "id": "1",
      "content_html": "<p>Hello, world!</p>",
      "content_text": "Hello, world!",
      "url": "https://example.org/initial-post",
      "date_published": "Tue, 01 Oct 2024 08:00:00 PDT",
      "tags": "abc",
      "author": {"avatar": "https://example.org/a.png"},
      "attachments": []
    },
    {
      "id": "0",
      "title": "\\ud83d\\ude00 Emoji and escapes \\t\\/",
      "date_published": "",
      "author": {}
    }
  ],
  "expired": true
}
"""

FILES["feeds/json/podcast.json"] = """\
{"version": "https://jsonfeed.org/version/1", "title": "Timetable", "home_page_url": "http://timetable.example.com/",
 "items": [
  {"id": "http://timetable.example.com/episodes/42", "title": "Episode 42", "url": "http://timetable.example.com/episodes/42",
   "content_text": "Chris has a test.", "date_published": "2024-09-10T14:00:00-07:00",
   "attachments": [
     {"url": "http://timetable.example.com/media/42.m4a", "mime_type": "audio/x-m4a", "size_in_bytes": 89970236, "duration_in_seconds": 6629},
     {"url": "http://timetable.example.com/media/42-notes.pdf?dl=1", "mime_type": "application/pdf", "title": "Show notes"}
   ]},
  {"id": "http://timetable.example.com/episodes/41", "title": "Episode 41",
   "attachments": [
     {"url": "http://timetable.example.com/media/41.m4a", "mime_type": "audio/x-m4a", "size_in_bytes": true, "duration_in_seconds": 90061},
     {"url": "http://timetable.example.com/media/41-bonus.m4a", "mime_type": "audio/x-m4a", "size_in_bytes": 0, "duration_in_seconds": -1}
   ]},
  {"id": "http://timetable.example.com/episodes/40", "content_html": "<p>Short one</p>", "date_published": "2024-08-27T14:00:00-07:00",
   "attachments": [{"url": "http://timetable.example.com/media/40.mp3", "mime_type": "audio/mpeg", "duration_in_seconds": 0}]}
 ]}
"""

FILES["feeds/json/bom.json"] = '\ufeff{"version": "1", "title": "With a BOM", "items": [{"id": "a"}]}\n'
FILES["feeds/json/int-id.json"] = '{"version": "1", "title": "Integer ids", "items": [{"id": 17, "title": "x"}]}\n'
FILES["feeds/json/no-title.json"] = '{"version": "https://jsonfeed.org/version/1.1", "items": []}\n'
FILES["feeds/json/null-title.json"] = '{"version": "1", "title": null}\n'
FILES["feeds/json/list.json"] = '[{"version": "1", "title": "A list"}]\n'
FILES["feeds/json/item-string.json"] = '{"version": "1", "title": "T", "items": ["not an object"]}\n'
FILES["feeds/json/items-number.json"] = '{"version": "1", "title": "T", "items": 5}\n'
FILES["feeds/json/items-null.json"] = '{"version": "1", "title": "Null items", "items": null, "author": "Someone"}\n'
FILES["feeds/json/tags-null.json"] = '{"version": "1", "title": "T", "items": [{"id": "1", "tags": null}]}\n'
FILES["feeds/json/size-float.json"] = '{"version": "1", "title": "T", "items": [{"id": "1", "attachments": [{"url": "u", "mime_type": "m", "size_in_bytes": 1.5}]}]}\n'
FILES["feeds/json/no-mime.json"] = '{"version": "1", "title": "T", "items": [{"id": "1", "attachments": [{"url": "u"}]}]}\n'
FILES["feeds/json/trailing-comma.json"] = '{"version": "1", "title": "T",}\n'
FILES["feeds/json/single-quotes.json"] = "{'version': '1', 'title': 'T'}\n"
FILES["feeds/json/truncated.json"] = '{"version": "1", "title": "T", "items": [{"id": "1"\n'
FILES["feeds/json/extra-data.json"] = '{"version": "1", "title": "T"} {"more": 1}\n'
FILES["feeds/json/nan.json"] = '{"version": "1", "title": "NaN is fine", "items": [{"id": "1", "attachments": [{"url": "http://x.example/a.ogg", "mime_type": "audio/ogg", "size_in_bytes": NaN}]}]}\n'
FILES["feeds/json/numbers.json"] = '{"version": "1", "title": "Numbers", "items": [{"id": "1", "attachments": [{"url": "http://x.example/a.ogg", "mime_type": "audio/ogg", "size_in_bytes": -0, "duration_in_seconds": 1E2}]}]}\n'
FILES["feeds/json/leading-zero.json"] = '{"version": "1", "title": "T", "items": [{"id": "1", "attachments": [{"url": "u", "mime_type": "m", "size_in_bytes": 012}]}]}\n'
FILES["feeds/json/control-char.json"] = '{"version": "1", "title": "Tab\there"}\n'
FILES["feeds/json/bad-escape.json"] = '{"version": "1", "title": "\\q"}\n'
FILES["feeds/json/duplicate-keys.json"] = '{"title": "First", "version": "1", "title": "Second", "items": [{"id": "a", "id": "b"}]}\n'

OPML = """\
<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <head>
    <title>mySubscriptions.opml</title>
    <dateCreated>Sat, 18 Jun 2005 12:11:52 GMT</dateCreated>
    <dateModified>Tue, 02 Aug 2005 21:42:48 GMT</dateModified>
    <ownerName>Dave Example</ownerName>
    <ownerEmail>dave@example.com</ownerEmail>
    <expansionState>1, 6, 13</expansionState>
    <vertScrollState>1</vertScrollState>
    <windowTop>61</windowTop>
    <windowLeft>304</windowLeft>
    <windowBottom>562</windowBottom>
    <windowRight>842</windowRight>
  </head>
  <body>
    <outline text="Scripting News" title="Scripting News" type="rss" version="RSS2" xmlUrl="http://scripting.example.com/rss.xml" htmlUrl="http://scripting.example.com/" description="It's even worse than it appears." language="en-us"/>
    <outline text="Podcasts">
      <outline text="The Changelog-ish" type="rss" xmlUrl="https://podcast.example.com/feed.xml"/>
      <outline text="Timetable" type="rss" xmlUrl="http://timetable.example.com/feed.json"/>
      <outline text="Dead link" type="rss" xmlUrl=""/>
      <outline text="Archived">
        <outline text="Old blog" type="rss" xmlUrl="http://old.example.com/rss091.xml"/>
      </outline>
    </outline>
    <outline text="dive into mark" type="rss" xmlUrl="http://example.org/feed.atom"/>
    <outline text="A web page" type="link" url="http://example.com/page.html"/>
    <outline text="My JSON blog" type="rss" xmlUrl="https://example.org/feed.json"/>
    <outline text="Uncached" type="rss" xmlUrl="https://uncached.example.com/feed"/>
    <outline text="Broken" type="rss" xmlUrl="https://broken.example.com/feed"/>
    <outline text="Hostile" type="rss" xmlUrl="https://hostile.example.com/feed"/>
    <outline text="Planet" type="RSS" xmlUrl="https://planet.example.org/atom.xml"/>
  </body>
</opml>
"""
FILES["opml/subscriptions.opml"] = OPML
FILES["opml/minimal.opml"] = '<opml version="1.0"><head/><body><outline text="x" type="rss" xmlUrl="http://x.example/feed"/></body></opml>\n'
FILES["opml/bad-int.opml"] = '<opml version="1.0"><head><windowTop>top</windowTop></head><body/></opml>\n'
FILES["opml/no-head.opml"] = '<opml version="1.0"><body/></opml>\n'
FILES["opml/no-body.opml"] = '<opml version="1.0"><head><title>t</title></head></opml>\n'

FILES["bad/unclosed.xml"] = '<rss version="2.0"><channel><title>Oops</channel></rss>\n'
FILES["bad/undefined-entity.xml"] = '<rss version="2.0"><channel><title>A&nbsp;B</title></channel></rss>\n'
FILES["bad/billion-laughs.xml"] = """\
<?xml version="1.0"?>
<!DOCTYPE lolz [
 <!ENTITY lol "lol">
 <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
 <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
]>
<rss version="2.0"><channel><title>&lol2;</title></channel></rss>
"""
FILES["bad/xxe.xml"] = """\
<?xml version="1.0"?>
<!DOCTYPE rss [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<rss version="2.0"><channel><title>&xxe;</title></channel></rss>
"""
FILES["bad/public-entity.xml"] = """\
<!DOCTYPE rss [
  <!-- a comment first -->
  <!ENTITY % ext PUBLIC "-//Example//Entities//EN" 'http://example.com/ents.dtd'>
]>
<rss version="2.0"/>
"""
FILES["bad/plain-doctype.xml"] = '<!DOCTYPE rss SYSTEM "rss.dtd">\n<rss version="2.0"><channel><title>A doctype is fine</title></channel></rss>\n'
FILES["bad/empty.xml"] = ""
FILES["bad/html.html"] = '<!doctype html>\n<html><head><title>Not a feed</title></head><body><p>Hi<br></body></html>\n'
FILES["bad/foreign-root.xml"] = '<?xml version="1.0"?>\n<sitemap><loc>https://example.com/</loc></sitemap>\n'

_CACHE = {
    "http://scripting.example.com/rss.xml": "feeds/rss/scripting-news.xml",
    "https://podcast.example.com/feed.xml": "feeds/rss/podcast.xml",
    "http://timetable.example.com/feed.json": "feeds/json/podcast.json",
    "http://old.example.com/rss091.xml": "feeds/rss/v091.xml",
    "http://example.org/feed.atom": "feeds/atom/blog.xml",
    "https://example.org/feed.json": "feeds/json/blog.json",
    "https://broken.example.com/feed": "bad/unclosed.xml",
    "https://hostile.example.com/feed": "bad/billion-laughs.xml",
    "https://planet.example.org/atom.xml": "feeds/atom/aggregated.xml",
}
FILES["cache/urls.tsv"] = "".join("%s\t%s\n" % kv for kv in _CACHE.items())

BYTES = {
    "feeds/json/latin1.json": '{"version": "1", "title": "Caf\xe9"}\n'.encode("latin-1"),
}

RSS_JOBS = [
    "scripting-news.xml", "podcast.xml", "dates.xml", "link-only.xml",
    "no-title-no-link.xml", "v091.xml", "no-channel.xml", "bad-ttl.xml",
    "ttl-spaces.xml", "image-no-url.xml", "enclosure-no-url.xml",
    "empty-source.xml", "required-empty.xml",
]
ATOM_JOBS = [
    "blog.xml", "aggregated.xml", "no-id.xml", "bad-type.xml",
    "link-no-href.xml", "category-no-term.xml", "empty-generator.xml",
    "empty-id.xml", "prefixed.xml", "old-namespace.xml",
]
JSON_JOBS = [
    "blog.json", "podcast.json", "bom.json", "int-id.json", "no-title.json",
    "null-title.json", "list.json", "item-string.json", "items-number.json",
    "items-null.json", "tags-null.json", "size-float.json", "no-mime.json",
    "trailing-comma.json", "single-quotes.json", "truncated.json",
    "extra-data.json", "nan.json", "numbers.json", "leading-zero.json",
    "control-char.json", "bad-escape.json", "duplicate-keys.json",
    "latin1.json",
]
BAD = ["unclosed.xml", "undefined-entity.xml", "billion-laughs.xml",
       "xxe.xml", "public-entity.xml", "plain-doctype.xml", "empty.xml",
       "html.html", "foreign-root.xml", "missing.xml"]

SIMPLE = (
    ["feeds/rss/" + n for n in ("scripting-news.xml", "podcast.xml",
                                "link-only.xml", "no-title-no-link.xml",
                                "v091.xml", "bad-ttl.xml")]
    + ["feeds/atom/" + n for n in ("blog.xml", "aggregated.xml",
                                   "no-id.xml", "prefixed.xml")]
    + ["feeds/json/" + n for n in ("blog.json", "podcast.json", "bom.json",
                                   "no-title.json", "list.json",
                                   "trailing-comma.json", "latin1.json")]
    + ["bad/" + n for n in BAD]
    + ["opml/subscriptions.opml"]
)
SIMPLE_BYTES = ["feeds/json/bom.json", "feeds/atom/blog.xml",
                "feeds/json/latin1.json", "bad/empty.xml"]

DATE_JOBS = DATES + [
    "Sun, 06 Nov 1994 08:49:37 MDT",
    "Sunday, 06-Nov-94 08:49:37 GMT",
    "Sun Nov  6 08:49:37 1994",
    "1994-11-06T08:49:37.123456+01:00",
    "2024-02-30T00:00:00Z",
    "Wed, 02 Oct 2002 08:00:00 EST trailing words",
    "Wed, 02 Oct 2002 13:00:00 GMT+02:00",
    "20240101T120000",
]


def main():
    for name, text in FILES.items():
        path = os.path.join(DATA, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
    for name, raw in BYTES.items():
        with open(os.path.join(DATA, name), "wb") as fh:
            fh.write(raw)
    jobs = ["# RSS 2.0"]
    jobs += ["rss\tdata/feeds/rss/" + n for n in RSS_JOBS]
    jobs.append("# Atom 1.0")
    jobs += ["atom\tdata/feeds/atom/" + n for n in ATOM_JOBS]
    jobs.append("# JSON Feed, from a file and from bytes")
    for n in JSON_JOBS:
        jobs.append("json\tdata/feeds/json/" + n)
        if n in ("bom.json", "blog.json", "latin1.json", "list.json"):
            jobs.append("json_bytes\tdata/feeds/json/" + n)
    jobs.append("# OPML")
    for n in ("subscriptions.opml", "minimal.opml", "bad-int.opml",
              "no-head.opml", "no-body.opml"):
        jobs.append("opml\tdata/opml/" + n)
    jobs.append("# broken and hostile XML")
    jobs += ["rss\tdata/bad/" + n for n in BAD]
    jobs.append("# the simple API, from a file and from bytes")
    jobs += ["simple\tdata/" + n for n in SIMPLE]
    jobs += ["simple_bytes\tdata/" + n for n in SIMPLE_BYTES]
    jobs.append("# dates, as the parsers read them")
    jobs += ["date\t" + d for d in DATE_JOBS]
    jobs.append("# programs")
    jobs.append("river\tdata/opml/subscriptions.opml")
    jobs.append("river\tdata/opml/minimal.opml")
    jobs.append("podcast\tdata/feeds/rss/podcast.xml")
    jobs.append("podcast\tdata/feeds/json/podcast.json")
    jobs.append("podcast\tdata/feeds/atom/blog.xml")
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(jobs) + "\n")
    files = sorted(list(FILES) + list(BYTES))
    with open(os.path.join(DATA, "files.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(files) + "\n")


main()
