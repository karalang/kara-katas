-- closures, upvalues and multiple results
local function counter(start)
  local n = start
  return function(step)
    n = n + (step or 1)
    return n
  end
end
local c1, c2 = counter(0), counter(100)
print(c1(), c1(), c1(5), c2(), c1())

local fns = {}
for i = 1, 3 do
  fns[i] = function() return i * 10 end
end
print(fns[1](), fns[2](), fns[3]())

local function shared()
  local v = 0
  local function get() return v end
  local function set(x) v = x end
  return get, set
end
local get, set = shared()
set(7)
print(get())

local function fib(n)
  if n < 2 then return n end
  return fib(n - 1) + fib(n - 2)
end
print(fib(20))

local function map(t, f)
  local out = {}
  for i, v in ipairs(t) do out[i] = f(v) end
  return out
end
local function filter(t, p)
  local out = {}
  for _, v in ipairs(t) do
    if p(v) then out[#out + 1] = v end
  end
  return out
end
local function reduce(t, f, acc)
  for _, v in ipairs(t) do acc = f(acc, v) end
  return acc
end
local nums = {}
for i = 1, 10 do nums[#nums + 1] = i end
local sq = map(nums, function(x) return x * x end)
local even = filter(sq, function(x) return x % 2 == 0 end)
print(table.concat(even, ","), reduce(sq, function(a, b) return a + b end, 0))

local function divmod(a, b) return a // b, a % b end
local q, r = divmod(17, 5)
print(q, r)
local a, b, c = divmod(9, 4)
print(a, b, c)
local x, y = 1, 2
x, y = y, x
print(x, y)
print((divmod(17, 5)))
local t = {divmod(20, 6), divmod(7, 2)}
print(#t, t[1], t[2], t[3])

local acc = 0
local i = 10
while i > 0 do
  acc = acc + i
  i = i - 3
end
repeat acc = acc - 1 until acc % 4 == 0
print(acc)
for k = 10, 1, -4 do io.write(k, " ") end
for k = 1, 2, 0.5 do io.write(k, " ") end
print()
for n = 1, 20 do
  if n % 7 == 0 then print("first multiple of 7:", n) break end
end
