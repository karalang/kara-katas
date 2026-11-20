// LeetCode #1201 bench: the ★ arm in Go, over the same 50000 queries and
// 10 rounds as the Kāra bench.
package main

import "fmt"

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func lcm(a, b int64) int64 { return a / gcd(a, b) * b }

func nthUglyNumber(n, a, b, c int64) int64 {
	ab, bc, ac := lcm(a, b), lcm(b, c), lcm(a, c)
	abc := lcm(ab, c)
	count := func(x int64) int64 { return x/a + x/b + x/c - x/ab - x/bc - x/ac + x/abc }
	low, high := int64(1), n*min(a, b, c)
	for low < high {
		mid := low + (high-low)/2
		if count(mid) >= n {
			high = mid
		} else {
			low = mid + 1
		}
	}
	return low
}

var seed int64 = 1201

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func big() int64 {
	high := nextRandom()
	low := nextRandom()
	return high*32768 + low
}

func main() {
	tops := [3]int64{1000000, 1000, 30}
	queries := make([][4]int64, 0, 50000)
	for k := 0; k < 50000; k++ {
		top := tops[k%3]
		a := big()%top + 1
		b := big()%top + 1
		c := big()%top + 1
		most := min(2000000000/min(a, b, c), 1000000000)
		n := big()%most + 1
		queries = append(queries, [4]int64{n, a, b, c})
	}
	var check int64
	for r := 0; r < 10; r++ {
		for _, q := range queries {
			check = (check*131 + nthUglyNumber(q[0], q[1], q[2], q[3])) % 1000000007
		}
	}
	fmt.Printf("10 rounds of 50000 queries: checksum %d\n", check)
}
