// LeetCode #1601: Maximum Number of Achievable Transfer Requests
// -- the bench in Go, mirroring transfers.kara: every subset of the
// requests as a bit mask, a subset no larger than the best skipped, a
// fresh slice of net changes per mask, on 100 problems of 16 requests
// among 6 buildings, all drawn first.
package main

import (
	"fmt"
	"math/bits"
)

func maximumRequests(n int32, requests [][]int32) int32 {
	r := len(requests)
	var best int32
	for mask := int64(0); mask < 1<<r; mask++ {
		size := int32(bits.OnesCount64(uint64(mask)))
		if size <= best {
			continue
		}
		net := make([]int64, n)
		for i := 0; i < r; i++ {
			if mask>>i&1 == 1 {
				net[requests[i][0]]--
				net[requests[i][1]]++
			}
		}
		ok := true
		for _, d := range net {
			if d != 0 {
				ok = false
			}
		}
		if ok {
			best = size
		}
	}
	return best
}

var seed int64 = 1601

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	problems := make([][][]int32, 100)
	for p := range problems {
		problems[p] = make([][]int32, 16)
		for i := range problems[p] {
			a := int32(nextRandom() % 6)
			b := int32(nextRandom() % 6)
			problems[p][i] = []int32{a, b}
		}
	}
	var check, total int64
	for _, requests := range problems {
		answer := maximumRequests(6, requests)
		total += int64(answer)
		check = (check*31 + int64(answer) + 1) % 1000000007
	}
	fmt.Printf("100 problems of 16 requests among 6 buildings: total %d, checksum %d\n", total, check)
}
