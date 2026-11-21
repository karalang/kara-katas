// LeetCode #2382: Maximum Segment Sum After Removals -- the bench, the ★
// arm in Go: the removals undone in reverse with a union-find, each root
// keeping its segment's sum.
package main

import "fmt"

func find(parent []int64, x int64) int64 {
	root := x
	for parent[root] != root {
		parent[root] = parent[parent[root]]
		root = parent[root]
	}
	return root
}

func join(parent, sum []int64, a, b int64) {
	ra := find(parent, a)
	rb := find(parent, b)
	if ra != rb {
		parent[ra] = rb
		sum[rb] += sum[ra]
	}
}

func maximumSegmentSum(nums, removeQueries []int64) []int64 {
	n := int64(len(nums))
	parent := make([]int64, n)
	for i := range parent {
		parent[i] = int64(i)
	}
	sum := make([]int64, n)
	back := make([]bool, n)
	answer := make([]int64, n)
	best := int64(0)
	for k := n - 1; k >= 1; k-- {
		x := removeQueries[k]
		back[x] = true
		sum[x] = nums[x]
		if x > 0 && back[x-1] {
			join(parent, sum, x-1, x)
		}
		if x+1 < n && back[x+1] {
			join(parent, sum, x+1, x)
		}
		best = max(best, sum[find(parent, x)])
		answer[k-1] = best
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	high := nextRandom(seed)
	return high*32768 + nextRandom(seed)
}

func main() {
	// 10 arrays of 10^5 values, array a's values from 1 to 10^a, each with
	// its own random order of removals
	seed := int64(2382)
	n := int64(100000)
	arrays := make([][]int64, 0, 10)
	orders := make([][]int64, 0, 10)
	for a := 0; a < 10; a++ {
		top := int64(1)
		for k := 0; k < a; k++ {
			top *= 10
		}
		values := make([]int64, n)
		for i := range values {
			values[i] = 1 + wide(&seed)%top
		}
		arrays = append(arrays, values)
		order := make([]int64, n)
		for i := range order {
			order[i] = int64(i)
		}
		for i := n - 1; i >= 1; i-- {
			j := wide(&seed) % (i + 1)
			order[i], order[j] = order[j], order[i]
		}
		orders = append(orders, order)
	}
	check := int64(0)
	for p := int64(0); p < 10; p++ {
		for a := 0; a < 10; a++ {
			answer := maximumSegmentSum(arrays[a], orders[a])
			for _, v := range answer {
				check = (check*31 + v + p) % 1000000007
			}
		}
	}
	fmt.Printf("10 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
