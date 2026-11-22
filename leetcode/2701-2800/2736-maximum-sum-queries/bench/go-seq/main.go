// LeetCode #2736: Maximum Sum Queries -- the bench (queries.kara in Go):
// pairs and queries by nums1 and x falling, a stack of (nums2, sum) with
// nums2 rising and sums falling, and a binary search per query.
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type pair struct{ a, b int64 }

func maximumSumQueries(nums1, nums2 []int64, queries [][]int64) []int64 {
	n := len(nums1)
	pairs := make([]pair, n)
	for i := range pairs {
		pairs[i] = pair{nums1[i], nums2[i]}
	}
	slices.SortStableFunc(pairs, func(p, q pair) int { return cmp.Compare(q.a, p.a) })
	order := make([]int, len(queries))
	for i := range order {
		order[i] = i
	}
	slices.SortStableFunc(order, func(p, q int) int { return cmp.Compare(queries[q][0], queries[p][0]) })
	answer := make([]int64, len(queries))
	for i := range answer {
		answer[i] = -1
	}
	stack := []pair{}
	j := 0
	for _, q := range order {
		x, y := queries[q][0], queries[q][1]
		for j < n && pairs[j].a >= x {
			a, b := pairs[j].a, pairs[j].b
			j++
			if len(stack) > 0 && stack[len(stack)-1].a >= b {
				continue
			}
			for len(stack) > 0 && stack[len(stack)-1].b <= a+b {
				stack = stack[:len(stack)-1]
			}
			stack = append(stack, pair{b, a + b})
		}
		low, high := 0, len(stack)
		for low < high {
			middle := (low + high) / 2
			if stack[middle].a >= y {
				high = middle
			} else {
				low = middle + 1
			}
		}
		if low < len(stack) {
			answer[q] = stack[low].b
		}
	}
	return answer
}

var seed int64 = 2736

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomUpTo(most int64) int64 {
	hi := nextRandom()
	return (hi*32768+nextRandom())%most + 1
}

type problem struct {
	nums1, nums2 []int64
	queries      [][]int64
}

func main() {
	const cases, n, rounds = 10, 100000, 3
	problems := []problem{}
	for c := 0; c < cases; c++ {
		nums1 := make([]int64, n)
		for i := range nums1 {
			nums1[i] = randomUpTo(1000000000)
		}
		nums2 := make([]int64, n)
		for i := range nums2 {
			nums2[i] = randomUpTo(1000000000)
		}
		queries := make([][]int64, n)
		for i := range queries {
			x := randomUpTo(1000000000)
			queries[i] = []int64{x, randomUpTo(1000000000)}
		}
		problems = append(problems, problem{nums1, nums2, queries})
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range problems {
			for _, best := range maximumSumQueries(p.nums1, p.nums2, p.queries) {
				sum += best
				check = (check*31 + best + 1 + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d cases of %d pairs and queries, %d rounds: answers sum to %d, checksum %d\n", cases, n, rounds, sum, check)
}
