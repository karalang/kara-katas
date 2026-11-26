package main

import "fmt"

func maxScore(cardPoints []int32, k int32) int32 {
	n := len(cardPoints)
	kk := int(k)
	var sum int32
	for _, c := range cardPoints[:kk] {
		sum += c
	}
	best := sum
	for i := 0; i < kk; i++ {
		sum += cardPoints[n-1-i] - cardPoints[kk-1-i]
		if sum > best {
			best = sum
		}
	}
	return best
}

func main() {
	var seed int64 = 1423
	pool := make([]int32, 1000000)
	for i := range pool {
		seed = (seed*1103515245 + 12345) % 2147483648
		pool[i] = int32(1 + seed/65536%10000)
	}
	var check int64
	for w := 0; w < 50000; w++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		start := seed / 65536 % 900001
		seed = (seed*1103515245 + 12345) % 2147483648
		k := int32(1 + seed/65536%100000)
		check = (check*131 + int64(maxScore(pool[start:start+100000], k))) % 1000000007
	}
	fmt.Printf("5 * 10^4 windows of 10^5 cards: checksum %d\n", check)
}
