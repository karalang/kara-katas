// LeetCode #1467 bench in Go: the ★ arm (a depth-first search over how
// many of each colour go into the first box) on the same 100 sets of 8
// colours and 2 passes.
package main

import (
	"fmt"
	"math"
)

func choose(n, k int64) int64 {
	c := int64(1)
	for i := int64(0); i < k; i++ {
		c = c * (n - i) / (i + 1)
	}
	return c
}

func ways(balls []int32, i int, first, a, b int64) int64 {
	if i == len(balls) {
		if first == 0 && a == b {
			return 1
		}
		return 0
	}
	n := int64(balls[i])
	var total int64
	for j := int64(0); j <= min(n, first); j++ {
		a2, b2 := a, b
		if j > 0 {
			a2++
		}
		if j < n {
			b2++
		}
		total += choose(n, j) * ways(balls, i+1, first-j, a2, b2)
	}
	return total
}

func getProbability(balls []int32) float64 {
	var total int64
	for _, b := range balls {
		total += int64(b)
	}
	good := ways(balls, 0, total/2, 0, 0)
	return float64(good) / float64(choose(total, total/2))
}

var seed int64 = 1467

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var sets [][]int32
	for len(sets) < 100 {
		balls := make([]int32, 8)
		var sum int32
		for i := range balls {
			balls[i] = int32(1 + nextRandom()%6)
			sum += balls[i]
		}
		if sum%2 == 0 {
			sets = append(sets, balls)
		}
	}
	var check int64
	for pass := int64(0); pass < 2; pass++ {
		for s := 0; s < 100; s++ {
			k := check % 8
			if sets[s][k] <= 4 {
				sets[s][k] += 2
			} else {
				sets[s][k] -= 2
			}
			p := getProbability(sets[s])
			check = (check*31 + int64(math.Floor(p*1000000000.0+0.5)) + pass) % 1000000007
		}
	}
	fmt.Printf("2 passes over 100 sets of 8 colours: checksum %d\n", check)
}
