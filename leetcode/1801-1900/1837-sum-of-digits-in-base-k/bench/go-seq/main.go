// LeetCode #1837: Sum of Digits in Base K -- the bench in Go: the ★ arm over
// 2 * 10^7 calls, each `n` from 1 to 100 and base from 2 to 10 drawn from the
// checksum so far.
package main

import "fmt"

func sumBase(n, k int64) int64 {
	left := n
	var sum int64
	for left > 0 {
		sum += left % k
		left /= k
	}
	return sum
}

func main() {
	var check int64
	for call := int64(0); call < 20000000; call++ {
		n := 1 + (check+call)%100
		k := 2 + (check/100+call)%9
		check = (check*31 + sumBase(n, k)) % 1000000007
	}
	fmt.Printf("20000000 calls: checksum %d\n", check)
}
