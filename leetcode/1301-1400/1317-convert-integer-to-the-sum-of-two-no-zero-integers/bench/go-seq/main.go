// LeetCode #1317 bench, Go mirror of the Kāra bench: the ★ arm (the first
// number tried from 1 up, each pair's digits read off by `% 10` and `/ 10`,
// until neither has a 0) on every n from 2 to 10^4; 300 passes, each
// starting its walk through the range at a place chosen by the checksum so
// far and folding both numbers of every answer into it.
package main

import "fmt"

func hasZero(x int64) bool {
	rest := x
	for rest > 0 {
		if rest%10 == 0 {
			return true
		}
		rest /= 10
	}
	return false
}

func getNoZeroIntegers(n int64) []int64 {
	a := int64(1)
	for hasZero(a) || hasZero(n-a) {
		a++
	}
	return []int64{a, n - a}
}

func main() {
	var check int64
	for pass := int64(0); pass < 300; pass++ {
		start := check % 9999
		for k := int64(0); k < 9999; k++ {
			n := 2 + (start+k)%9999
			v := getNoZeroIntegers(n)
			check = (check*31 + v[0]*7 + v[1] + pass) % 1000000007
		}
	}
	fmt.Printf("300 passes over every n from 2 to 10^4: checksum %d\n", check)
}
