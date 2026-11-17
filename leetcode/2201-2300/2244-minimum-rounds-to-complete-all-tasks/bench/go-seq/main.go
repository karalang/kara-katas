// LeetCode #2244: Minimum Rounds to Complete All Tasks -- the benchmark's
// Go mirror of rounds.kara: the tasks of each difficulty counted in a
// map; a lone task gives -1, any other count c takes ceil(c / 3) rounds,
// summed.
package main

import "fmt"

func minimumRounds(tasks []int64) int64 {
	counts := map[int64]int64{}
	for _, t := range tasks {
		counts[t]++
	}
	rounds := int64(0)
	for _, c := range counts {
		if c == 1 {
			return -1
		}
		rounds += (c + 2) / 3
	}
	return rounds
}

var seed int64 = 2244

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	check := int64(0)
	for l := 0; l < 40; l++ {
		kinds := make([]int64, 30000)
		for i := range kinds {
			kinds[i] = wideRandom()%1000000000 + 1
		}
		tasks := make([]int64, 0, 100000)
		for i := 0; i < 50000; i++ {
			t := kinds[wideRandom()%30000]
			tasks = append(tasks, t, t)
		}
		check = (check*31 + minimumRounds(tasks) + 1) % 1000000007
	}
	fmt.Printf("40 lists of 100000 tasks: checksum %d\n", check)
}
