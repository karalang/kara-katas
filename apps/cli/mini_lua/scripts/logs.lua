-- an access-log report: parse each line with a pattern, aggregate, rank
local pattern = '^(%S+) %S+ %S+ %[([^%]]+)%] "(%u+) (%S+) [^"]*" (%d+) (%d+) (%d+)ms "([^"]*)"$'
local by_status, by_path, by_ip = {}, {}, {}
local bytes, slow, total, bad = 0, {}, 0, 0
for line in io.lines("data/access.log") do
  local ip, when, method, path, status, size, ms, agent = line:match(pattern)
  if not ip then
    bad = bad + 1
  else
    total = total + 1
    status = tonumber(status)
    by_status[status] = (by_status[status] or 0) + 1
    path = path:gsub("%?.*$", "")
    local p = by_path[path] or {hits = 0, ms = 0, errors = 0}
    p.hits = p.hits + 1
    p.ms = p.ms + tonumber(ms)
    if status >= 500 then p.errors = p.errors + 1 end
    by_path[path] = p
    by_ip[ip] = (by_ip[ip] or 0) + 1
    bytes = bytes + tonumber(size)
    if tonumber(ms) >= 800 then
      slow[#slow + 1] = string.format("%s %s %s %dms", when:match(":(%d+:%d+:%d+)"), method, path, ms)
    end
  end
end
print(string.format("%d requests, %d unparsed, %.1f KiB sent", total, bad, bytes / 1024))
local codes = {}
for code in pairs(by_status) do codes[#codes + 1] = code end
table.sort(codes)
for _, code in ipairs(codes) do
  print(string.format("  %d %3d %5.1f%%", code, by_status[code], 100 * by_status[code] / total))
end
local paths = {}
for path, p in pairs(by_path) do paths[#paths + 1] = {path = path, p = p} end
table.sort(paths, function(a, b)
  if a.p.hits ~= b.p.hits then return a.p.hits > b.p.hits end
  return a.path < b.path
end)
print("top paths:")
for i = 1, 5 do
  local e = paths[i]
  print(string.format("  %-18s %3d hits  avg %6.1fms  %d errors", e.path, e.p.hits, e.p.ms / e.p.hits, e.p.errors))
end
local ips = {}
for ip, n in pairs(by_ip) do ips[#ips + 1] = ip end
table.sort(ips, function(a, b) return by_ip[a] > by_ip[b] or (by_ip[a] == by_ip[b] and a < b) end)
io.write("clients:")
for _, ip in ipairs(ips) do io.write(" ", ip, "=", by_ip[ip]) end
print()
print("slow requests (" .. #slow .. "):")
for i = 1, math.min(4, #slow) do print("  " .. slow[i]) end
local out = io.open("report.txt", "w")
out:write("total=", total, "\n", "bytes=", bytes, "\n")
out:close()
local back = {}
for l in io.lines("report.txt") do back[#back + 1] = l end
print("report.txt: " .. table.concat(back, ";"))
