// LeetCode #1406 bench, Go: the same lead from the last stone back,
// workload and checksum as stone_game_iii.kara.
package main

import (
	"fmt"
	"math"
)

func stoneGameIII(stoneValue []int32) string {
	n := len(stoneValue)
	best := make([]int32, n+1)
	for i := n - 1; i >= 0; i-- {
		var taken int32
		best[i] = math.MinInt32
		for k := 1; k <= 3; k++ {
			if i+k > n {
				break
			}
			taken += stoneValue[i+k-1]
			if lead := taken - best[i+k]; lead > best[i] {
				best[i] = lead
			}
		}
	}
	if best[0] > 0 {
		return "Alice"
	} else if best[0] < 0 {
		return "Bob"
	}
	return "Tie"
}

func main() {
	var seed int64 = 1406
	pool := make([]int32, 0, 100000)
	for i := 0; i < 100000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		pool = append(pool, int32(seed/65536%41-20))
	}
	var check int64
	for r := int64(0); r < 1000; r++ {
		at := (check + r*7919) % 50001
		row := append([]int32(nil), pool[at:at+50000]...)
		var code int64 = 3
		switch stoneGameIII(row) {
		case "Alice":
			code = 1
		case "Bob":
			code = 2
		}
		check = (check*131 + code) % 1000000007
	}
	fmt.Printf("1000 rows of 5 * 10^4 stones: checksum %d\n", check)
}
