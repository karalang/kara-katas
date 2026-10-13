// Benchmark for #517: Go mirror of the ★ arm (the flow across each gap);
// see ../find_min_moves.kara.
package main

import "fmt"

func findMinMoves(machines []int64) int64 {
	n := int64(len(machines))
	var total int64
	for _, m := range machines {
		total += m
	}
	if total%n != 0 {
		return -1
	}
	average := total / n
	var moves, surplus int64
	for _, m := range machines {
		extra := m - average
		surplus += extra
		flow := surplus
		if flow < 0 {
			flow = -flow
		}
		moves = max(moves, flow, extra)
	}
	return moves
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 100 random rows of 10,000 machines (the problem's most) holding up
	// to 100,000 dresses each, every other row topped up so the dresses
	// share out evenly, built once. Then each is solved 300 times.
	seed := int64(517)
	rows := 100
	all := make([][]int64, 0, rows)
	for t := 0; t < rows; t++ {
		machines := make([]int64, 0, 10000)
		var total int64
		for i := 0; i < 10000; i++ {
			a := nextRandom(&seed)
			b := nextRandom(&seed)
			m := (a*32768 + b) % 100001
			machines = append(machines, m)
			total += m
		}
		if t%2 == 0 {
			machines[9999] += (10000 - total%10000) % 10000
		}
		all = append(all, machines)
	}
	var checksum int64
	for r := 0; r < 300; r++ {
		for t := 0; t < rows; t++ {
			checksum = (checksum*31 + findMinMoves(all[t]) + 1) % 1000000007
		}
	}
	fmt.Printf("%d rows of 10000 machines, 300 times each: checksum %d\n", rows, checksum)
}
