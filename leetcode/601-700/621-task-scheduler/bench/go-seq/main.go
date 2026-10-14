// LeetCode #621: Task Scheduler -- Go mirror of the Kāra bench.
//
// The ★ arm's frame count over the same lists and rounds; a task is a
// `rune`.
package main

import "fmt"

func leastInterval(tasks []rune, n int64) int64 {
	var counts [26]int64
	for _, t := range tasks {
		counts[t-'A']++
	}
	var most int64
	for _, c := range counts {
		if c > most {
			most = c
		}
	}
	var tied int64
	for _, c := range counts {
		if c == most {
			tied++
		}
	}
	frame := (most-1)*(n+1) + tied
	if frame > int64(len(tasks)) {
		return frame
	}
	return int64(len(tasks))
}

var seed int64 = 621

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTasks(size, kinds int64, skew bool) []rune {
	tasks := make([]rune, 0, size)
	weight := kinds
	if skew {
		weight = kinds * (kinds + 1) / 2
	}
	for i := int64(0); i < size; i++ {
		r := nextRandom() % weight
		var k int64
		if skew {
			for r > k {
				r -= k + 1
				k++
			}
		} else {
			k = r
		}
		tasks = append(tasks, rune(65+k))
	}
	return tasks
}

func main() {
	const lists = 100
	const rounds = 30000
	all := make([][]rune, 0, lists)
	for i := 0; i < lists; i++ {
		kinds := 1 + nextRandom()%26
		all = append(all, randomTasks(10000, kinds, i%2 == 0))
	}
	var sum, checksum int64
	for r := int64(0); r < rounds; r++ {
		answer := leastInterval(all[(r*7)%lists], r%101)
		sum += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d lists, %d rounds: total %d, checksum %d\n", lists, rounds, sum, checksum)
}
