// Benchmark: LeetCode #986 Interval List Intersections -- the ★ arm, two pointers,
// on pairs of LeetCode's largest lists, 1000 intervals each.
// Mirrors ../interval_intersection.kara, .rs, .c and .py.
package main

import "fmt"

func intervalIntersection(first, second [][2]int64) [][2]int64 {
	var out [][2]int64
	i, j := 0, 0
	for i < len(first) && j < len(second) {
		lo := max(first[i][0], second[j][0])
		hi := min(first[i][1], second[j][1])
		if lo <= hi {
			out = append(out, [2]int64{lo, hi})
		}
		if first[i][1] < second[j][1] {
			i++
		} else {
			j++
		}
	}
	return out
}

var seed int64 = 986

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func randomList() [][2]int64 {
	var out [][2]int64
	pos := wideRandom() % 499999
	for k := 0; k < 1000; k++ {
		start := pos
		end := start + 1 + wideRandom()%499999
		out = append(out, [2]int64{start, end})
		pos = end + 1 + wideRandom()%499999
	}
	return out
}

func main() {
	rounds := 1000
	var lists [][][2]int64
	for k := 0; k < 21; k++ {
		lists = append(lists, randomList())
	}
	var found, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			k := (r + i) % 20
			answer := intervalIntersection(lists[k], lists[k+1])
			found += int64(len(answer))
			m := answer[len(answer)/2]
			check = (check*31 + int64(len(answer)) + m[0]%1000 + m[1]%1000) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 pairs of 1000 intervals: %d intersections, checksum %d\n", rounds, found, check)
}
