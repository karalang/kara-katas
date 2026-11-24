// LeetCode #1340 bench in Go: the ★ arm (memoized depth-first search, each
// direction walked outward up to d steps and stopped at the first value
// not lower) on the same 20 arrays of 1000 values and 20 passes.
package main

import "fmt"

func mostFrom(arr []int, d, i int, memo []int) int {
	if memo[i] > 0 {
		return memo[i]
	}
	best := 1
	for _, step := range []int{-1, 1} {
		j := i + step
		for j >= 0 && j < len(arr) && abs(j-i) <= d && arr[j] < arr[i] {
			best = max(best, 1+mostFrom(arr, d, j, memo))
			j += step
		}
	}
	memo[i] = best
	return best
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func maxJumps(arr []int, d int) int {
	memo := make([]int, len(arr))
	best := 0
	for i := range arr {
		best = max(best, mostFrom(arr, d, i, memo))
	}
	return best
}

var seed int64 = 1340

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := 1000
	arrays := make([][]int, 20)
	for a := range arrays {
		arrays[a] = make([]int, n)
		for k := 0; k < n; k++ {
			if a%2 == 0 {
				arrays[a][k] = int(1 + nextRandom()%100000)
			} else {
				arrays[a][k] = int(100*int64(k) + 1 + nextRandom()%100)
			}
		}
	}
	var check int64
	for pass := int64(0); pass < 20; pass++ {
		for a := 0; a < 20; a++ {
			arrays[a][check%int64(n)] = int(1 + (check/7)%100000)
			d := 1000
			if a%2 == 1 {
				d = 300
			}
			answer := maxJumps(arrays[a], d)
			check = (check*31 + int64(answer) + pass) % 1000000007
		}
	}
	fmt.Printf("20 passes over 20 arrays of 1000: checksum %d\n", check)
}
