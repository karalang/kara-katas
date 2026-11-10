// LeetCode #2100: Find Good Days to Rob the Bank -- Go mirror of the ★
// arm's benchmark (good_days.kara): the same 100 schedules of 10^5 days,
// the two runs counted in two passes.
package main

import "fmt"

func goodDaysToRobBank(security []int64, time int64) []int64 {
	n := len(security)
	before := make([]int64, n)
	after := make([]int64, n)
	for i := 1; i < n; i++ {
		if security[i] <= security[i-1] {
			before[i] = before[i-1] + 1
		}
	}
	for i := n - 2; i >= 0; i-- {
		if security[i] <= security[i+1] {
			after[i] = after[i+1] + 1
		}
	}
	var good []int64
	for i := 0; i < n; i++ {
		if before[i] >= time && after[i] >= time {
			good = append(good, int64(i))
		}
	}
	return good
}

var seed int64 = 2100

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	total := 0
	var check int64
	for r := 0; r < 100; r++ {
		guards := int64(50000)
		security := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			guards += nextRandom()%3 - 1
			if guards < 0 {
				guards = 0
			}
			if guards > 100000 {
				guards = 100000
			}
			security = append(security, guards)
		}
		time := nextRandom() % 8
		good := goodDaysToRobBank(security, time)
		total += len(good)
		for _, d := range good {
			check = (check*31 + d + 1) % 1000000007
		}
	}
	fmt.Printf("100 answers: %d good days, checksum %d\n", total, check)
}
