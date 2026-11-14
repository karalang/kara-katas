// LeetCode #1569: Number of Ways to Reorder Array to Get Same BST -- bench:
// the ★ arm (the interleavings, by recursion and Pascal's triangle) over 20
// permutations of 1 to 1000, built once; 15 passes, each first swapping two
// values of every permutation.
package main

import "fmt"

const MOD = 1000000007

func ways(nums []int64, choose [][]int64) int64 {
	if len(nums) <= 2 {
		return 1
	}
	root := nums[0]
	left := make([]int64, 0)
	right := make([]int64, 0)
	for _, x := range nums[1:] {
		if x < root {
			left = append(left, x)
		}
	}
	for _, x := range nums[1:] {
		if x > root {
			right = append(right, x)
		}
	}
	return choose[len(nums)-1][len(left)] * ways(left, choose) % MOD * ways(right, choose) % MOD
}

func numOfWays(nums []int64) int64 {
	n := len(nums)
	choose := make([][]int64, n+1)
	for i := range choose {
		choose[i] = make([]int64, n+1)
	}
	for i := 0; i <= n; i++ {
		choose[i][0] = 1
		for j := 1; j <= i; j++ {
			choose[i][j] = (choose[i-1][j-1] + choose[i-1][j]) % MOD
		}
	}
	return (ways(nums, choose) - 1 + MOD) % MOD
}

var seed int64 = 1569

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 1000
	perms := make([][]int64, 0, 20)
	for p := 0; p < 20; p++ {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = int64(i + 1)
		}
		for i := int64(n - 1); i >= 1; i-- {
			a := nextRandom()
			j := (a*32768 + nextRandom()) % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		perms = append(perms, nums)
	}
	var check, total int64
	for pass := int64(0); pass < 15; pass++ {
		for p := range perms {
			i := (pass*7919 + int64(p)*104729) % n
			j := (pass*104729 + int64(p)*7919 + 1) % n
			perms[p][i], perms[p][j] = perms[p][j], perms[p][i]
			w := numOfWays(perms[p])
			total = (total + w) % MOD
			check = mix(check, w)
		}
	}
	fmt.Printf("15 passes over 20 permutations of 1000 values: ways sum %d, checksum %d\n", total, check)
}
