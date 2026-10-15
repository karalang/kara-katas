# Per-status report over an access log.
function bucket(code) {
    return int(code / 100) "xx"
}
{
    b = bucket($9)
    if (!(b in count)) order[++n] = b
    count[b]++
    bytes[b] += $10
}
END {
    for (i = 1; i <= n; i++) {
        b = order[i]
        printf "%s %3d requests %8d bytes\n", b, count[b], bytes[b]
    }
}
