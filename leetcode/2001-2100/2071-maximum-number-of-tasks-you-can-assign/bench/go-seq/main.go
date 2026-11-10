// LeetCode #2071: Maximum Number of Tasks You Can Assign -- Go mirror of
// the ★ arm's benchmark (tasks.kara): 12 problems of 50000 tasks and 50000
// workers, strengths up to 1000000000, 0 to 11000 pills of strength
// 10000000.
// The deque is a slice the size of the tasks, a head and a tail.
package main

import (
	"fmt"
	"sort"
)

func canDo(tasks, workers []int64, k int, pills, strength int64, waiting []int64) bool {
	left := pills
	head, tail, next := 0, 0, 0
	for _, w := range workers[len(workers)-k:] {
		for next < k && tasks[next] <= w+strength {
			waiting[tail] = tasks[next]
			tail++
			next++
		}
		if head == tail {
			return false
		}
		if waiting[head] <= w {
			head++
		} else {
			if left == 0 {
				return false
			}
			left--
			tail--
		}
	}
	return true
}

func maxTaskAssign(tasks, workers []int64, pills, strength int64) int64 {
	sort.Slice(tasks, func(i, j int) bool { return tasks[i] < tasks[j] })
	sort.Slice(workers, func(i, j int) bool { return workers[i] < workers[j] })
	waiting := make([]int64, len(tasks))
	lo, hi := 0, len(tasks)
	if len(workers) < hi {
		hi = len(workers)
	}
	for lo < hi {
		mid := (lo + hi + 1) / 2
		if canDo(tasks, workers, mid, pills, strength, waiting) {
			lo = mid
		} else {
			hi = mid - 1
		}
	}
	return int64(lo)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func strengths(n int, low, high int64, seed *int64) []int64 {
	out := make([]int64, n)
	for i := range out {
		a := nextRandom(seed)
		b := nextRandom(seed)
		out[i] = low + (a*32768+b)%(high-low+1)
	}
	return out
}

func main() {
	seed := int64(2071)
	total, check := int64(0), int64(0)
	for t := int64(0); t < 12; t++ {
		tasks := strengths(50000, 0, 1000000000, &seed)
		workers := strengths(50000, 0, 1000000000, &seed)
		a := maxTaskAssign(tasks, workers, t*1000, 10000000)
		total += a
		check = (check*31 + a) % 1000000007
	}
	fmt.Printf("12 problems: sum %d, checksum %d\n", total, check)
}
