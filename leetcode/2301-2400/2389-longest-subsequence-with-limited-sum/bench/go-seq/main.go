// LeetCode #2389: Longest Subsequence With Limited Sum -- the bench, the
// ★ arm in Go: the values sorted into prefix sums, each query answered by
// binary search.
package main

import (
	"fmt"
	"sort"
)

func answerQueries(nums, queries []int64) []int64 {
	prefix := append([]int64{}, nums...)
	sort.Slice(prefix, func(i, j int) bool { return prefix[i] < prefix[j] })
	for i := 1; i < len(prefix); i++ {
		prefix[i] += prefix[i-1]
	}
	answer := make([]int64, 0, len(queries))
	for _, q := range queries {
		low, high := 0, len(prefix)
		for low < high {
			mid := (low + high) / 2
			if prefix[mid] <= q {
				low = mid + 1
			} else {
				high = mid
			}
		}
		answer = append(answer, int64(low))
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	high := nextRandom(seed)
	return high*32768 + nextRandom(seed)
}

func main() {
	// 100 arrays of 1000 values up to 10^6, each with 1000 queries up to
	// 10^9; each pass answers them all and folds every answer
	seed := int64(2389)
	arrays := make([][]int64, 100)
	asks := make([][]int64, 100)
	for a := 0; a < 100; a++ {
		arrays[a] = make([]int64, 1000)
		for i := range arrays[a] {
			arrays[a][i] = 1 + wide(&seed)%1000000
		}
		asks[a] = make([]int64, 1000)
		for i := range asks[a] {
			asks[a][i] = 1 + wide(&seed)%1000000000
		}
	}
	check := int64(0)
	for p := int64(0); p < 200; p++ {
		for a := 0; a < 100; a++ {
			for _, v := range answerQueries(arrays[a], asks[a]) {
				check = (check*31 + v + p) % 1000000007
			}
		}
	}
	fmt.Printf("200 passes over 100 arrays of 1000 values and 1000 queries: checksum %d\n", check)
}
