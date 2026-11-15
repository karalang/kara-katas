// LeetCode #2180: Count Integers With Even Digit Sum -- the benchmark's
// Go mirror of even_digits.kara.
package main

import "fmt"

func countEven(num int64) int64 {
	var count int64
	for x := int64(1); x <= num; x++ {
		var total int64
		rest := x
		for rest > 0 {
			total += rest % 10
			rest /= 10
		}
		if total%2 == 0 {
			count++
		}
	}
	return count
}

var seed int64 = 2180

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for r := 0; r < 200000; r++ {
		num := nextRandom()%1000 + 1
		check = (check*31 + countEven(num)) % 1000000007
	}
	fmt.Printf("200000 solves: checksum %d\n", check)
}
