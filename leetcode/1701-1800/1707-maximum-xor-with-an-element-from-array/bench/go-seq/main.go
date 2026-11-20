// LeetCode #1707: Maximum XOR With an Element From Array -- the bench's Go
// mirror: the ★ arm on 4 random problems of 100000 values and 100000
// queries, all drawn first, each answered 3 times.
package main

import (
	"fmt"
	"sort"
)

// the queries offline by limit, against a 30-bit trie of the values allowed
func maximizeXor(nums []int32, queries [][2]int32) []int32 {
	values := append([]int32(nil), nums...)
	sort.Slice(values, func(a, b int) bool { return values[a] < values[b] })
	order := make([]int, len(queries))
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(a, b int) bool { return queries[order[a]][1] < queries[order[b]][1] })
	// children of each node, 0 for none: the root is node 0
	trie := [][2]int64{{0, 0}}
	next := 0
	answer := make([]int32, len(queries))
	for i := range answer {
		answer[i] = -1
	}
	for _, i := range order {
		x, m := int64(queries[i][0]), queries[i][1]
		for next < len(values) && values[next] <= m {
			node := int64(0)
			for bit := 29; bit >= 0; bit-- {
				b := int64(values[next]) >> bit & 1
				if trie[node][b] == 0 {
					trie = append(trie, [2]int64{0, 0})
					trie[node][b] = int64(len(trie) - 1)
				}
				node = trie[node][b]
			}
			next++
		}
		if next == 0 {
			continue
		}
		node, best := int64(0), int64(0)
		for bit := 29; bit >= 0; bit-- {
			want := (x >> bit & 1) ^ 1
			if trie[node][want] != 0 {
				best |= 1 << bit
				node = trie[node][want]
			} else {
				node = trie[node][want^1]
			}
		}
		answer[i] = int32(best)
	}
	return answer
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1707

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// a random value below 10^9, from two draws
func value() int64 {
	a := nextRandom()
	return (a*32768 + nextRandom()) % 1000000000
}

func main() {
	const count, rounds, n = 4, 3, 100000
	allNums := make([][]int32, count)
	allQueries := make([][][2]int32, count)
	for c := 0; c < count; c++ {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32(value())
		}
		queries := make([][2]int32, n)
		for i := range queries {
			x := int32(value())
			queries[i] = [2]int32{x, int32(value())}
		}
		allNums[c] = nums
		allQueries[c] = queries
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			for _, a := range maximizeXor(allNums[c], allQueries[c]) {
				sum += int64(a)
				check = (check*31 + int64(a) + 1 + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d problems of %d values and %d queries, %d rounds: answers sum to %d, checksum %d\n", count, n, n, rounds, sum, check)
}
