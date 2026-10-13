// Benchmark for #464: mirror of can_i_win.kara (the ★ arm: search with a
// memo keyed by the bitmask of numbers used) on the same workload. The
// memo is a Go map.
package main

import "fmt"

func winsFrom(used, left, m int64, memo map[int64]bool) bool {
	if known, ok := memo[used]; ok {
		return known
	}
	result := false
	for n := int64(1); n < m+1; n++ {
		bit := int64(1) << (n - 1)
		if used&bit == 0 && (n >= left || !winsFrom(used|bit, left-n, m, memo)) {
			result = true
			break
		}
	}
	memo[used] = result
	return result
}

func canIWin(maxChoosable, desiredTotal int64) bool {
	if desiredTotal <= 0 {
		return true
	}
	if maxChoosable*(maxChoosable+1)/2 < desiredTotal {
		return false
	}
	return winsFrom(0, desiredTotal, maxChoosable, map[int64]bool{})
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const games = 10
	seed := int64(464)
	won := 0
	checksum := int64(0)
	for game := int64(0); game < games; game++ {
		total := 100 + nextRandom(&seed)%111
		if canIWin(20, total) {
			won++
			checksum = (checksum*31 + game + 1) % 1000000007
		}
	}
	fmt.Printf("%d games of 1 to 20: the first player wins %d, checksum %d\n", games, won, checksum)
}
