// LeetCode #2747: Count Zero Request Servers -- the bench (servers.kara in
// Go): the logs sorted by time, the queries in time order, and a window of
// logs sliding forward with a count for each server.
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type entry struct{ time, server int64 }

func countServers(n int64, logs [][2]int64, x int64, queries []int64) []int64 {
	byTime := make([]entry, len(logs))
	for i, log := range logs {
		byTime[i] = entry{log[1], log[0]}
	}
	slices.SortFunc(byTime, func(a, b entry) int {
		if c := cmp.Compare(a.time, b.time); c != 0 {
			return c
		}
		return cmp.Compare(a.server, b.server)
	})
	order := make([]int, len(queries))
	for i := range order {
		order[i] = i
	}
	slices.SortStableFunc(order, func(a, b int) int { return cmp.Compare(queries[a], queries[b]) })
	requests := make([]int64, n+1)
	var busy int64
	answers := make([]int64, len(queries))
	start, end := 0, 0
	for _, i := range order {
		q := queries[i]
		for end < len(byTime) && byTime[end].time <= q {
			s := byTime[end].server
			if requests[s] == 0 {
				busy++
			}
			requests[s]++
			end++
		}
		for start < end && byTime[start].time < q-x {
			s := byTime[start].server
			requests[s]--
			if requests[s] == 0 {
				busy--
			}
			start++
		}
		answers[i] = n - busy
	}
	return answers
}

var seed int64 = 2747

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type testCase struct {
	logs    [][2]int64
	x       int64
	queries []int64
}

func main() {
	const count, rounds = 10, 3
	const n int64 = 100000
	cases := []testCase{}
	for k := 0; k < count; k++ {
		x := (nextRandom()*32768+nextRandom())%100000 + 1
		logs := make([][2]int64, 100000)
		for i := range logs {
			server := nextRandom()%n + 1
			hi := nextRandom()
			logs[i] = [2]int64{server, (hi*32768+nextRandom())%1000000 + 1}
		}
		queries := make([]int64, 100000)
		for i := range queries {
			hi := nextRandom()
			queries[i] = x + 1 + (hi*32768+nextRandom())%(1000000-x)
		}
		cases = append(cases, testCase{logs, x, queries})
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, c := range cases {
			for _, a := range countServers(n, c.logs, c.x, c.queries) {
				sum += a
				check = (check*31 + a + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d cases of 100000 logs and queries, %d rounds: answers sum to %d, checksum %d\n", count, rounds, sum, check)
}
