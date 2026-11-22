// LeetCode #2865: Beautiful Towers I -- the bench, as towers.kara: 2000
// arrays of 10^3 towers, each answered 20 times by the stack arm.
package main

import "fmt"

func maximumSumOfHeights(h []int64) int64 {
	n := int64(len(h))
	left := make([]int64, n)
	right := make([]int64, n)
	stack := make([]int64, 0)
	for i := int64(0); i < n; i++ {
		for len(stack) > 0 && h[stack[len(stack)-1]] > h[i] {
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			j := stack[len(stack)-1]
			left[i] = left[j] + (i-j)*h[i]
		} else {
			left[i] = (i + 1) * h[i]
		}
		stack = append(stack, i)
	}
	stack = stack[:0]
	var best int64
	for i := n - 1; i >= 0; i-- {
		for len(stack) > 0 && h[stack[len(stack)-1]] > h[i] {
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			j := stack[len(stack)-1]
			right[i] = right[j] + (j-i)*h[i]
		} else {
			right[i] = (n - i) * h[i]
		}
		stack = append(stack, i)
		if here := left[i] + right[i] - h[i]; here > best {
			best = here
		}
	}
	return best
}

var seed int64 = 2865

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 2000, 20, 1000
	arrays := make([][]int64, count)
	for c := 0; c < count; c++ {
		top := int64(50)
		if c%2 == 0 {
			top = 1000000000
		}
		arrays[c] = make([]int64, n)
		for i := range arrays[c] {
			arrays[c][i] = wide()%top + 1
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, heights := range arrays {
			best := maximumSumOfHeights(heights)
			total += best
			check = (check*31 + best%1000000007 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: sums total %d, checksum %d\n", count, n, rounds, total, check)
}
