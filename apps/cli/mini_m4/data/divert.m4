divert(1)this goes to diversion 1
divert(2)this goes to diversion 2
divert(0)dnl
start divnum
undivert(2)dnl
divert(3)three: divnum
divert(-1)this is discarded
define(`later', `defined while discarding')
divert`'dnl
after: later
m4wrap(`wrapped one
')m4wrap(`wrapped two
')dnl
divert(4)four
undivert(1)dnl
divert`'dnl
divert(1)one again
divert`'dnl
undivert(9)undivert(-1)dnl
end of the file
