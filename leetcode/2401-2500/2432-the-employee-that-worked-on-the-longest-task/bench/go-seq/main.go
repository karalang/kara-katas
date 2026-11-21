// LeetCode #2432: The Employee That Worked on the Longest Task -- the
// bench, the ★ arm: one pass with the last leave time in hand, the best
// replaced by a longer task or an equal one of a smaller id.
package main

import "fmt"

func hardestWorker(n int64, logs [][]int64) int64 {
	bestID, bestTime, start := n, int64(0), int64(0)
	for _, log := range logs {
		time := log[1] - start
		if time > bestTime || (time == bestTime && log[0] < bestID) {
			bestTime = time
			bestID = log[0]
		}
		start = log[1]
	}
	return bestID
}

var seed int64 = 2432

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var cases [][][]int64
	for c := 0; c < 2000; c++ {
		var logs [][]int64
		var time, last int64 = 0, -1
		for i := 0; i < 500; i++ {
			id := nextRandom() % 500
			if id == last {
				id = (id + 1) % 500
			}
			time += 1 + nextRandom()%3
			logs = append(logs, []int64{id, time})
			last = id
		}
		cases = append(cases, logs)
	}
	var check int64
	for p := int64(0); p < 50; p++ {
		for c := range cases {
			cases[c][499][1]++
			check = (check*31 + hardestWorker(500, cases[c]) + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 2000 cases of 500 logs: checksum %d\n", check)
}
