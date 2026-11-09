// LeetCode #2050: Parallel Courses III -- Go mirror of the ★ arm's
// benchmark (courses.kara): the same 40 graphs of 50000 courses, the same
// Kahn's topological order, the queue a slice taken from the front.
package main

import "fmt"

var seed int64 = 2050

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func minimumTime(n int, relations [][2]int, time []int64) int64 {
	next := make([][]int, n)
	waiting := make([]int64, n)
	for _, r := range relations {
		next[r[0]-1] = append(next[r[0]-1], r[1]-1)
		waiting[r[1]-1]++
	}
	start := make([]int64, n)
	queue := []int{}
	for v := 0; v < n; v++ {
		if waiting[v] == 0 {
			queue = append(queue, v)
		}
	}
	var months int64
	for len(queue) > 0 {
		v := queue[0]
		queue = queue[1:]
		done := start[v] + time[v]
		if done > months {
			months = done
		}
		for _, w := range next[v] {
			if done > start[w] {
				start[w] = done
			}
			waiting[w]--
			if waiting[w] == 0 {
				queue = append(queue, w)
			}
		}
	}
	return months
}

func main() {
	n := 50000
	var sum, check int64
	for t := int64(0); t < 40; t++ {
		reach := 1 + t*1000
		order := make([]int, n)
		for i := range order {
			order[i] = i + 1
		}
		for i := n - 1; i >= 1; i-- {
			j := int(nextRandom() % int64(i+1))
			order[i], order[j] = order[j], order[i]
		}
		relations := make([][2]int, 0, n-1)
		for i := 1; i < n; i++ {
			span := reach
			if int64(i) < span {
				span = int64(i)
			}
			at := i - int(nextRandom()%span+1)
			relations = append(relations, [2]int{order[at], order[i]})
		}
		time := make([]int64, n)
		for v := range time {
			time[v] = nextRandom()%10000 + 1
		}
		months := minimumTime(n, relations, time)
		sum += months
		check = (check*31 + months) % 1000000007
	}
	fmt.Printf("40 graphs: sum %d, checksum %d\n", sum, check)
}
