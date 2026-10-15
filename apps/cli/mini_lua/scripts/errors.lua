-- errors and pcall
local function risky(n)
  if n > 2 then
    error("too big: " .. n)
  end
  return n * 2
end
print(pcall(risky, 1))
print(pcall(risky, 5))
print(pcall(error, "plain", 0))
local ok, e = pcall(error, {code = 42})
print(ok, type(e), e.code)
print(pcall(function() error("level two", 2) end))
local function outer()
  local function inner() error("deep") end
  inner()
end
print(pcall(outer))
print(pcall(assert, false, "assertion text"))
print(pcall(assert, 1 == 1, "never"))
print(select("#", pcall(assert, nil)))
local ok2, msg = pcall(function()
  local ok3, inner = pcall(error, "first")
  error("second after " .. inner, 0)
end)
print(ok2, msg)
local results = {}
for i = 1, 4 do
  local ok4, v = pcall(risky, i)
  results[#results + 1] = ok4 and tostring(v) or "fail"
end
print(table.concat(results, " "))
local function retry(times, f)
  local last
  for attempt = 1, times do
    local ok5, v = pcall(f, attempt)
    if ok5 then return v, attempt end
    last = v
  end
  return nil, last
end
print(retry(3, function(n) if n < 3 then error("not yet", 0) end return "done" end))
print(retry(2, function(n) error("never " .. n, 0) end))
