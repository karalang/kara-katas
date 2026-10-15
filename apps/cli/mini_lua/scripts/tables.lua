-- tables as arrays, records, sets and matrices
local t = {10, 20, 30, x = 1, ["y z"] = 2, [100] = "hundred"}
print(#t, t[1], t.x, t["y z"], t[100], t[4])
t[#t + 1] = 40
table.insert(t, 50)
table.insert(t, 1, 5)
print(#t, table.concat(t, " "))
print(table.remove(t), table.remove(t, 1), #t, table.concat(t, "-"))
t[2] = nil
print(t[1], t[2], t[3])

local words = {"pear", "apple", "fig", "banana", "cherry", "date"}
table.sort(words)
print(table.concat(words, " "))
table.sort(words, function(a, b) return #a < #b or (#a == #b and a < b) end)
print(table.concat(words, " "))
local nums = {5, 3, 9, 1, 7, 2, 8, 6, 4}
table.sort(nums, function(a, b) return a > b end)
print(table.concat(nums, ","))

local inventory = {apples = 4, pears = 0, plums = 12, kiwis = 3}
local keys = {}
for k in pairs(inventory) do keys[#keys + 1] = k end
table.sort(keys)
for _, k in ipairs(keys) do io.write(k, "=", inventory[k], " ") end
print()
inventory.pears = nil
local n = 0
for _, v in pairs(inventory) do n = n + v end
print("total", n)

local set = {}
for w in ("a b c a b a"):gmatch("%a") do set[w] = (set[w] or 0) + 1 end
print(set.a, set.b, set.c, set.d)

local m = {}
for i = 1, 3 do
  m[i] = {}
  for j = 1, 3 do m[i][j] = (i - 1) * 3 + j end
end
local rows = {}
for i = 1, 3 do rows[i] = table.concat(m[i], " ") end
print(table.concat(rows, " | "))
local tr = {}
for i = 1, 3 do
  tr[i] = {}
  for j = 1, 3 do tr[i][j] = m[j][i] end
end
print(tr[1][3], tr[3][1], #tr, #tr[2])

local a = {1, 2, 3}
local b = a
b[1] = 99
print(a[1], a == b, {} == {})
local nested = {inner = {deep = {value = "found"}}}
print(nested.inner.deep.value)
local fkey = {}
fkey[1.0] = "one"
fkey[2] = "two"
print(fkey[1], fkey[2.0], #fkey)
local stack = {}
for i = 1, 5 do stack[#stack + 1] = i * i end
while #stack > 0 do io.write(table.remove(stack), " ") end
print()
print(select("#", 1, 2, 3), next({}))
