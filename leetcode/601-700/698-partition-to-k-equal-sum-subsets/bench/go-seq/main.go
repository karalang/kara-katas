// LeetCode #698: Partition to K Equal Sum Subsets -- bench program, Go mirror of the bottom-up arm.
package main

import "fmt"

var seed int64 = 698

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func canPartitionKSubsets(nums []int64, k int64) bool {
	n := len(nums)
	var total int64
	for _, x := range nums {
		total += x
	}
	if total%k != 0 {
		return false
	}
	target := total / k
	size := 1 << n
	fill := make([]int64, size)
	for m := range fill {
		fill[m] = -1
	}
	fill[0] = 0
	for mask := 0; mask < size; mask++ {
		if fill[mask] < 0 {
			continue
		}
		for i := 0; i < n; i++ {
			next := mask | (1 << i)
			if next != mask && fill[next] < 0 && fill[mask]+nums[i] <= target {
				fill[next] = (fill[mask] + nums[i]) % target
			}
		}
	}
	return fill[size-1] == 0
}

func main() {
	problems := [][]int64{}
	ks := []int64{}
	for p := int64(0); p < 100; p++ {
		k := int64(1) << (p % 5)
		g := 16 / k
		target := 16 + nextRandom()%9985
		nums := []int64{}
		for b := int64(0); b < k; b++ {
			left := target
			for q := int64(0); q < g-1; q++ {
				part := 1 + nextRandom()%(target/g)
				nums = append(nums, part)
				left -= part
			}
			nums = append(nums, left)
		}
		for i := int64(0); i < 16; i++ {
			j := i + nextRandom()%(16-i)
			nums[i], nums[j] = nums[j], nums[i]
		}
		if p%2 == 1 {
			i := nextRandom() % 16
			j := (i + 1 + nextRandom()%15) % 16
			most := min(nums[j]-1, 10000-nums[i])
			if most >= 1 {
				d := 1 + nextRandom()%most
				nums[i] += d
				nums[j] -= d
			}
		}
		problems = append(problems, nums)
		ks = append(ks, k)
	}
	rounds := 2
	var yes, checksum int64
	for r := 0; r < rounds; r++ {
		for p := range problems {
			ok := canPartitionKSubsets(problems[p], ks[p])
			bit := int64(0)
			if ok {
				yes++
				bit = 1
			}
			checksum = (checksum*3 + bit + int64(p)) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 100 problems of 16 values: %d answers yes, checksum %d\n", rounds, yes, checksum)
}
