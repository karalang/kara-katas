// Benchmark for #826: Most Profit Assigning Work -- the ★ arm (two sorted sweeps).
//
// Mirrors max_profit_assignment.kara: the jobs paired and sorted by
// difficulty (then profit) and a copy of the workers sorted, then one
// pointer walks the jobs as the abilities grow, keeping the best profit
// among the jobs passed.
package main

import (
	"fmt"
	"sort"
)

type job struct{ d, p int64 }

func maxProfitAssignment(difficulty, profit, worker []int64) int64 {
	n := len(difficulty)
	jobs := make([]job, 0, n)
	for i := 0; i < n; i++ {
		jobs = append(jobs, job{difficulty[i], profit[i]})
	}
	sort.Slice(jobs, func(a, b int) bool {
		if jobs[a].d != jobs[b].d {
			return jobs[a].d < jobs[b].d
		}
		return jobs[a].p < jobs[b].p
	})
	abilities := append([]int64(nil), worker...)
	sort.Slice(abilities, func(a, b int) bool { return abilities[a] < abilities[b] })
	next := 0
	var best, total int64
	for _, ability := range abilities {
		for next < n && jobs[next].d <= ability {
			if jobs[next].p > best {
				best = jobs[next].p
			}
			next++
		}
		total += best
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func draw(seed *int64, count int) []int64 {
	v := make([]int64, count)
	for i := range v {
		v[i] = 1 + nextRandom(seed)%100000
	}
	return v
}

func main() {
	count := 64
	rounds := 2000
	seed := int64(826)
	var difficulties, profits, workers [][]int64
	for g := 0; g < count; g++ {
		difficulties = append(difficulties, draw(&seed, 10000))
		profits = append(profits, draw(&seed, 10000))
		workers = append(workers, draw(&seed, 10000))
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		g := round % count
		r := maxProfitAssignment(difficulties[g], profits[g], workers[g])
		total += r
		checksum = (checksum*131 + r) % 1000000007
	}
	fmt.Printf("%d rounds of %d cases: total %d, checksum %d\n", rounds, count, total, checksum)
}
