// LeetCode #2443: Sum of Number and Its Reverse -- the bench, the ★ arm:
// every `k` from 0 to `num` tried, its digits reversed by `% 10` and
// `/ 10`.
package main

import "fmt"

func reversed(x int64) int64 {
	var r int64
	for y := x; y > 0; y /= 10 {
		r = r*10 + y%10
	}
	return r
}

func sumOfNumberAndReverse(num int64) bool {
	for k := int64(0); k <= num; k++ {
		if k+reversed(k) == num {
			return true
		}
	}
	return false
}

var seed int64 = 2443

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for i := int64(0); i < 400; i++ {
		a := nextRandom()
		num := 90000 + (a*32768+nextRandom())%10001
		var verdict int64
		if sumOfNumberAndReverse(num) {
			verdict = 1
		}
		check = (check*31 + num*2 + verdict + i) % 1000000007
	}
	fmt.Printf("400 nums near 10^5: checksum %d\n", check)
}
