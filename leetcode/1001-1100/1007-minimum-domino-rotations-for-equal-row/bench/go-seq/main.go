// Benchmark: LeetCode #1007 Minimum Domino Rotations For Equal Row -- the
// ★ arm, two candidates, on rows of 20000 dominoes, LeetCode's longest.
// Mirrors min_rotations.kara, .c, .rs and .py.
package main

import "fmt"

func rotations(tops, bottoms []int64, v int64) int64 {
	toTop, toBottom := int64(0), int64(0)
	for i := range tops {
		if tops[i] != v && bottoms[i] != v {
			return -1
		}
		if tops[i] != v {
			toTop++
		} else if bottoms[i] != v {
			toBottom++
		}
	}
	if toTop < toBottom {
		return toTop
	}
	return toBottom
}

func minDominoRotations(tops, bottoms []int64) int64 {
	a := rotations(tops, bottoms, tops[0])
	b := rotations(tops, bottoms, bottoms[0])
	if a == -1 {
		return b
	}
	if b == -1 {
		return a
	}
	if a < b {
		return a
	}
	return b
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	rounds := int64(400)
	n := int64(20000)
	seed := int64(1007)
	allTops := make([][]int64, 0, 20)
	allBottoms := make([][]int64, 0, 20)
	for t := int64(0); t < 20; t++ {
		target := t%6 + 1
		tops := make([]int64, 0, n)
		bottoms := make([]int64, 0, n)
		for j := int64(0); j < n; j++ {
			top := 1 + nextRandom(&seed)%6
			bottom := 1 + nextRandom(&seed)%6
			if t%2 == 0 || nextRandom(&seed)%2000 != 0 {
				if nextRandom(&seed)%2 == 0 {
					top = target
				} else {
					bottom = target
				}
			}
			tops = append(tops, top)
			bottoms = append(bottoms, bottom)
		}
		allTops = append(allTops, tops)
		allBottoms = append(allBottoms, bottoms)
	}
	total := int64(0)
	check := int64(0)
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < 20; i++ {
			t := (r + i) % 20
			got := minDominoRotations(allTops[t], allBottoms[t])
			total += got
			check = (check*31 + got + 2) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 rows of %d dominoes: answers sum to %d, checksum %d\n", rounds, n, total, check)
}
