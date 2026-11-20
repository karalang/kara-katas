// LeetCode #1711: Count Good Meals -- the Go mirror of the bench
// (meals.kara): one pass, each dish paired with the earlier dishes that
// make each of the 22 powers with it, counted in a map, on 10 random
// lists of 100000 dishes, each answered 3 times.
package main

import "fmt"

func countPairs(deliciousness []int32) int32 {
	seen := map[int32]int64{}
	var pairs int64
	for _, d := range deliciousness {
		for b := 0; b < 22; b++ {
			pairs += seen[int32(1)<<b-d]
		}
		seen[d]++
	}
	return int32(pairs % 1000000007)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 10
	var rounds int64 = 3
	n := 100000
	var top int64 = 1 << 20
	var seed int64 = 1711
	lists := make([][]int32, count)
	for p := 0; p < count; p++ {
		lists[p] = make([]int32, n)
		for i := 0; i < n; i++ {
			a := nextRandom(&seed)
			lists[p][i] = int32((a*32768 + nextRandom(&seed)) % (top + 1))
		}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, deliciousness := range lists {
			answer := int64(countPairs(deliciousness))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d lists of %d dishes, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
