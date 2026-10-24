// Benchmark: LeetCode #975 Odd Even Jump -- the stack arm (sorted order
// and a monotonic stack), on 20 arrays of 20000 random values. Mirrors
// odd_even_jumps.kara, .rs, .c and .py.
package main

import (
	"fmt"
	"sort"
)

func nextIn(order []int, n int) []int {
	next := make([]int, n)
	for i := range next {
		next[i] = -1
	}
	stack := []int{}
	for _, i := range order {
		for len(stack) > 0 && stack[len(stack)-1] < i {
			next[stack[len(stack)-1]] = i
			stack = stack[:len(stack)-1]
		}
		stack = append(stack, i)
	}
	return next
}

func oddEvenJumps(arr []int64) int {
	n := len(arr)
	up := make([]int, n)
	down := make([]int, n)
	for i := range up {
		up[i], down[i] = i, i
	}
	sort.Slice(up, func(a, b int) bool {
		i, j := up[a], up[b]
		if arr[i] != arr[j] {
			return arr[i] < arr[j]
		}
		return i < j
	})
	sort.Slice(down, func(a, b int) bool {
		i, j := down[a], down[b]
		if arr[i] != arr[j] {
			return arr[i] > arr[j]
		}
		return i < j
	})
	odd := nextIn(up, n)
	even := nextIn(down, n)
	higher := make([]bool, n)
	lower := make([]bool, n)
	higher[n-1], lower[n-1] = true, true
	for i := n - 2; i >= 0; i-- {
		if odd[i] >= 0 {
			higher[i] = lower[odd[i]]
		}
		if even[i] >= 0 {
			lower[i] = higher[even[i]]
		}
	}
	good := 0
	for _, h := range higher {
		if h {
			good++
		}
	}
	return good
}

var seed int64 = 975

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count := 10, 20
	arrays := make([][]int64, count)
	for c := range arrays {
		arrays[c] = make([]int64, 20000)
		for i := range arrays[c] {
			arrays[c][i] = nextRandom() % 100000
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			good := int64(oddEvenJumps(arrays[(r+i)%count]))
			total += good
			check = (check*31 + good) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d arrays of 20000 values: %d good starts, checksum %d\n", rounds, count, total, check)
}
