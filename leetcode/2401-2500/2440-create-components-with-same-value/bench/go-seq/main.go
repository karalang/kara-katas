// LeetCode #2440: Create Components With Same Value -- the bench, the ★
// arm: each component count dividing the total, from `n` down, checked by
// gathering subtree sums in reverse breadth-first order.
package main

import "fmt"

func fits(order, parent, nums []int64, target int64) bool {
	sum := append([]int64(nil), nums...)
	for i := len(order); i > 0; {
		i--
		u := order[i]
		if sum[u] > target {
			return false
		}
		if sum[u] < target {
			if u == 0 {
				return false
			}
			sum[parent[u]] += sum[u]
		}
	}
	return true
}

func componentValue(nums []int64, edges [][]int64) int64 {
	n := int64(len(nums))
	adjacent := make([][]int64, n)
	for _, e := range edges {
		adjacent[e[0]] = append(adjacent[e[0]], e[1])
		adjacent[e[1]] = append(adjacent[e[1]], e[0])
	}
	parent := make([]int64, n)
	for i := range parent {
		parent[i] = -1
	}
	order := []int64{0}
	seen := make([]bool, n)
	seen[0] = true
	for head := 0; head < len(order); head++ {
		u := order[head]
		for _, v := range adjacent[u] {
			if !seen[v] {
				seen[v] = true
				parent[v] = u
				order = append(order, v)
			}
		}
	}
	var total int64
	for _, x := range nums {
		total += x
	}
	for k := n; k > 1; k-- {
		if total%k == 0 && fits(order, parent, nums, total/k) {
			return k - 1
		}
	}
	return 0
}

var seed int64 = 2440

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := int64(20000)
	trees := make([][][]int64, 10)
	values := make([][]int64, 10)
	for c := 0; c < 10; c++ {
		edges := make([][]int64, 0, n-1)
		for i := int64(1); i < n; i++ {
			edges = append(edges, []int64{nextRandom() % i, i})
		}
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = 1 + nextRandom()%50
		}
		trees[c] = edges
		values[c] = nums
	}
	var check int64
	for p := int64(0); p < 50; p++ {
		for c := range trees {
			at := (p*7919 + int64(c)*104729) % n
			values[c][at] = 1 + nextRandom()%50
			check = (check*31 + componentValue(values[c], trees[c]) + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 10 trees of 2 * 10^4 nodes: checksum %d\n", check)
}
