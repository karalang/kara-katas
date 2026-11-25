// LeetCode #1375 bench -- Go: the ★ arm: after step i the string is
// aligned exactly when the largest bit flipped so far is i.
package main

import "fmt"

func numTimesAllBlue(flips []int32) int {
	var largest int32
	aligned := 0
	for i, f := range flips {
		largest = max(largest, f)
		if int(largest) == i+1 {
			aligned++
		}
	}
	return aligned
}

var seed int64 = 1375

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 orders of 5 * 10^4 bits, the constraints' most, 1 to n shuffled
	// within runs of 2 to 8, built once; then 1000 rounds, each trading
	// two neighbouring flips of one order, both drawn from the checksum
	// so far, and counting that order's aligned steps
	const n = 50000
	orders := make([][]int32, 0, 20)
	for o := 0; o < 20; o++ {
		flips := make([]int32, n)
		for v := range flips {
			flips[v] = int32(v + 1)
		}
		var start int64
		for start < n {
			end := min(start+2+nextRandom()%7, n)
			for i := end - 1; i > start; i-- {
				j := start + nextRandom()%(i-start+1)
				flips[i], flips[j] = flips[j], flips[i]
			}
			start = end
		}
		orders = append(orders, flips)
	}
	var check int64
	for r := int64(0); r < 1000; r++ {
		flips := orders[check%20]
		k := (check / 20) % (n - 1)
		flips[k], flips[k+1] = flips[k+1], flips[k]
		got := int64(numTimesAllBlue(flips))
		check = (check*31 + got + r) % 1000000007
	}
	fmt.Printf("1000 rounds over 20 orders of 50000 bits: checksum %d\n", check)
}
