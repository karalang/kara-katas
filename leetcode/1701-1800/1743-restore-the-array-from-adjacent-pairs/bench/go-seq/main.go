// LeetCode #1743: Restore the Array From Adjacent Pairs -- the bench
// (restore.kara in Go): the pairs as a graph, walked from an end.
package main

import "fmt"

func restoreArray(adjacentPairs [][2]int32) []int32 {
	next := make(map[int32][]int32)
	for _, pair := range adjacentPairs {
		next[pair[0]] = append(next[pair[0]], pair[1])
		next[pair[1]] = append(next[pair[1]], pair[0])
	}
	var start int32
	for v, near := range next {
		if len(near) == 1 {
			start = v
			break
		}
	}
	order := []int32{start, next[start][0]}
	for len(order) < len(adjacentPairs)+1 {
		before, last := order[len(order)-2], order[len(order)-1]
		near := next[last]
		if near[0] == before {
			order = append(order, near[1])
		} else {
			order = append(order, near[0])
		}
	}
	return order
}

var seed int64 = 1743

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func randomPairs(n int) [][2]int32 {
	taken := make(map[int64]bool)
	values := make([]int32, 0, n)
	for len(values) < n {
		v := wide()%200001 - 100000
		if !taken[v] {
			taken[v] = true
			values = append(values, int32(v))
		}
	}
	pairs := make([][2]int32, 0, n-1)
	for i := 1; i < n; i++ {
		if nextRandom()%2 == 0 {
			pairs = append(pairs, [2]int32{values[i-1], values[i]})
		} else {
			pairs = append(pairs, [2]int32{values[i], values[i-1]})
		}
	}
	for i := len(pairs) - 1; i >= 1; i-- {
		j := (nextRandom()*32768 + nextRandom()) % int64(i+1)
		pairs[i], pairs[j] = pairs[j], pairs[i]
	}
	return pairs
}

func main() {
	const count, rounds, n = 10, 4, 100000
	problems := make([][][2]int32, count)
	for i := range problems {
		problems[i] = randomPairs(n)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, pairs := range problems {
			order := restoreArray(pairs)
			first, last := order[0], order[len(order)-1]
			middle := order[len(order)-1-len(order)/2]
			if first < last {
				middle = order[len(order)/2]
			}
			low := int64(min(first, last))
			sum += low
			check = (check*31 + low + int64(middle) + 200000 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: smaller ends sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
