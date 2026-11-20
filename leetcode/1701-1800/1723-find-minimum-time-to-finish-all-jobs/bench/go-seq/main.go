// LeetCode #1723: Find Minimum Time to Finish All Jobs -- the bench
// (jobs.kara): each job, the longest first, tried on every worker by
// backtracking, a branch cut once it cannot beat the best finish found,
// and only the first idle worker tried.
package main

import (
	"fmt"
	"sort"
)

func place(jobs []int32, i int, loads []int32, best *int32) {
	if i == len(jobs) {
		most := loads[0]
		for _, l := range loads[1:] {
			if l > most {
				most = l
			}
		}
		*best = most
		return
	}
	for w := range loads {
		if loads[w]+jobs[i] < *best {
			loads[w] += jobs[i]
			place(jobs, i+1, loads, best)
			loads[w] -= jobs[i]
		}
		if loads[w] == 0 {
			break
		}
	}
}

func minimumTimeRequired(jobs []int32, k int) int32 {
	order := append([]int32(nil), jobs...)
	sort.Slice(order, func(a, b int) bool { return order[a] > order[b] })
	var total int32
	for _, j := range order {
		total += j
	}
	loads := make([]int32, k)
	best := total + 1
	place(order, 0, loads, &best)
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func main() {
	count := 100
	var rounds int64 = 5
	n := 12
	var seed int64 = 1723
	jobs := make([][]int32, count)
	ks := make([]int, count)
	for c := 0; c < count; c++ {
		jobs[c] = make([]int32, n)
		for i := range jobs[c] {
			jobs[c][i] = int32(wide(&seed)%10000000 + 1)
		}
		ks[c] = int(nextRandom(&seed)%11 + 2)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			answer := int64(minimumTimeRequired(jobs[c], ks[c]))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d jobs, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
