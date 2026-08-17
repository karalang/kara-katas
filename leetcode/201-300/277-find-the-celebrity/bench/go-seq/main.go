// LeetCode 277 bench mirror — Go. Same algorithm as celebrity.kara.
package main

import "fmt"

const N = 2500000
const Instances = 64

func knows(star, a, b int64) bool {
	if b == star {
		return true
	}
	if a == star {
		return false
	}
	h := (a*1103515245 + b*12345) % 2147483647
	return h%2 == 0
}

func findCelebrity(n, star int64) int64 {
	var cand int64
	for i := int64(1); i < n; i++ {
		if knows(star, cand, i) {
			cand = i
		}
	}
	for j := int64(0); j < n; j++ {
		if j != cand {
			if knows(star, cand, j) {
				return -1
			}
			if !knows(star, j, cand) {
				return -1
			}
		}
	}
	return cand
}

func main() {
	var sink int64
	for i := int64(0); i < Instances; i++ {
		star := (i * 7919) % N
		sink = (sink + (i*1000003+findCelebrity(N, star))%1000000007) % 1000000007
	}
	fmt.Println(sink)
}
