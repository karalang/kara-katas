// LeetCode #2344: Minimum Deletions to Make Array Divisible -- the bench,
// the ★ arm in Go: the gcd of numsDivide, then nums sorted and scanned for
// the first value that divides it.
package main

import (
	"fmt"
	"slices"
)

func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func minOperations(nums, numsDivide []int64) int64 {
	g := int64(0)
	for _, x := range numsDivide {
		g = gcd(g, x)
	}
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	for i, x := range sorted {
		if g%x == 0 {
			return int64(i)
		}
	}
	return -1
}

func scrambled(index int64) int64 {
	return index * 2654435761 % 2147483647
}

func main() {
	nums := make([][]int64, 10)
	divide := make([][]int64, 10)
	for a := int64(0); a < 10; a++ {
		nums[a] = make([]int64, 100000)
		for i := int64(0); i < 100000; i++ {
			nums[a][i] = scrambled(a*100000+i)%1000000 + 1
		}
		base := nums[a][a*7919%100000]
		divide[a] = make([]int64, 10000)
		for i := int64(0); i < 10000; i++ {
			divide[a][i] = base * (scrambled(a*10000+i+7)%1000 + 1)
		}
	}
	check := int64(0)
	for p := int64(0); p < 20; p++ {
		for a := 0; a < 10; a++ {
			check = (check*31 + minOperations(nums[a], divide[a]) + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 cases of 10^5 values against 10^4: checksum %d\n", check)
}
