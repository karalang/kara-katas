// LeetCode #1802: Maximum Value at a Given Index in a Bounded Array -- the
// bench in Go: the ★ arm over 4000 random cases built once, 1000000 calls.
package main

import "fmt"

func side(v, k int64) int64 {
	if k <= v-1 {
		return (v - 1 + v - k) * k / 2
	}
	return (v-1)*v/2 + (k - (v - 1))
}

func maxValue(n32, index32, maxSum32 int32) int32 {
	n, index, maxSum := int64(n32), int64(index32), int64(maxSum32)
	lo, hi := int64(1), maxSum
	for lo < hi {
		mid := (lo + hi + 1) / 2
		if mid+side(mid, index)+side(mid, n-1-index) <= maxSum {
			lo = mid
		} else {
			hi = mid - 1
		}
	}
	return int32(lo)
}

var seed int64 = 1802

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	cases := make([][3]int32, 4000)
	for c := range cases {
		n := 1 + nextRandom()%1000000
		index := nextRandom() % n
		hi := nextRandom()
		wide := hi*32768 + nextRandom()
		maxSum := n + wide%(1000000001-n)
		cases[c] = [3]int32{int32(n), int32(index), int32(maxSum)}
	}
	var check int64
	for call := int64(0); call < 1000000; call++ {
		c := cases[(check+call)%4000]
		check = (check*31 + int64(maxValue(c[0], c[1], c[2]))) % 1000000007
	}
	fmt.Printf("1000000 calls over 4000 cases: checksum %d\n", check)
}
