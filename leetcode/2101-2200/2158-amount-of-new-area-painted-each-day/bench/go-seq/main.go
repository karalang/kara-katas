// LeetCode #2158: Amount of New Area Painted Each Day -- the benchmark's Go
// mirror of painted.kara.
package main

import "fmt"

func firstUnpainted(next []int64, x int64) int64 {
	for next[x] != x {
		next[x] = next[next[x]]
		x = next[x]
	}
	return x
}

func amountPainted(paint [][2]int64) []int64 {
	var wall int64
	for _, p := range paint {
		if p[1] > wall {
			wall = p[1]
		}
	}
	next := make([]int64, wall+1)
	for x := range next {
		next[x] = int64(x)
	}
	log := make([]int64, 0, len(paint))
	for _, p := range paint {
		var painted int64
		x := firstUnpainted(next, p[0])
		for x < p[1] {
			painted++
			next[x] = x + 1
			x = firstUnpainted(next, x+1)
		}
		log = append(log, painted)
	}
	return log
}

var seed int64 = 2158

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func segment() [2]int64 {
	length := wideRandom()%500 + 1
	start := wideRandom() % (50000 - length + 1)
	return [2]int64{start, start + length}
}

func main() {
	lists := make([][][2]int64, 4)
	for l := range lists {
		lists[l] = make([][2]int64, 100000)
		for i := range lists[l] {
			lists[l][i] = segment()
		}
	}
	var total, check int64
	for round := int64(0); round < 5; round++ {
		for l := 0; l < 4; l++ {
			at := wideRandom() % 100000
			lists[l][at] = segment()
			log := amountPainted(lists[l])
			for day, a := range log {
				total += a
				check = (check*31 + a*int64(day+1) + round) % 1000000007
			}
		}
	}
	fmt.Printf("20 solves: %d units in all, checksum %d\n", total, check)
}
