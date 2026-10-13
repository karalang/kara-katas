// Benchmark for #532: Go mirror of the ★ arm (count each number); see
// ../find_pairs.kara.
package main

import "fmt"

func findPairs(nums []int64, k int64) int64 {
	counts := map[int64]int64{}
	for _, x := range nums {
		counts[x]++
	}
	var pairs int64
	for v, c := range counts {
		if k == 0 {
			if c >= 2 {
				pairs++
			}
		} else if _, ok := counts[v+k]; ok {
			pairs++
		}
	}
	return pairs
}

func main() {
	// 20 arrays of 10,000 numbers made once, the a-th drawn from
	// -1,000(a + 1) to 1,000(a + 1); then each array is answered for 200
	// values of k from 0 to 19.
	seed := int64(532)
	var arrays [][]int64
	for a := int64(0); a < 20; a++ {
		half := 1000 * (a + 1)
		nums := make([]int64, 0, 10000)
		for i := 0; i < 10000; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			nums = append(nums, seed/65536%(2*half+1)-half)
		}
		arrays = append(arrays, nums)
	}
	var total, checksum int64
	for round := 0; round < 200; round++ {
		for a := range arrays {
			seed = (seed*1103515245 + 12345) % 2147483648
			answer := findPairs(arrays[a], seed/65536%20)
			total += answer
			checksum = (checksum*31 + answer) % 1000000007
		}
	}
	fmt.Printf("20 arrays of 10000, 200 values of k each: total %d, checksum %d\n", total, checksum)
}
