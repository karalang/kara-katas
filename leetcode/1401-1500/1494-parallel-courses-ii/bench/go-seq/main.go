// LeetCode #1494: Parallel Courses II -- the bench in Go, mirroring
// min_number_of_semesters.kara: a DP over the sets of courses taken.
package main

import (
	"fmt"
	"math"
	"math/bits"
)

func minNumberOfSemesters(n int, relations [][]int32, k int32) int32 {
	pre := make([]int64, n)
	for _, r := range relations {
		pre[r[1]-1] |= 1 << (r[0] - 1)
	}
	full := int64(1)<<n - 1
	semesters := make([]int32, full+1)
	for i := range semesters {
		semesters[i] = math.MaxInt32
	}
	semesters[0] = 0
	for taken := int64(0); taken < full; taken++ {
		if semesters[taken] == math.MaxInt32 {
			continue
		}
		var open int64
		for i := 0; i < n; i++ {
			if taken&(1<<i) == 0 && pre[i]&taken == pre[i] {
				open |= 1 << i
			}
		}
		next := semesters[taken] + 1
		if int32(bits.OnesCount64(uint64(open))) <= k {
			if next < semesters[taken|open] {
				semesters[taken|open] = next
			}
			continue
		}
		for pick := open; pick > 0; pick = (pick - 1) & open {
			if int32(bits.OnesCount64(uint64(pick))) == k && next < semesters[taken|pick] {
				semesters[taken|pick] = next
			}
		}
	}
	return semesters[full]
}

func main() {
	var check int64
	for call := int64(0); call < 300; call++ {
		seed := check + call
		next := func() int64 {
			seed = (seed*1103515245 + 12345) % 2147483648
			return seed / 65536
		}
		dense := next() % 8
		k := 2 + next()%4
		var relations [][]int32
		for a := int32(1); a <= 15; a++ {
			for b := a + 1; b <= 15; b++ {
				if next()%100 < dense {
					relations = append(relations, []int32{a, b})
				}
			}
		}
		check = (check*31 + int64(minNumberOfSemesters(15, relations, int32(k)))) % 1000000007
	}
	fmt.Printf("300 calls on 15 courses: checksum %d\n", check)
}
