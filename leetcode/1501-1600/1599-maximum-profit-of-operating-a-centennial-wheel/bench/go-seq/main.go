// LeetCode #1599: Maximum Profit of Operating a Centennial Wheel
// -- the bench in Go, mirroring wheel.kara: the wheel run rotation by
// rotation in int64, on 300 days of 100000 arrivals, all drawn first.
package main

import "fmt"

func minOperationsMaxProfit(customers []int32, boardingCost, runningCost int32) int32 {
	var waiting, profit, best, rotations int64
	var answer int32 = -1
	n := int64(len(customers))
	for rotations < n || waiting > 0 {
		if rotations < n {
			waiting += int64(customers[rotations])
		}
		board := min(waiting, 4)
		waiting -= board
		profit += board*int64(boardingCost) - int64(runningCost)
		rotations++
		if profit > best {
			best = profit
			answer = int32(rotations)
		}
	}
	return answer
}

var seed int64 = 1599

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type day struct {
	customers         []int32
	boarding, running int32
}

func main() {
	days := make([]day, 300)
	for d := range days {
		c := make([]int32, 100000)
		for i := range c {
			c[i] = int32(nextRandom() % 9)
		}
		b := int32(nextRandom()%100 + 1)
		r := int32(nextRandom()%100 + 1)
		days[d] = day{c, b, r}
	}
	var check int64
	for _, d := range days {
		answer := minOperationsMaxProfit(d.customers, d.boarding, d.running)
		check = (check*31 + int64(answer) + 1) % 1000000007
	}
	fmt.Printf("300 days of 100000 arrivals: checksum %d\n", check)
}
