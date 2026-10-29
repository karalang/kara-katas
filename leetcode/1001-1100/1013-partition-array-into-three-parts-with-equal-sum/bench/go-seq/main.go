// LeetCode #1013: Partition Array Into Three Parts With Equal Sum -- bench
// Mirrors ../three_parts.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

func canThreePartsEqualSum(arr []int64) bool {
	var total int64
	for _, x := range arr {
		total += x
	}
	if total%3 != 0 {
		return false
	}
	target := total / 3
	var prefix int64
	cuts := 0
	for i := 0; i < len(arr)-1; i++ {
		prefix += arr[i]
		if cuts == 0 && prefix == target {
			cuts = 1
		} else if cuts == 1 && prefix == 2*target {
			return true
		}
	}
	return false
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := int64(50000)
	rounds := 10000
	seed := int64(1013)
	arr := make([]int64, 0, count)
	var total int64
	for i := int64(0); i < count; i++ {
		x := nextRandom(&seed)%7 - 2
		arr = append(arr, x)
		total += x
	}
	arr[count-1] -= total % 3
	yes := 0
	var check int64
	for r := 0; r < rounds; r++ {
		hi := nextRandom(&seed)
		lo := nextRandom(&seed)
		at := (hi*32768 + lo) % count
		arr[at] += 3 * (nextRandom(&seed)%3 - 1)
		answer := canThreePartsEqualSum(arr)
		if answer {
			yes++
		}
		var bit int64
		if answer {
			bit = 1
		}
		check = (check*2 + bit) % 1000000007
	}
	fmt.Printf("%d rounds over %d values: %d split, checksum %d\n", rounds, count, yes, check)
}
