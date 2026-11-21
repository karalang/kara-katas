// LeetCode #2498: Frog Jump II -- Go mirror of the benchmark (frog.kara):
// the same rows, passes and checksum.
package main

import "fmt"

var seed int64 = 2498

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func maxJump(stones []int64) int64 {
	cost := stones[1] - stones[0]
	for i := 2; i < len(stones); i++ {
		if stones[i]-stones[i-2] > cost {
			cost = stones[i] - stones[i-2]
		}
	}
	return cost
}

func main() {
	const n int64 = 100000
	const passes int64 = 55
	rows := make([][]int64, 20)
	for r := range rows {
		stones := make([]int64, n)
		for i := int64(1); i < n; i++ {
			stones[i] = stones[i-1] + nextRandom()%10000 + 1
		}
		rows[r] = stones
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for r := 0; r < 20; r++ {
			stones := rows[r]
			at := check%(n-2) + 1
			was := stones[at]
			room := stones[at+1] - stones[at-1] - 1
			if room > 0 {
				stones[at] = stones[at-1] + 1 + (check+p)%room
			}
			check = (check*31 + maxJump(stones) + p) % 1000000007
			stones[at] = was
		}
	}
	fmt.Printf("%d passes over 20 rows of 10^5: checksum %d\n", passes, check)
}
