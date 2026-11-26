// LeetCode #1788: Maximize the Beauty of the Garden -- the bench in Go,
// mirroring maximum_beauty.kara: a prefix sum of the positives and each
// beauty's first position.
package main

import (
	"fmt"
	"math"
)

func maximumBeauty(flowers []int32) int32 {
	n := len(flowers)
	positive := make([]int64, n+1)
	for i := 0; i < n; i++ {
		p := int64(0)
		if flowers[i] > 0 {
			p = int64(flowers[i])
		}
		positive[i+1] = positive[i] + p
	}
	first := make(map[int32]int)
	best := int64(math.MinInt64)
	for j := 0; j < n; j++ {
		v := flowers[j]
		if i, ok := first[v]; ok {
			garden := 2*int64(v) + positive[j] - positive[i+1]
			if garden > best {
				best = garden
			}
		} else {
			first[v] = j
		}
	}
	return int32(best)
}

var seed int64 = 1788

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	gardens := make([][]int32, 0, 400)
	for g := 0; g < 400; g++ {
		flowers := make([]int32, 0, 2000)
		for i := 0; i < 2000; i++ {
			flowers = append(flowers, int32(nextRandom()%20001-10000))
		}
		flowers[1999] = flowers[0]
		gardens = append(gardens, flowers)
	}
	var check int64
	for call := int64(0); call < 10000; call++ {
		flowers := gardens[(check+call)%400]
		check = (check*31 + int64(maximumBeauty(flowers)) + 1000000000) % 1000000007
	}
	fmt.Printf("10000 calls over 400 gardens: checksum %d\n", check)
}
