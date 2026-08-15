// LeetCode 276 bench mirror — brute-force enumeration, Go.
// Same algorithm as paint_enum.kara; sequential over the 16 prefixes.
package main

import "fmt"

const N = 13
const K = 4

func countPrefix(p0, p1 int64) int64 {
	var c [N]int64
	c[0] = p0
	c[1] = p1
	var count int64
	for {
		ok := true
		for i := 2; i < N; i++ {
			if c[i] == c[i-1] && c[i-1] == c[i-2] {
				ok = false
			}
		}
		if ok {
			count++
		}
		p := N - 1
		for p >= 2 && c[p] == K-1 {
			c[p] = 0
			p--
		}
		if p < 2 {
			break
		}
		c[p]++
	}
	return count
}

func main() {
	var total int64
	for pre := int64(0); pre < K*K; pre++ {
		total += countPrefix(pre/K, pre%K)
	}
	fmt.Println(total)
}
