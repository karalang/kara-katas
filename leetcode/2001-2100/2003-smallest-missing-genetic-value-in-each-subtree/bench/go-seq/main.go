// LeetCode #2003: Smallest Missing Genetic Value in Each Subtree -- the
// benchmark's Go twin, the same algorithm as genetic.kara here.
package main

import "fmt"

func mark(u int64, children [][]int64, nums []int64, seen []bool, visited []bool) {
	visited[u] = true
	if nums[u] < int64(len(seen)) {
		seen[nums[u]] = true
	}
	for _, c := range children[u] {
		if !visited[c] {
			mark(c, children, nums, seen, visited)
		}
	}
}

func smallestMissing(parents, nums []int64) []int64 {
	n := len(parents)
	answer := make([]int64, n)
	for i := range answer {
		answer[i] = 1
	}
	one := int64(-1)
	for i, v := range nums {
		if v == 1 {
			one = int64(i)
			break
		}
	}
	if one == -1 {
		return answer
	}
	children := make([][]int64, n)
	for i := 1; i < n; i++ {
		children[parents[i]] = append(children[parents[i]], int64(i))
	}
	seen := make([]bool, n+2)
	visited := make([]bool, n)
	missing := int64(1)
	for u := one; u != -1; u = parents[u] {
		mark(u, children, nums, seen, visited)
		for seen[missing] {
			missing++
		}
		answer[u] = missing
	}
	return answer
}

var seed int64 = 2003

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n, width, extra int64) ([]int64, []int64) {
	parents := []int64{-1}
	for i := int64(1); i < n; i++ {
		lo := i - width
		if lo < 0 {
			lo = 0
		}
		parents = append(parents, lo+nextRandom()%(i-lo))
	}
	values := make([]int64, n+extra)
	for i := range values {
		values[i] = int64(i) + 1
	}
	for i := int64(len(values)) - 1; i >= 1; i-- {
		j := nextRandom() % (i + 1)
		values[i], values[j] = values[j], values[i]
	}
	return parents, values[:n]
}

func main() {
	// 40 trees of 20000 nodes built once, then the ★ arm on each, 25 rounds
	type tree struct{ parents, nums []int64 }
	var trees []tree
	widths := []int64{2, 5, 50, 20000}
	for a := int64(0); a < 40; a++ {
		p, v := randomTree(20000, widths[a%4], a%2)
		trees = append(trees, tree{p, v})
	}
	var calls, sum, check int64
	for r := 0; r < 25; r++ {
		for _, t := range trees {
			answer := smallestMissing(t.parents, t.nums)
			calls++
			for _, a := range answer {
				sum += a
				check = (check*31 + a) % 1000000007
			}
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
