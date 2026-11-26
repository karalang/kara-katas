// LeetCode #1482: Minimum Number of Days to Make m Bouquets -- bench, the
// Go twin of min_days.kara.
package main

import "fmt"

func bouquets(bloomDay []int32, k int32, day int32) int64 {
	var made int64
	var run int32
	for _, d := range bloomDay {
		if d <= day {
			run++
			if run == k {
				made++
				run = 0
			}
		} else {
			run = 0
		}
	}
	return made
}

func minDays(bloomDay []int32, m int32, k int32) int32 {
	if int64(m)*int64(k) > int64(len(bloomDay)) {
		return -1
	}
	lo, hi := bloomDay[0], bloomDay[0]
	for _, d := range bloomDay[1:] {
		if d < lo {
			lo = d
		}
		if d > hi {
			hi = d
		}
	}
	for lo < hi {
		mid := lo + (hi-lo)/2
		if bouquets(bloomDay, k, mid) >= int64(m) {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1482)
	bloom := make([]int32, 100000)
	for i := range bloom {
		hi := nextRandom(&seed)
		lo := nextRandom(&seed)
		bloom[i] = int32(1 + (hi*32768+lo)%1000000000)
	}
	var check int64
	for pass := int64(0); pass < 150; pass++ {
		bloom[check%100000] = int32(1 + (check*7)%1000000000)
		k := 1 + check%10
		m := 1 + (check/10)%(100000/k+100)
		check = (check*31 + int64(minDays(bloom, int32(m), int32(k))) + 1 + pass) % 1000000007
	}
	fmt.Printf("150 passes over 100000 flowers: checksum %d\n", check)
}
