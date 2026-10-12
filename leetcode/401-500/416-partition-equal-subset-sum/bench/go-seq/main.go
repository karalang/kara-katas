// LeetCode #416: Partition Equal Subset Sum -- Go mirror of
// can_partition.kara (sums up to half).
package main

import "fmt"

func canPartition(nums []int64) bool {
	var total int64
	for _, x := range nums {
		total += x
	}
	if total%2 != 0 {
		return false
	}
	half := total / 2
	reach := make([]bool, half+1)
	reach[0] = true
	for _, x := range nums {
		s := half
		for s >= x {
			if reach[s-x] {
				reach[s] = true
			}
			s--
		}
	}
	return reach[half]
}

var seed int64 = 416

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 200
	var rounds int64 = 2000
	nums := make([]int64, 0, n)
	var total int64
	for k := int64(0); k < n; k++ {
		x := 1 + step()%100
		nums = append(nums, x)
		total += x
	}
	if total%2 != 0 {
		if nums[0] < 100 {
			nums[0]++
		} else {
			nums[0]--
		}
	}
	var yes, checksum int64
	for r := int64(0); r < rounds; r++ {
		i := step() % n
		j := step() % n
		if nums[i] < 100 && nums[j] > 1 {
			nums[i]++
			nums[j]--
		}
		answer := canPartition(nums)
		var bonus int64
		if answer {
			yes++
			bonus = r
		}
		checksum = (checksum*31 + nums[i] + bonus) % 1000000007
	}
	fmt.Printf("%d rounds on %d numbers: %d can be split, checksum %d\n", rounds, n, yes, checksum)
}
