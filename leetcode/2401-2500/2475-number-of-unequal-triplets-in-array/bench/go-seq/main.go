// LeetCode #2475: Number of Unequal Triplets in Array -- the bench, the ★
// arm in Go: a `map` counts the values, and each value of count `c` is
// the middle of `left * c * right` triplets.
package main

import "fmt"

func unequalTriplets(nums []int64) int64 {
	counts := map[int64]int64{}
	for _, v := range nums {
		counts[v]++
	}
	n := int64(len(nums))
	var left, total int64
	for _, c := range counts {
		total += left * c * (n - left - c)
		left += c
	}
	return total
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2475

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 2000 lists of 100 values from 1 to 50 built once; then 600 passes,
	// each setting one value of every list from the checksum so far, then
	// answering it, folding the count plus the pass into the checksum
	lists := make([][]int64, 2000)
	for a := range lists {
		lists[a] = make([]int64, 100)
		for i := range lists[a] {
			lists[a][i] = 1 + nextRandom()%50
		}
	}
	var check int64
	for p := int64(0); p < 600; p++ {
		for a := range lists {
			lists[a][(check+int64(a))%100] = 1 + check%50
			check = (check*31 + unequalTriplets(lists[a]) + p) % 1000000007
		}
	}
	fmt.Printf("600 passes over 2000 lists of 100: checksum %d\n", check)
}
