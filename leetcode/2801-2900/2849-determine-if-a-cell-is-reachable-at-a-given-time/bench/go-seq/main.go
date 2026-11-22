// LeetCode #2849: Determine if a Cell Is Reachable at a Given Time --
// the bench: the ★ arm over 10^6 random cases on LeetCode's grid, the
// finish within 3 of the start and t within 2 of the distance, all
// drawn first, then each answered 20 times.
package main

import "fmt"

type cell struct{ sx, sy, fx, fy, t int64 }

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func isReachableAtTime(sx, sy, fx, fy, t int64) bool {
	if sx == fx && sy == fy {
		return t != 1
	}
	return max(abs(sx-fx), abs(sy-fy)) <= t
}

var seed int64 = 2849

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 1000000, 20
	cases := make([]cell, 0, count)
	for i := 0; i < count; i++ {
		sx := nextRandom()*30000%1000000000 + 1
		sy := nextRandom()*30000%1000000000 + 1
		fx := min(max(sx+nextRandom()%7-3, 1), 1000000000)
		fy := sy
		if nextRandom()%2 != 0 {
			fy = min(max(sy+nextRandom()%7-3, 1), 1000000000)
		}
		d := max(abs(sx-fx), abs(sy-fy))
		t := max(d+nextRandom()%5-2, 0)
		cases = append(cases, cell{sx, sy, fx, fy, t})
	}
	var yes, check int64
	for r := int64(0); r < rounds; r++ {
		for _, c := range cases {
			ok := isReachableAtTime(c.sx, c.sy, c.fx, c.fy, c.t)
			add := int64(1)
			if ok {
				yes++
				add = 2
			}
			check = (check*3 + add + r) % 1000000007
		}
	}
	fmt.Printf("%d cases, %d rounds: %d true, checksum %d\n", count, rounds, yes, check)
}
