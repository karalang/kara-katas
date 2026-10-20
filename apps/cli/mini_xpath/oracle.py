# Runs data/ through lxml (libxml2's XPath and libxslt) and prints what
# expected.out holds. Run it from the app directory, after mk.py.
from lxml import etree


def read_lines(path):
    with open(path, encoding="utf-8", newline="") as f:
        return [line[:-1] if line.endswith("\n") else line for line in f]


def parse(name):
    return etree.parse("data/docs/" + name)


def qname(el):
    local = etree.QName(el).localname
    return el.prefix + ":" + local if el.prefix else local


# Each element as the names of its ancestors and itself, each with its
# position among the siblings of the same name.
def path(el):
    parts = []
    while el is not None:
        n = 1
        sib = el.getprevious()
        while sib is not None:
            if isinstance(sib.tag, str) and sib.tag == el.tag:
                n += 1
            sib = sib.getprevious()
        parts.append("%s[%d]" % (qname(el), n))
        el = el.getparent()
    return "/" + "/".join(reversed(parts))


def attr_name(el, clark):
    if clark.startswith("{"):
        uri, local = clark[1:].split("}")
        if uri == "http://www.w3.org/XML/1998/namespace":
            return "xml:" + local
        for p, u in el.nsmap.items():
            if u == uri and p:
                return p + ":" + local
    return clark


def show(item):
    if isinstance(item, etree._Comment):
        return "comment " + repr(item.text)
    if isinstance(item, etree._ProcessingInstruction):
        return "pi %s %r" % (item.target, item.text)
    if isinstance(item, etree._Element):
        return "<%s>" % path(item)
    if isinstance(item, tuple):
        return "ns " + repr(item)
    if item.is_attribute:
        el = item.getparent()
        return "@%s=%r on <%s>" % (attr_name(el, item.attrname), str(item), path(el))
    owner = item.getparent()
    if item.is_tail:
        owner = owner.getparent()
    return "text %r in <%s>" % (str(item), path(owner))


def run_queries():
    print("== queries")
    tree = None
    nss = {}
    vars_ = {}
    for line in read_lines("data/queries.txt"):
        kind, rest = line.split(" ", 1)
        if kind == "doc":
            print("doc " + rest)
            tree = parse(rest)
            nss = {}
            vars_ = {}
        elif kind == "ns":
            p, u = rest.split(" ")
            nss[p] = u
        elif kind == "var":
            t, name, v = rest.split(" ", 2)
            vars_[name] = (v == "True") if t == "bool" else float(v) if t == "num" else v
        else:
            print("q " + rest)
            try:
                r = tree.xpath(rest, namespaces=nss, **vars_)
            except etree.XPathError as e:
                print("  ! %s: %s" % (type(e).__name__, e))
                continue
            if isinstance(r, list):
                if not r:
                    print("  []")
                for item in r:
                    print("  " + show(item))
            elif isinstance(r, bool):
                print("  " + str(r))
            elif isinstance(r, float):
                print("  " + repr(r))
            else:
                print("  " + repr(str(r)))


XSL = "http://www.w3.org/1999/XSL/Transform"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def literal(s):
    return "'" + s + "'" if "'" not in s else '"' + s + '"'


# The stylesheet xmlstarlet sel writes for its arguments.
def stylesheet(args):
    nss = []
    body = []
    open_ = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-N":
            p, u = args[i + 1].split("=", 1)
            nss.append((p, u))
            i += 2
        elif a == "-t":
            i += 1
        elif a == "-m":
            body.append('<xsl:for-each select="%s">' % esc(args[i + 1]))
            open_.append("for-each")
            i += 2
        elif a == "-s":
            order, dtype, _ = args[i + 1].split(":")
            body.append('<xsl:sort order="%s" data-type="%s" select="%s"/>' % (
                "ascending" if order == "A" else "descending",
                "number" if dtype == "N" else "text", esc(args[i + 2])))
            i += 3
        elif a == "-i":
            body.append('<xsl:if test="%s">' % esc(args[i + 1]))
            open_.append("if")
            i += 2
        elif a == "-b":
            body.append("</xsl:%s>" % open_.pop())
            i += 1
        elif a == "-v":
            body.append('<xsl:call-template name="value-of-template"><xsl:with-param name="select" select="%s"/></xsl:call-template>' % esc(args[i + 1]))
            i += 2
        elif a == "-c":
            body.append('<xsl:copy-of select="%s"/>' % esc(args[i + 1]))
            i += 2
        elif a == "-o":
            body.append('<xsl:value-of select="%s"/>' % esc(literal(args[i + 1])))
            i += 2
        elif a == "-n":
            body.append("<xsl:value-of select=\"'&#10;'\"/>")
            i += 1
        else:
            raise ValueError(a)
    while open_:
        body.append("</xsl:%s>" % open_.pop())
    decls = "".join(' xmlns:%s="%s"' % (p, esc(u)) for p, u in nss)
    return """<xsl:stylesheet version="1.0" xmlns:xsl="%s" xmlns:exslt="http://exslt.org/common" extension-element-prefixes="exslt"%s>
<xsl:output omit-xml-declaration="yes" indent="no" method="text"/>
<xsl:template match="/">%s</xsl:template>
<xsl:template name="value-of-template">
<xsl:param name="select"/>
<xsl:value-of select="$select"/>
<xsl:for-each select="exslt:node-set($select)[position()&gt;1]">
<xsl:value-of select="'&#10;'"/>
<xsl:value-of select="."/>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>""" % (XSL, decls, "".join(body))


def run_sel():
    for line in read_lines("data/sel.tsv"):
        f = line.split("\t")
        print("== xmlstarlet sel " + " ".join(f[1:]) + " " + f[0])
        xslt = etree.XSLT(etree.fromstring(stylesheet(f[1:]).encode()))
        out = str(xslt(parse(f[0])))
        for l in out.split("\n"):
            print("| " + l)


run_queries()
run_sel()
