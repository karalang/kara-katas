// LeetCode #915: Partition Array into Disjoint Intervals -- bench: Go
// mirror of the largest on the left against the smallest on the right in
// partition_disjoint.kara.
package main

import "fmt"

func partitionDisjoint(nums []int64) int64 {
	n := len(nums)
	leastAfter := make([]int64, n)
	leastAfter[n-1] = nums[n-1]
	for i := n - 1; i > 0; i-- {
		leastAfter[i-1] = min(nums[i-1], leastAfter[i])
	}
	most := nums[0]
	for k := 1; k < n; k++ {
		if most <= leastAfter[k] {
			return int64(k)
		}
		most = max(most, nums[k])
	}
	return int64(n)
}

var seed int64 = 915

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func big() int64 {
	high := nextRandom()
	return (high*32768 + nextRandom()) % 1000001
}

func main() {
	rounds := 2000
	n := int64(100000)
	nums := make([]int64, 0, n)
	for i := int64(0); i < n; i++ {
		v := big() % 500000
		if i < n/2 {
			nums = append(nums, v)
		} else {
			nums = append(nums, 500000+v)
		}
	}
	total := int64(0)
	check := int64(0)
	for r := 0; r < rounds; r++ {
		i := big() % n
		old := nums[i]
		nums[i] = big()
		k := partitionDisjoint(nums)
		total += k
		check = (check*1000003 + k) % 1000000007
		nums[i] = old
	}
	fmt.Printf("%d rounds over %d values: left sides summing to %d, checksum %d\n", rounds, n, total, check)
}
