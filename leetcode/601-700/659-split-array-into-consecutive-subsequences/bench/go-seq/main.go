// Benchmark for #659: the greedy, as the Kara ★ arm.
package main

import (
	"fmt"
	"sort"
)

func isPossible(nums []int64) bool {
	left := map[int64]int64{}
	for _, x := range nums {
		left[x]++
	}
	ends := map[int64]int64{}
	for _, x := range nums {
		if left[x] == 0 {
			continue
		}
		left[x]--
		if ends[x-1] > 0 {
			ends[x-1]--
			ends[x]++
		} else if left[x+1] > 0 && left[x+2] > 0 {
			left[x+1]--
			left[x+2]--
			ends[x+2]++
		} else {
			return false
		}
	}
	return true
}

var seed int64 = 659

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	inputs, rounds := 8, 40
	arrays := make([][]int64, inputs)
	for k := 0; k < inputs; k++ {
		nums := []int64{}
		for r := 0; r < 25000; r++ {
			start := nextRandom() % 20001
			length := 3 + nextRandom()%3
			for v := start; v < start+length; v++ {
				nums = append(nums, v)
			}
		}
		if k%2 == 1 {
			nums = append(nums, 30000)
		}
		sort.Slice(nums, func(i, j int) bool { return nums[i] < nums[j] })
		arrays[k] = nums
	}
	var yes, checksum int64
	for r := 0; r < rounds; r++ {
		pick := (r * 3) % inputs
		ok := isPossible(arrays[pick])
		bit := int64(0)
		if ok {
			yes++
			bit = 1
		}
		checksum = (checksum*31 + int64(len(arrays[pick]))*2 + bit) % 1000000007
	}
	fmt.Printf("%d arrays, %d rounds: %d split, checksum %d\n", inputs, rounds, yes, checksum)
}
