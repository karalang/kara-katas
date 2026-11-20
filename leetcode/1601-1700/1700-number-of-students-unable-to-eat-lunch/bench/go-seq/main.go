// LeetCode #1700: Number of Students Unable to Eat Lunch -- the bench's Go
// mirror: the ★ arm on 50000 random lunches of 100 students, all drawn
// first, each answered 80 times.
package main

import "fmt"

func countStudents(students, sandwiches []int32) int32 {
	wanting := [2]int32{}
	for _, s := range students {
		wanting[s]++
	}
	for _, s := range sandwiches {
		if wanting[s] == 0 {
			break
		}
		wanting[s]--
	}
	return wanting[0] + wanting[1]
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1700

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 50000, 80, 100
	students := make([][]int32, count)
	sandwiches := make([][]int32, count)
	for c := 0; c < count; c++ {
		lean := nextRandom() % 11
		students[c] = make([]int32, n)
		sandwiches[c] = make([]int32, n)
		for i := range students[c] {
			if nextRandom()%10 < lean {
				students[c][i] = 1
			}
		}
		for i := range sandwiches[c] {
			if nextRandom()%10 < lean {
				sandwiches[c][i] = 1
			}
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			answer := int64(countStudents(students[c], sandwiches[c]))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d lunches of %d students, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, total, check)
}
