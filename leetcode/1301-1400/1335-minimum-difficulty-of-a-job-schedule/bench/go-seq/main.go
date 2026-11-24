// LeetCode #1335 bench, Go mirror of the Kāra bench: the ★ arm on 20
// schedules of 300 jobs built once, then 30 passes, each setting one job
// of every schedule and the number of days from the checksum so far,
// answering every schedule.
package main

import (
	"fmt"
	"math"
)

func minDifficulty(jobDifficulty []int32, d int) int {
	n := len(jobDifficulty)
	if n < d {
		return -1
	}
	const far = math.MaxInt64 / 2
	best := make([]int64, n+1)
	for i := range best {
		best[i] = far
	}
	best[0] = 0
	for day := 1; day <= d; day++ {
		next := make([]int64, n+1)
		for i := range next {
			next[i] = far
		}
		for i := day; i <= n; i++ {
			var hardest int64
			for j := i - 1; j >= day-1; j-- {
				hardest = max(hardest, int64(jobDifficulty[j]))
				next[i] = min(next[i], best[j]+hardest)
			}
		}
		best = next
	}
	return int(best[n])
}

var seed int64 = 1335

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 300
	schedules := make([][]int32, 20)
	for t := range schedules {
		jobs := make([]int32, n)
		for i := range jobs {
			jobs[i] = int32(nextRandom() % 1001)
		}
		schedules[t] = jobs
	}
	var check int64
	for pass := int64(0); pass < 30; pass++ {
		d := int(6 + check%5)
		for t := 0; t < 20; t++ {
			at := check % n
			schedules[t][at] = int32(check / 3 % 1001)
			answer := minDifficulty(schedules[t], d)
			check = (check*31 + int64(answer) + pass) % 1000000007
		}
	}
	fmt.Printf("30 passes over 20 schedules of 300 jobs: checksum %d\n", check)
}
