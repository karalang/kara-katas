// LeetCode #2070: Most Beautiful Item for Each Query -- Go mirror of the ★
// arm's benchmark (beauty.kara): 20 shops of 100000 items and 100000
// queries each, prices, beauties and queries up to 10^9.
package main

import (
	"fmt"
	"sort"
)

func maximumBeauty(items [][]int64, queries []int64) []int64 {
	s := make([][]int64, len(items))
	copy(s, items)
	sort.SliceStable(s, func(i, j int) bool { return s[i][0] < s[j][0] })
	best := make([]int64, 0, len(s))
	var most int64
	for _, item := range s {
		most = max(most, item[1])
		best = append(best, most)
	}
	out := make([]int64, len(queries))
	for k, q := range queries {
		end := sort.Search(len(s), func(i int) bool { return s[i][0] > q })
		if end > 0 {
			out[k] = best[end-1]
		}
	}
	return out
}

var seed int64 = 2070

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func upTo(top int64) int64 {
	hi := nextRandom()
	return (hi*32768+nextRandom())%top + 1
}

func main() {
	var sum, check int64
	for s := 0; s < 20; s++ {
		items := make([][]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			p := upTo(1000000000)
			items = append(items, []int64{p, upTo(1000000000)})
		}
		queries := make([]int64, 100000)
		for i := range queries {
			queries[i] = upTo(1000000000)
		}
		for _, a := range maximumBeauty(items, queries) {
			sum += a
			check = (check*31 + a) % 1000000007
		}
	}
	fmt.Printf("20 shops: sum %d, checksum %d\n", sum, check)
}
