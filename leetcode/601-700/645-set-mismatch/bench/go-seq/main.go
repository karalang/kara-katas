// Benchmark for #645: mirror of set_mismatch.kara (the ★ arm: counting
// each value) on the same workload.
package main

import "fmt"

func findErrorNums(nums []int64) (int64, int64) {
	n := int64(len(nums))
	seen := make([]int64, n+1)
	for _, x := range nums {
		seen[x]++
	}
	var twice, missing int64
	for v := int64(1); v < n+1; v++ {
		if seen[v] == 2 {
			twice = v
		} else if seen[v] == 0 {
			missing = v
		}
	}
	return twice, missing
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func mismatched(n int64, seed *int64) []int64 {
	nums := make([]int64, n)
	for v := int64(1); v < n+1; v++ {
		nums[v-1] = v
	}
	for i := int64(0); i < n-1; i++ {
		j := i + nextRandom(seed)%(n-i)
		nums[i], nums[j] = nums[j], nums[i]
	}
	from := nextRandom(seed) % n
	to := nextRandom(seed) % (n - 1)
	if to >= from {
		to++
	}
	nums[to] = nums[from]
	return nums
}

func main() {
	var seed int64 = 645
	arrays := make([][]int64, 0, 20)
	for a := 0; a < 20; a++ {
		arrays = append(arrays, mismatched(100000, &seed))
	}
	var rounds int64 = 2000
	var twiceSum, missingSum int64
	for r := int64(0); r < rounds; r++ {
		t, m := findErrorNums(arrays[r%20])
		twiceSum += t
		missingSum += m
	}
	fmt.Printf("%d rounds over 20 arrays of 100000 values: copies add to %d, missing values to %d\n", rounds, twiceSum, missingSum)
}
