// LeetCode #2322: Minimum Score After Removals on a Tree -- the bench, the
// ★ arm in Go. Rooted at 0, two removals are two nodes other than the
// root; one walk gives each subtree's XOR and each node's entry and exit
// times, and the three parts follow from whether one node is the other's
// ancestor. O(n^2).
package main

import (
	"fmt"
	"math"
)

func visit(node, parent int, adjacent [][]int, nums, xor []int64, enter, leave []int, clock *int) {
	enter[node] = *clock
	*clock++
	xor[node] = nums[node]
	for _, next := range adjacent[node] {
		if next != parent {
			visit(next, node, adjacent, nums, xor, enter, leave, clock)
			xor[node] ^= xor[next]
		}
	}
	leave[node] = *clock
}

func minimumScore(nums []int64, edges [][2]int) int64 {
	n := len(nums)
	adjacent := make([][]int, n)
	for _, e := range edges {
		adjacent[e[0]] = append(adjacent[e[0]], e[1])
		adjacent[e[1]] = append(adjacent[e[1]], e[0])
	}
	xor := make([]int64, n)
	enter := make([]int, n)
	leave := make([]int, n)
	clock := 0
	visit(0, -1, adjacent, nums, xor, enter, leave, &clock)
	whole := xor[0]
	best := int64(math.MaxInt64)
	for a := 1; a < n; a++ {
		for b := a + 1; b < n; b++ {
			var x, y, z int64
			if enter[a] <= enter[b] && leave[b] <= leave[a] {
				x, y, z = xor[b], xor[a]^xor[b], whole^xor[a]
			} else if enter[b] <= enter[a] && leave[a] <= leave[b] {
				x, y, z = xor[a], xor[b]^xor[a], whole^xor[b]
			} else {
				x, y, z = xor[a], xor[b], whole^xor[a]^xor[b]
			}
			best = min(best, max(x, y, z)-min(x, y, z))
		}
	}
	return best
}

var seed int64 = 2322

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 1000
	values := make([][]int64, 10)
	shapes := make([][][2]int, 10)
	for k := 0; k < 10; k++ {
		values[k] = make([]int64, n)
		for i := range values[k] {
			values[k][i] = nextRandom()%100000000 + 1
		}
		for i := 1; i < n; i++ {
			shapes[k] = append(shapes[k], [2]int{int(nextRandom() % int64(i)), i})
		}
	}
	var check int64
	for p := 0; p < 30; p++ {
		for k := 0; k < 10; k++ {
			i := nextRandom() % n
			values[k][i] = nextRandom()%100000000 + 1
			check = (check*31 + minimumScore(values[k], shapes[k])) % 1000000007
		}
	}
	fmt.Printf("30 passes over 10 trees of 1000 nodes: checksum %d\n", check)
}
