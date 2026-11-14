// LeetCode #1553: Minimum Number of Days to Eat N Oranges -- bench: the ★
// arm (halve or third after the single days, every answer kept in a fresh
// map per call) over 20000 piles of 1 to 2*10^9, drawn once, each asked 3
// times. Go mirror of
// oranges.kara.
package main

import "fmt"

func days(n int64, memo map[int64]int64) int64 {
	if n <= 1 {
		return n
	}
	if known, ok := memo[n]; ok {
		return known
	}
	halve := n%2 + days(n/2, memo)
	third := n%3 + days(n/3, memo)
	best := 1 + min(halve, third)
	memo[n] = best
	return best
}

func minDays(n int64) int64 {
	return days(n, map[int64]int64{})
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	seed := int64(1553)
	piles := []int64{}
	for i := 0; i < 20000; i++ {
		wide := (nextRandom(&seed)*32768+nextRandom(&seed))*32768 + nextRandom(&seed)
		piles = append(piles, wide%2000000000+1)
	}
	check, total := int64(0), int64(0)
	for pass := 0; pass < 3; pass++ {
		for _, n := range piles {
			d := minDays(n)
			total += d
			check = mix(check, d)
		}
	}
	fmt.Printf("3 passes over 20000 piles of up to 2000000000: %d days, checksum %d\n", total, check)
}
