// LeetCode #2048 -- the ★ arm as a benchmark; mirror of ../beautiful.kara.
package main

import "fmt"

func isBalanced(x int64) bool {
	var counts [10]int64
	for y := x; y > 0; y /= 10 {
		counts[y%10]++
	}
	for d := int64(0); d < 10; d++ {
		if counts[d] != 0 && counts[d] != d {
			return false
		}
	}
	return true
}

func nextBeautifulNumber(n int64) int64 {
	x := n + 1
	for !isBalanced(x) {
		x++
	}
	return x
}

func main() {
	var calls, sum, check int64
	for k := int64(0); k < 1000; k++ {
		x := nextBeautifulNumber(k*1000 + k*7%1000)
		calls++
		sum += x
		check = (check*31 + x) % 1000000007
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
