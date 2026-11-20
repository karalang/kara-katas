// LeetCode #1231 bench: the ★ arm in Go, over the same 100 random bars and
// 20 passes as the Kāra bench.
package main

import "fmt"

func pieces(sweetness []int64, m int64) int64 {
	count, piece := int64(0), int64(0)
	for _, s := range sweetness {
		piece += s
		if piece >= m {
			count++
			piece = 0
		}
	}
	return count
}

func maximizeSweetness(sweetness []int64, k int64) int64 {
	total := int64(0)
	for _, s := range sweetness {
		total += s
	}
	lo, hi := int64(1), total/(k+1)
	for lo < hi {
		mid := (lo + hi + 1) / 2
		if pieces(sweetness, mid) >= k+1 {
			lo = mid
		} else {
			hi = mid - 1
		}
	}
	return lo
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1231)
	bars := make([][]int64, 100)
	cuts := make([]int64, 100)
	for b := 0; b < 100; b++ {
		bars[b] = make([]int64, 10000)
		for i := range bars[b] {
			bars[b][i] = nextRandom(&seed)%100000 + 1
		}
		cuts[b] = nextRandom(&seed) % 10000
	}
	check := int64(0)
	for pass := 0; pass < 20; pass++ {
		for b := 0; b < 100; b++ {
			check = (check*131 + maximizeSweetness(bars[b], cuts[b])) % 1000000007
		}
	}
	fmt.Printf("100 bars of 10^4 chunks, 20 passes: checksum %d\n", check)
}
