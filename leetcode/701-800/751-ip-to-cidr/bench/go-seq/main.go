// LeetCode 751 — IP to CIDR, bench: the ★ arm (greedy by the lowest
// set bit) on half a million ranges from a pool of 1000 addresses.
// Mirrors ip_to_cidr.kara.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func address(ip string) int64 {
	var x int64
	for _, part := range strings.Split(ip, ".") {
		v, _ := strconv.ParseInt(part, 10, 64)
		x = x*256 + v
	}
	return x
}

func dotted(x int64) string {
	return fmt.Sprintf("%d.%d.%d.%d", x/16777216%256, x/65536%256, x/256%256, x%256)
}

func ipToCIDR(ip string, n int64) []string {
	x := address(ip)
	left := n
	var out []string
	for left > 0 {
		var size int64
		if x == 0 {
			size = 4294967296
		} else {
			size = x & -x
		}
		for size > left {
			size /= 2
		}
		var bits int64
		for (int64(1) << bits) < size {
			bits++
		}
		out = append(out, fmt.Sprintf("%s/%d", dotted(x), 32-bits))
		x += size
		left -= size
	}
	return out
}

var seed int64 = 751

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const queries = 500000
	pool := make([]string, 1000)
	for i := range pool {
		a := nextRandom() % 255
		b := nextRandom() % 256
		c := nextRandom() % 256
		d := nextRandom() % 256
		pool[i] = fmt.Sprintf("%d.%d.%d.%d", a, b, c, d)
	}
	var blocks, check int64
	for q := 0; q < queries; q++ {
		n := 1 + nextRandom()%1000
		found := ipToCIDR(pool[q%1000], n)
		blocks += int64(len(found))
		for _, block := range found {
			check = (check*31 + int64(len(block))) % 1000000007
		}
	}
	fmt.Printf("%d ranges: %d blocks in all, checksum %d\n", queries, blocks, check)
}
