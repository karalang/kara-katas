package main

import "fmt"

func sqDigitSum(n int64) int64 {
	var total int64 = 0
	x := n
	for x > 0 {
		d := x % 10
		total += d * d
		x /= 10
	}
	return total
}

func isHappy(n int64) bool {
	slow := n
	fast := sqDigitSum(n)
	for fast != 1 && slow != fast {
		slow = sqDigitSum(slow)
		fast = sqDigitSum(sqDigitSum(fast))
	}
	return fast == 1
}

func main() {
	var limit int64 = 4000000
	var sink int64 = 0
	for i := int64(1); i < limit; i++ {
		if isHappy(i) {
			sink += 1
		}
	}
	fmt.Println(sink)
}
