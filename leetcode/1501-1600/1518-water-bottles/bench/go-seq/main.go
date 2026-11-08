// LeetCode #1518 bench: the ★ arm (whole lots a round), as bottles.kara.
package main

import "fmt"

func numWaterBottles(numBottles, numExchange int64) int64 {
	var drunk, empty int64
	full := numBottles
	for full > 0 {
		drunk += full
		empty += full
		full = empty / numExchange
		empty %= numExchange
	}
	return drunk
}

func main() {
	var check int64
	for i := int64(0); i < 20000000; i++ {
		bottles := i*7919%1000000000 + 1
		exchange := i%99 + 2
		check = (check*31 + numWaterBottles(bottles, exchange) + 1) % 1000000007
	}
	fmt.Printf("20000000 questions up to 10^9 bottles and 2 to 100 for 1: checksum %d\n", check)
}
