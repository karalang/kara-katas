// LeetCode #2274: Maximum Consecutive Floors Without Special Floors --
// the bench, the ★ arm. The floors are copied and sorted by `sort.Slice`.
package main

import (
	"fmt"
	"sort"
)

func maxConsecutive(bottom, top int64, special []int64) int64 {
	floors := append([]int64(nil), special...)
	sort.Slice(floors, func(a, b int) bool { return floors[a] < floors[b] })
	best := floors[0] - bottom
	if top-floors[len(floors)-1] > best {
		best = top - floors[len(floors)-1]
	}
	for i := 1; i < len(floors); i++ {
		if run := floors[i] - floors[i-1] - 1; run > best {
			best = run
		}
	}
	return best
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2274

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 50; t++ {
		special := make([]int64, 0)
		f := 1 + nextRandom()%20000
		for f <= 1000000000 && len(special) < 100000 {
			special = append(special, f)
			f += 1 + nextRandom()%20000
		}
		for j := len(special) - 1; j >= 1; j-- {
			r := nextRandom() % int64(j+1)
			special[j], special[r] = special[r], special[j]
		}
		check = (check*31 + maxConsecutive(1, 1000000000, special)) % 1000000007
	}
	fmt.Printf("50 buildings of 10^5: checksum %d\n", check)
}
