// LeetCode #739: Daily Temperatures -- a stack of colder days.
// Benchmark mirror of the Kara star arm: walk the days keeping a stack
// of the days still waiting; a day warmer than the top answers it, and
// every day under it that it is warmer than, and then waits itself.
package main

import "fmt"

func dailyTemperatures(temperatures []int64) []int64 {
	n := len(temperatures)
	var answer []int64
	for i := 0; i < n; i++ {
		answer = append(answer, 0)
	}
	var waiting []int
	for i := 0; i < n; i++ {
		for len(waiting) > 0 && temperatures[waiting[len(waiting)-1]] < temperatures[i] {
			j := waiting[len(waiting)-1]
			waiting = waiting[:len(waiting)-1]
			answer[j] = int64(i - j)
		}
		waiting = append(waiting, i)
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(739)
	n := int64(100000)
	t := make([]int64, 0)
	for i := int64(0); i < n; i++ {
		t = append(t, 30+nextRandom(&seed)%71)
	}
	var total int64
	for r := 0; r < 300; r++ {
		for k := 0; k < 100; k++ {
			a := nextRandom(&seed)
			b := nextRandom(&seed)
			j := (a*32768 + b) % n
			t[j] = 30 + nextRandom(&seed)%71
		}
		answer := dailyTemperatures(t)
		for _, a := range answer {
			total += a
		}
	}
	fmt.Printf("300 rounds of 100000 days: %d days waited in all\n", total)
}
