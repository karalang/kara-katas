"""Writes data/ for mini_transitions: three state machines (a door, a
nested alarm and a counter) with their variables, conditions, actions and
callbacks, and a script of events and control commands with a few
mistakes in both files.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def put(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


put("machines.conf", """\
# A front door, the alarm it talks to, and a visitor counter.

machine door
var keys 1
var opens 0
var locked_at 0
state closed initial
state open
state locked
state broken final
cond has_key keys > 0
cond no_key keys <= 0
cond worn opens >= 4
action chime say ding dong
action count add opens 1
action note_lock set locked_at 1
action unnote_lock set locked_at 0
action tell_alarm trigger alarm door_opened
action creak say the hinge creaks
transition open closed -> open before=count after=tell_alarm
transition open open -> = before=creak
transition close open -> closed
transition lock closed -> locked if=has_key after=note_lock
transition lock closed -> locked unless=has_key before=creak
transition unlock locked -> closed if=has_key after=unnote_lock
transition kick locked -> broken if=worn
transition kick * -> = before=creak
on_enter open chime
on_exit locked creak

machine alarm
queued
var trips 0
var armed 0
state off initial
state on
state on.armed
state on.armed.away
state on.armed.stay
state on.tripped
action siren say WEEOO
action trip add trips 1
action arm_flag set armed 1
action disarm_flag set armed 0
action calm trigger alarm reset
action loop trigger alarm door_opened
transition arm off -> on.armed.away after=arm_flag
transition stay on.armed.away -> on.armed.stay
transition door_opened on.armed -> on.tripped before=trip after=siren
transition door_opened off -> =
transition disarm on -> off after=disarm_flag
transition reset on.tripped -> on.armed.away after=loop
on_enter on.tripped calm
on_exit on.armed disarm_flag
on_enter on.armed arm_flag

machine counter
var n 0
state idle initial
state busy
action inc add n 1
action dec add n -1
action again trigger spin
action page trigger pager page
transition tick idle -> busy after=inc
transition tick busy -> = after=inc
transition untick busy -> = after=dec
transition rest busy -> idle
transition spin busy -> = before=inc after=again
transition ping * -> = after=page

# Mistakes, each reported and skipped.
machine door
machine Bad-Name
state nowhere
machine extra
var x 1
var x 2
var y lots
state a initial
state b initial
state c.d
state a
state e final
cond c1 x ~ 3
cond c2 z > 1
cond c3 x > 1
action a1 dance x
action a2 add z 1
action a3 add x
action a4 trigger
transition go a -> nope
transition go e -> a
transition go a -> e if=c9
transition go a -> e sometimes=c3
transition to_b a -> b
transition go a b
on_enter zz a1
on_exit a nope
frobnicate
machine stateless
var v 0
""")

put("events.log", """\
# A morning at the front door.
door open
door close
@ state door
door lock
door open
door unlock
door open
door open
alarm arm
@ triggers alarm
door close
door open
alarm stay
door close
door open
alarm reset
@ state alarm
alarm disarm
alarm stay
@ set door keys 0
door close
door lock
door unlock
@ set door keys 1
door unlock
counter tick
counter tick
counter untick
counter to_idle
counter to_busy
counter spin
counter to_nowhere
counter rest
counter ping
@ triggers counter
door kick
door lock
door kick
door to_closed
door open
@ triggers door
@ state door
nosuch go
alarm
@ set door keys many
@ set door ghosts 1
@ state nosuch
@ frobnicate
@
alarm to_on.armed.stay
alarm door_opened
@ state alarm
counter extra
""")
