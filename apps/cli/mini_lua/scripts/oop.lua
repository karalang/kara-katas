-- classes with metatables
local Account = {}
Account.__index = Account

function Account.new(owner, balance)
  local self = setmetatable({}, Account)
  self.owner = owner
  self.balance = balance or 0
  return self
end

function Account:deposit(v)
  self.balance = self.balance + v
  return self
end

function Account:withdraw(v)
  if v > self.balance then
    error("insufficient funds")
  end
  self.balance = self.balance - v
end

Account.__tostring = function(a)
  return "Account(" .. a.owner .. ", " .. a.balance .. ")"
end

local acc = Account.new("ada", 100)
acc:deposit(50):deposit(25)
print(acc.balance, tostring(acc))
print(acc)
local ok, err = pcall(acc.withdraw, acc, 1000)
print(ok, err)
acc:withdraw(75)
print(acc.balance)

local Savings = setmetatable({}, {__index = Account})
Savings.__index = Savings
Savings.__tostring = Account.__tostring

function Savings.new(owner, balance, rate)
  local self = Account.new(owner, balance)
  self.rate = rate
  return setmetatable(self, Savings)
end

function Savings:interest()
  return self.balance * self.rate
end

local s = Savings.new("grace", 1000, 0.05)
s:deposit(200)
print(s.balance, s:interest(), tostring(s), getmetatable(s) == Savings)
print(rawget(s, "deposit"), s.deposit == Account.deposit)

local Stack = {}
Stack.__index = Stack
function Stack.new() return setmetatable({items = {}, size = 0}, Stack) end
function Stack:push(v) self.size = self.size + 1; self.items[self.size] = v end
function Stack:pop()
  if self.size == 0 then return nil end
  local v = self.items[self.size]
  self.items[self.size] = nil
  self.size = self.size - 1
  return v
end
local st = Stack.new()
for _, w in ipairs({"a", "b", "c"}) do st:push(w) end
print(st:pop(), st:pop(), st.size, st:pop(), st:pop())

local defaults = setmetatable({}, {__index = function(t, k) return k .. "?" end})
defaults.known = "yes"
print(defaults.known, defaults.missing)

local Vec = {}
Vec.__index = Vec
local function vec(x, y) return setmetatable({x = x, y = y}, Vec) end
Vec.__add = function(a, b) return vec(a.x + b.x, a.y + b.y) end
Vec.__eq = function(a, b) return a.x == b.x and a.y == b.y end
Vec.__tostring = function(v) return "(" .. v.x .. ", " .. v.y .. ")" end
Vec.__lt = function(a, b) return a.x < b.x end
local p = vec(1, 2) + vec(3, 4)
print(tostring(p), p == vec(4, 6), p == vec(0, 0), vec(1, 0) < vec(2, 0))
