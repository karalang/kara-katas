// LeetCode #2364: Count Number of Bad Pairs -- the bench, the ★ arm in Go:
// each place's key nums[j] - j counted in a map as the places go by, the
// places before j with the same key its good pairs, and the bad pairs all
// n (n - 1) / 2 less the good ones.
package main

import "fmt"

func countBadPairs(nums []int64) int64 {
	n := int64(len(nums))
	seen := map[int64]int64{}
	good := int64(0)
	for j, x := range nums {
		key := x - int64(j)
		before := seen[key]
		good += before
		seen[key] = before + 1
	}
	return n*(n-1)/2 - good
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wideRandom(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func main() {
	// array a: 10^5 values, each the place plus one of 4^a offsets (at
	// most 10^5) below 999 * 10^6, so the keys run from one to tens of
	// thousands
	seed := int64(2364)
	arrays := make([][]int64, 0, 10)
	for a := 0; a < 10; a++ {
		kinds := int64(1) << (2 * a)
		if kinds > 100000 {
			kinds = 100000
		}
		offsets := make([]int64, kinds)
		for k := range offsets {
			offsets[k] = wideRandom(&seed) % 999000000
		}
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = 1 + int64(i) + offsets[wideRandom(&seed)%kinds]
		}
		arrays = append(arrays, nums)
	}
	check := int64(0)
	for p := int64(0); p < 20; p++ {
		for _, nums := range arrays {
			check = (check*31 + countBadPairs(nums)%1000000007 + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
