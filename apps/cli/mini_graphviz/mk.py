"""Writes data/script.txt for mini_graphviz: the DOT source of a small
service fleet's dependency map, built a statement at a time, with the
quoting cases the library handles and a mistake for each rule it checks.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)

SCRIPT = r"""# A service fleet's dependency map. `\s` in a word is a space, `\N` a
# newline; a value starting with `!` is nohtml, one starting with `%` is
# escaped.

begin legend graph name=Legend comment=How\sto\sread\sthe\smap graph.rankdir=LR node.tooltip=see\sC:\docs\
node ok label=healthy color=green
node warn label=degraded color=orange
node down label=<<b>down</b>> color=red
edge ok warn style=dashed
end
print legend

begin fleet digraph name=fleet\smap comment=Generated\sfrom\sthe\sinventory graph.rankdir=LR graph.splines=ortho node.shape=box node.fontname=Helvetica edge.arrowsize=0.7
node gateway label=API\sgateway
node auth label=auth-service tier=1
node orders label=Orders tier=2 color=blue
node 42 label=answer
node -1.5 label=negative
node .5 label=half
node 7. label=trailing\sdot
node 1e3 label=not\sa\sDOT\snumber
node Node label=a\skeyword\sin\sany\scase
node subgraph label=lower\scase\skeyword
node café label=accented
node _private
node "quoted" label=say\s"hi"
node back\"slash label=already\sescaped
node two\\\"slashes label=even\sbackslashes
node trailing\ label=odd\sbackslash\sat\sthe\send
node it's\ label=a\squote\stoo
node ends\\ label=even\sbackslashes\sat\sthe\send
node line\N label=a\snewline\sat\sthe\send
node <tag> label=an\sHTML-like\sname
node !<tag> label=nohtml
node %C:\temp label=escaped
node db label=Postgres\\lprimary\\l shape=cylinder
node cache label=Redis shape=cylinder style=filled fillcolor=!<lightgrey>
edge gateway auth label=checks\stoken
edge gateway orders weight=2
edge orders db:w label=writes
edge orders:out:e cache:in:w label=reads
edge orders:p1:e:extra db
edge !<tag> db
edge !<tag>:<port> db
edge %a\b db
edge "x":"y" db
edges auth db auth cache
edges gateway
attr rank=same nodesep=0.3
attr graph label=Fleet\smap fontsize=20
attr Node shape=ellipse
attr edge
attr cluster color=red
attr node bad
subgraph name=cluster_data graph.label=Data\sstores graph.style=filled node.style=filled
node db
node cache
subgraph name=cluster_cold comment=Cold\sstorage graph.label=Archive
node archive label=S3\sbucket
edge db archive label=nightly
end
attr color=lightgrey
end
subgraph
node queue
edge orders queue
end
include legend
end
print fleet

# Copies, clears and other graphs.
copy fleet fleet_v2
clear fleet_v2 keep
print fleet_v2
copy fleet fleet_v3
clear fleet_v3
print fleet_v3

begin strictly digraph strict name=strict
node a
edge a b
edge a b
end
print strictly
begin undirected graph
node a
node b label=
edge a b
include strictly
include legend
end
print undirected
begin with_strict digraph
include strictly
include fleet
include legend
end
print with_strict

# Mistakes.
node outside
end
include legend
begin late graph
begin again graph
print fleet
copy fleet nope
clear fleet
save fleet fleet.gv
attr
edge a
edges a b c
node
node x bad
node x label
include
include nosuch
end
begin late digraph
begin bad graph shape=box
begin bad graph name=a name=b
begin bad graph nodes.shape=box
begin bad tree
begin
begin fleet graph
print nosuch
print
copy nosuch x
copy fleet
copy fleet legend
clear nosuch
clear fleet all
save nosuch x.gv
save fleet ../escape.gv
save fleet Fleet.gv
save fleet
render fleet

save fleet fleet.gv
save undirected undirected.gv
"""

with open(os.path.join("data", "script.txt"), "w", encoding="utf-8", newline="") as fh:
    fh.write(SCRIPT)
