// Benchmark workload for LeetCode #351 — Go mirror of unlock_patterns.kara.
// The same search: a skip table, runs from keys 1, 2 and 5 weighted 4, 4, 1.
package main

import "fmt"

const rounds = 48

func skipTable() []int64 {
	skip := make([]int64, 100)
	pairs := [][3]int64{{1, 3, 2}, {4, 6, 5}, {7, 9, 8}, {1, 7, 4}, {2, 8, 5}, {3, 9, 6}, {1, 9, 5}, {3, 7, 5}}
	for _, p := range pairs {
		skip[p[0]*10+p[1]] = p[2]
		skip[p[1]*10+p[0]] = p[2]
	}
	return skip
}

func countFrom(key, length, m, n int64, visited []bool, skip []int64) int64 {
	var total int64
	if length >= m {
		total++
	}
	if length == n {
		return total
	}
	visited[key] = true
	for next := int64(1); next < 10; next++ {
		mid := skip[key*10+next]
		if !visited[next] && (mid == 0 || visited[mid]) {
			total += countFrom(next, length+1, m, n, visited, skip)
		}
	}
	visited[key] = false
	return total
}

func numberOfPatterns(m, n int64) int64 {
	if m > n {
		return 0
	}
	skip := skipTable()
	visited := make([]bool, 10)
	corner := countFrom(1, 1, m, n, visited, skip)
	edge := countFrom(2, 1, m, n, visited, skip)
	center := countFrom(5, 1, m, n, visited, skip)
	return 4*corner + 4*edge + center
}

func main() {
	var sink int64
	for round := int64(0); round < rounds; round++ {
		for m := int64(1); m < 10; m++ {
			for n := int64(1); n < 10; n++ {
				c := numberOfPatterns(m, n)
				sink = (sink*31 + c + round) % 1000000007
			}
		}
	}
	fmt.Printf("sink %d\n", sink)
}
