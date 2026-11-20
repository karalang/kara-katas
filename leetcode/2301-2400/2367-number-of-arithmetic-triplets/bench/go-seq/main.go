// LeetCode #2367: Number of Arithmetic Triplets -- the bench, the ★ arm in
// Go: a map of the values, and each value x the start of a triplet when
// the map holds x + diff and x + 2 diff.
package main

import "fmt"

func arithmeticTriplets(nums []int64, diff int64) int64 {
	values := map[int64]struct{}{}
	for _, x := range nums {
		values[x] = struct{}{}
	}
	count := int64(0)
	for _, x := range nums {
		_, one := values[x+diff]
		_, two := values[x+2*diff]
		if one && two {
			count++
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// set s: each value from 0 to 200 kept with a chance of 1 + s % 8 in 8,
	// and at least the three values 0, 1 and 2
	seed := int64(2367)
	sets := make([][]int64, 0, 1000)
	for s := int64(0); s < 1000; s++ {
		nums := []int64{}
		for v := int64(0); v < 201; v++ {
			if v < 3 || nextRandom(&seed)%8 <= s%8 {
				nums = append(nums, v)
			}
		}
		sets = append(sets, nums)
	}
	check := int64(0)
	for p := int64(0); p < 50; p++ {
		for s := int64(0); s < 1000; s++ {
			diff := 1 + (s+p)%50
			check = (check*31 + arithmeticTriplets(sets[s], diff) + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 1000 sets of up to 201 values: checksum %d\n", check)
}
