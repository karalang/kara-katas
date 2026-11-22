// LeetCode #2895: Minimum Processing Time -- the bench, as
// processing.kara: 20 cases of 25000 processors and 10^5 tasks, each
// answered 20 times by the sorting arm, each sorting fresh copies.
package main

import (
	"fmt"
	"slices"
)

func minProcessingTime(processorTime, tasks []int64) int64 {
	free := slices.Clone(processorTime)
	slices.Sort(free)
	longest := slices.Clone(tasks)
	slices.Sort(longest)
	slices.Reverse(longest)
	var finish int64
	for i, p := range free {
		finish = max(finish, p+longest[4*i])
	}
	return finish
}

var seed int64 = 2895

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 20, 20, 25000
	processors := make([][]int64, count)
	tasks := make([][]int64, count)
	for c := 0; c < count; c++ {
		processors[c] = make([]int64, n)
		for i := range processors[c] {
			processors[c][i] = wide() % 1000000000
		}
		tasks[c] = make([]int64, 4*n)
		for i := range tasks[c] {
			tasks[c][i] = wide()%1000000000 + 1
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			time := minProcessingTime(processors[c], tasks[c])
			total += time
			check = (check*31 + time + r) % 1000000007
		}
	}
	fmt.Printf("%d cases of %d, %d rounds: times total %d, checksum %d\n", count, n, rounds, total, check)
}
