// LeetCode #2792: Count Nodes That Are Great Enough -- the bench in Go:
// the ★ arm over 20 random trees of 10^4 nodes with values up to 10^4
// and k = 10, all drawn first, then each answered 20 times.
package main

import (
	"fmt"
	"slices"
)

func countGreatEnoughNodes(vals, left, right []int64, k int) int64 {
	n := len(vals)
	order := []int64{}
	stack := []int64{0}
	for len(stack) > 0 {
		u := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		order = append(order, u)
		for _, c := range [2]int64{left[u], right[u]} {
			if c >= 0 {
				stack = append(stack, c)
			}
		}
	}
	least := make([][]int64, n)
	var great int64
	for j := len(order) - 1; j >= 0; j-- {
		u := order[j]
		mine := []int64{vals[u]}
		for _, c := range [2]int64{left[u], right[u]} {
			if c >= 0 {
				mine = append(mine, least[c]...)
			}
		}
		slices.Sort(mine)
		if len(mine) > k {
			mine = mine[:k]
		}
		if len(mine) == k && mine[k-1] < vals[u] {
			great++
		}
		least[u] = mine
	}
	return great
}

var seed int64 = 2792

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 20
	rounds := 20
	n := 10000
	vals := make([][]int64, count)
	lefts := make([][]int64, count)
	rights := make([][]int64, count)
	for c := 0; c < count; c++ {
		vals[c] = make([]int64, n)
		for i := range vals[c] {
			vals[c][i] = nextRandom()%10000 + 1
		}
		lefts[c] = make([]int64, n)
		rights[c] = make([]int64, n)
		for i := range lefts[c] {
			lefts[c][i], rights[c][i] = -1, -1
		}
		for i := 1; i < n; i++ {
			for {
				p := nextRandom() % int64(i)
				if nextRandom()%2 == 0 {
					if lefts[c][p] < 0 {
						lefts[c][p] = int64(i)
						break
					}
				} else if rights[c][p] < 0 {
					rights[c][p] = int64(i)
					break
				}
			}
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := countGreatEnoughNodes(vals[c], lefts[c], rights[c], 10)
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d trees of 10^4, %d rounds: great enough sum to %d, checksum %d\n", count, rounds, total, check)
}
