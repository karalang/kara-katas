// LeetCode #2365: Task Scheduler II -- the bench, the ★ arm in Go: the day
// goes forward one for each task, and jumps to the day after the type's
// last run plus `space` when that is later; a map keeps each type's last
// day.
package main

import "fmt"

func taskSchedulerII(tasks []int64, space int64) int64 {
	last := map[int64]int64{}
	day := int64(0)
	for _, task := range tasks {
		day++
		if before, ok := last[task]; ok {
			day = max(day, before+space+1)
		}
		last[task] = day
	}
	return day
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wideRandom(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

type list struct {
	tasks []int64
	space int64
}

func main() {
	// list a: 10^5 tasks of 4^(a / 2 + 1) types (at most 10^5) up to
	// 10^9, with a space of 3^a
	seed := int64(2365)
	lists := make([]list, 0, 10)
	space := int64(1)
	for a := 0; a < 10; a++ {
		kinds := min(int64(1)<<(2*(a/2+1)), 100000)
		types := make([]int64, kinds)
		for k := range types {
			types[k] = 1 + wideRandom(&seed)%1000000000
		}
		tasks := make([]int64, 100000)
		for i := range tasks {
			tasks[i] = types[wideRandom(&seed)%kinds]
		}
		lists = append(lists, list{tasks, space})
		space *= 3
	}
	check := int64(0)
	for p := int64(0); p < 20; p++ {
		for _, l := range lists {
			check = (check*31 + taskSchedulerII(l.tasks, l.space)%1000000007 + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 lists of 10^5 tasks: checksum %d\n", check)
}
