// LeetCode #2513: Minimize the Maximum of Two Arrays -- Go mirror of the
// benchmark (minimize.kara): the same cases, passes and checksum.
package main

import "fmt"

func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func minimizeSet(d1, d2, c1, c2 int64) int64 {
	lcm := d1 / gcd(d1, d2) * d2
	lo, hi := int64(1), 2*(c1+c2)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if mid-mid/d1 >= c1 && mid-mid/d2 >= c2 && mid-mid/lcm >= c1+c2 {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

var seed int64 = 2513

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func below(top int64) int64 {
	hi := nextRandom()
	return (hi*32768 + nextRandom()) % top
}

func main() {
	cases := make([][4]int64, 100000)
	for i := range cases {
		cases[i][0] = below(99999) + 2
		cases[i][1] = below(99999) + 2
		cases[i][2] = below(999998999) + 1
		cases[i][3] = below(999999000-cases[i][2]) + 1
	}
	const passes = 10
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, c := range cases {
			check = (check*31 + minimizeSet(c[0], c[1], c[2]+check%1000, c[3]) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 10^5 cases: checksum %d\n", passes, check)
}
