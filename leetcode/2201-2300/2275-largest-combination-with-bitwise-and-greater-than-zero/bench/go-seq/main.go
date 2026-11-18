// LeetCode #2275: Largest Combination With Bitwise AND Greater Than Zero
// -- the bench, the ★ arm.
package main

import "fmt"

func largestCombination(candidates []int64) int64 {
	var best int64
	for bit := 0; bit < 24; bit++ {
		var count int64
		for _, x := range candidates {
			if (x>>bit)&1 == 1 {
				count++
			}
		}
		if count > best {
			best = count
		}
	}
	return best
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2275

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 100; t++ {
		candidates := make([]int64, 0)
		for i := 0; i < 100000; i++ {
			high := nextRandom()
			candidates = append(candidates, (high*32768+nextRandom())%10000000+1)
		}
		check = (check*31 + largestCombination(candidates)) % 1000000007
	}
	fmt.Printf("100 lists of 10^5: checksum %d\n", check)
}
