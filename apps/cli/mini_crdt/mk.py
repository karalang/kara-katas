"""Writes data/ for mini_crdt: five sessions of replicas editing shared
objects offline and syncing, and one with mistakes in it.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)

SESSIONS = {
    "1_counters.crdt": """# Three app servers count page views and adjust stock while cut off
# from each other, then sync. Counters add up whatever the order.
replicas a b c
a counter views add 3
b counter views add 2
c counter views add 5
a counter stock add 40
b counter stock add -3
c counter stock add -4
show a
sync a b
show b
sync b c
sync c a
show a
check
a counter stock add -1
check
sync all
check
""",
    "2_cart.crdt": """# A shared shopping list on two phones and a laptop. The set is
# add-wins: a remove takes away only the adds its replica had seen.
replicas phone tablet laptop
phone set cart add milk
phone set cart add eggs
sync phone tablet
tablet set cart remove milk
laptop set cart add milk
laptop set cart add bread
phone set cart add milk
show tablet
sync all
show phone
check
tablet set cart remove milk
tablet set cart remove bread
laptop set cart remove bread
sync all
show laptop
laptop set cart remove butter
check
""",
    "3_profile.crdt": """# A profile edited on three devices. Each field is a last-writer-wins
# register: the higher Lamport time wins, and a tie goes to the later
# replica name.
replicas web ios android
web reg name set Ada
ios reg name set Ada_L
android reg city set Paris
sync web ios
ios reg city set Lyon
android reg name set Ada_Lovelace
web reg city set Nice
show web
sync all
show ios
check
web reg name set Countess
sync web android
show android
sync all
check
""",
    "4_doc.crdt": """# Two writers and a reviewer edit one document. Concurrent inserts at
# the same place keep both, in Lamport order, and never interleave.
replicas ann bob cy
ann text doc insert 0 The cat sat.
sync ann bob
sync ann cy
ann text doc insert 4 black 
bob text doc insert 4 fat 
cy text doc delete 4 4
show ann
show bob
sync all
show cy
check
bob text doc insert 0 >> 
ann text doc delete 0 3
cy text doc insert 18 !
cy text doc delete 0 40
sync all
show bob
check
""",
    "5_offline.crdt": """# A field app: two tablets and a server. One tablet goes offline for
# a shift and crashes; it restarts from its op log and syncs.
replicas server t1 t2
server set sites add north
server set sites add south
server reg lead set kim
sync all
t1 counter samples add 12
t1 set sites add east
t1 text notes insert 0 north: clear
t2 counter samples add 7
t2 set sites remove south
t2 text notes insert 0 south: closed
sync t2 server
crash t1
t1 counter samples add 1
sync server t1
sync all
show server
restart t1
show t1
t1 reg lead set lee
t1 text notes insert 12 ;
sync t1 server
sync server t2
show t2
crash t2
sync all
restart t2
sync all
show t2
check
""",
    "6_bad.crdt": """# Mistakes the loader reports.
a counter x add 1
replicas a b
replicas a c
z counter x add 1
a set cart add milk
a counter cart add 1
a counter n add many
a text doc insert x hello
b gadget g poke
sync a
a reg title set two words
""",
}
for name, text in SESSIONS.items():
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
