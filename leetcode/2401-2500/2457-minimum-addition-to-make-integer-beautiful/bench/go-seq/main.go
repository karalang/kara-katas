// LeetCode #2457: Minimum Addition to Make Integer Beautiful -- bench, Go
// mirror of beautiful.kara: while the digit sum is too large, n + x is
// rounded up to the next multiple of a power of ten one place higher.
package main

import "fmt"

func digitSum(x int64) int64 {
	var sum int64
	for x > 0 {
		sum += x % 10
		x /= 10
	}
	return sum
}

func makeIntegerBeautiful(n, target int64) int64 {
	m, p := n, int64(1)
	for digitSum(m) > target {
		p *= 10
		m = (m + p - 1) / p * p
	}
	return m - n
}

var seed int64 = 2457

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	ns := make([]int64, 100000)
	ts := make([]int64, 100000)
	for i := range ns {
		a := nextRandom()
		b := nextRandom()
		ns[i] = 1 + (a*1073741824+b*32768+nextRandom())%1000000000000
		ts[i] = nextRandom() % 150
	}
	var check int64
	for p := int64(0); p < 36; p++ {
		for i := range ns {
			check = (check*31 + makeIntegerBeautiful(ns[i], 1+(ts[i]+p)%150) + p) % 1000000007
		}
	}
	fmt.Printf("36 passes over 10^5 pairs: checksum %d\n", check)
}
