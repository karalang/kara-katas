// Benchmark: LeetCode #996 Number of Squareful Arrays -- the ★ arm,
// backtracking over the sorted values, on random arrays of 12 values,
// LeetCode's largest. Mirrors num_squareful_perms.kara, .c, .rs and .py.
package main

import (
	"fmt"
	"math"
	"sort"
)

func isSquare(s int64) bool {
	r := int64(math.Sqrt(float64(s)))
	for r*r > s {
		r--
	}
	for (r+1)*(r+1) <= s {
		r++
	}
	return r*r == s
}

func place(a []int64, used []bool, depth int, last int64) int64 {
	n := len(a)
	if depth == n {
		return 1
	}
	var count int64
	for i := 0; i < n; i++ {
		if used[i] {
			continue
		}
		if i > 0 && a[i] == a[i-1] && !used[i-1] {
			continue
		}
		if depth > 0 && !isSquare(last+a[i]) {
			continue
		}
		used[i] = true
		count += place(a, used, depth+1, a[i])
		used[i] = false
	}
	return count
}

func numSquarefulPerms(nums []int64) int64 {
	a := append([]int64(nil), nums...)
	sort.Slice(a, func(i, j int) bool { return a[i] < a[j] })
	used := make([]bool, len(a))
	return place(a, used, 0, 0)
}

var seed int64 = 996

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// 12 values below 50, each making a square with the one before
func randomWalk() []int64 {
	nums := []int64{nextRandom() % 50}
	for k := 1; k < 12; k++ {
		v := nums[len(nums)-1]
		var options []int64
		for r := int64(0); r*r < v+50; r++ {
			if r*r >= v {
				options = append(options, r*r-v)
			}
		}
		nums = append(nums, options[nextRandom()%int64(len(options))])
	}
	return nums
}

func main() {
	rounds := 300
	arrays := make([][]int64, 20)
	for i := range arrays {
		arrays[i] = randomWalk()
	}
	var found, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			got := numSquarefulPerms(arrays[(r+i)%20])
			found += got
			check = (check*31 + got + 1) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 arrays of 12 values: %d squareful permutations, checksum %d\n", rounds, found, check)
}
