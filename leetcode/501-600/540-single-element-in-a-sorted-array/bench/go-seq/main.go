// Benchmark for #540: Go mirror of the ★ arm (binary search over the
// pairs); see ../single_non_duplicate.kara.
package main

import "fmt"

func singleNonDuplicate(nums []int64) int64 {
	low, high := 0, len(nums)-1
	for low < high {
		mid := (low + high) / 2
		if mid%2 == 1 {
			mid--
		}
		if nums[mid] == nums[mid+1] {
			low = mid + 2
		} else {
			high = mid
		}
	}
	return nums[low]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 100 arrays of 0 to 49,999 pairs and the single element at a
	// random place, values rising by 1 or 2, built once. Then the answer
	// for each array is found 200,000 times.
	arrays := 100
	seed := int64(540)
	all := make([][]int64, arrays)
	elements := 0
	for t := 0; t < arrays; t++ {
		high := nextRandom(&seed)
		pairs := (high*32768 + nextRandom(&seed)) % 50000
		high = nextRandom(&seed)
		single := (high*32768 + nextRandom(&seed)) % (pairs + 1)
		nums := make([]int64, 0, 2*pairs+1)
		var v int64
		for i := int64(0); i < pairs+1; i++ {
			v += 1 + nextRandom(&seed)%2
			nums = append(nums, v)
			if i != single {
				nums = append(nums, v)
			}
		}
		elements += len(nums)
		all[t] = nums
	}
	var total, checksum int64
	for r := 0; r < 200000; r++ {
		for _, nums := range all {
			answer := singleNonDuplicate(nums)
			total += answer
			checksum = (checksum*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d arrays, %d elements, 200000 times each: total %d, checksum %d\n", arrays, elements, total, checksum)
}
