// LeetCode #1523: Count Odd Numbers in an Interval Range -- bench: the ★
// arm over 2000000 random intervals within 0 to 10^9, built once and
// answered 100 times, each pass summed.
package main

import "fmt"

func countOdds(low, high int64) int64 {
	return (high+1)/2 - low/2
}

var seed int64 = 1523

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

func main() {
	const count = 2000000
	lows := make([]int64, 0, count)
	highs := make([]int64, 0, count)
	for i := 0; i < count; i++ {
		hi := nextRandom()
		a := (hi*32768 + nextRandom()) % 1000000001
		hi = nextRandom()
		b := (hi*32768 + nextRandom()) % 1000000001
		if a < b {
			lows = append(lows, a)
			highs = append(highs, b)
		} else {
			lows = append(lows, b)
			highs = append(highs, a)
		}
	}
	var check int64
	for pass := 0; pass < 100; pass++ {
		var total int64
		for i := 0; i < count; i++ {
			total += countOdds(lows[i], highs[i])
		}
		check = mix(check, total%1000000007)
	}
	fmt.Printf("100 passes over 2000000 intervals within 0 to 10^9: checksum %d\n", check)
}
