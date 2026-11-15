// benchmark's Go mirror of minimal.kara (LeetCode #2195, the ★ arm): the
// gaps walked, each a series.
package main

import (
	"fmt"
	"sort"
)

func runSum(from, to int64) int64 {
	return (from + to) * (to - from + 1) / 2
}

func minimalKSum(nums []int64, k int64) int64 {
	sorted := append([]int64(nil), nums...)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i] < sorted[j] })
	wanted, sum, last := k, int64(0), int64(0)
	for _, x := range sorted {
		if x > last+1 && wanted > 0 {
			take := wanted
			if x-last-1 < wanted {
				take = x - last - 1
			}
			sum += runSum(last+1, last+take)
			wanted -= take
		}
		if x > last {
			last = x
		}
	}
	if wanted > 0 {
		sum += runSum(last+1, last+wanted)
	}
	return sum
}

var seed int64 = 2195

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	nums := []int64{}
	for i := 0; i < 100000; i++ {
		a := nextRandom()
		b := nextRandom()
		nums = append(nums, (a*32768+b)%1000000000+1)
	}
	var check int64
	for i := int64(0); i < 300; i++ {
		k := 100000000 - i*1000
		check = (check*31 + minimalKSum(nums, k)%1000000007) % 1000000007
	}
	fmt.Printf("300 solves over %d numbers: checksum %d\n", len(nums), check)
}
