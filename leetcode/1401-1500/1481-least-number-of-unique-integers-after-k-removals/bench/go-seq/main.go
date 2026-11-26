// LeetCode #1481: Least Number of Unique Integers after K Removals --
// bench, Go mirror of find_least_num_of_unique_ints.kara
package main

import (
	"fmt"
	"slices"
)

func findLeastNumOfUniqueInts(arr []int32, k int32) int32 {
	count := map[int32]int64{}
	for _, x := range arr {
		count[x]++
	}
	counts := make([]int64, 0, len(count))
	for _, c := range count {
		counts = append(counts, c)
	}
	slices.Sort(counts)
	left := int64(k)
	unique := int64(len(counts))
	for _, c := range counts {
		if c > left {
			break
		}
		left -= c
		unique--
	}
	return int32(unique)
}

var seed int64 = 1481

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arr := make([]int32, 100000)
	for i := range arr {
		arr[i] = int32(1 + nextRandom()%30000)
	}
	var check int64
	for pass := int64(0); pass < 100; pass++ {
		arr[check%100000] = int32(1 + (check/7)%30000)
		k := int32(check % 100000)
		check = (check*31 + int64(findLeastNumOfUniqueInts(arr, k)) + pass) % 1000000007
	}
	fmt.Printf("100 passes over 100000 values: checksum %d\n", check)
}
