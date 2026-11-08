// LeetCode #2031: Count Subarrays With More Ones Than Zeros -- the ★ arm in
// Go, the same algorithm and workload as subarrays.kara.
package main

import "fmt"

const MOD = 1000000007

func subarraysMoreOnes(nums []int64) int64 {
	n := int64(len(nums))
	seen := make([]int64, 2*n+1)
	prefix := n
	seen[prefix] = 1
	var below, total int64
	for _, x := range nums {
		if x == 1 {
			below += seen[prefix]
			prefix++
		} else {
			prefix--
			below -= seen[prefix]
		}
		total = (total + below) % MOD
		seen[prefix]++
	}
	return total
}

var seed int64 = 2031

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 20)
	for a := int64(0); a < 20; a++ {
		nums := make([]int64, 100000)
		for i := range nums {
			if nextRandom()%10 < a%9+1 {
				nums[i] = 1
			}
		}
		arrays[a] = nums
	}
	var calls, sum, check int64
	for round := int64(0); round < 100; round++ {
		for a := int64(0); a < 20; a++ {
			at := (round*997 + a*31) % 100000
			arrays[a][at] = 1 - arrays[a][at]
			answer := subarraysMoreOnes(arrays[a])
			calls++
			sum = (sum + answer) % MOD
			check = (check*31 + answer) % MOD
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
