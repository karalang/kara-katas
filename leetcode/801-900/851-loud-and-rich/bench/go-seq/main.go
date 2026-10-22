// Benchmark for #851: Loud and Rich -- Go twin of the Kāra ★ arm (memoised
// search up the richer-than graph).
package main

import "fmt"

func answerFor(x int64, richerThan [][]int64, quiet []int64, answer []int64) int64 {
	if answer[x] < 0 {
		best := x
		for _, y := range richerThan[x] {
			candidate := answerFor(y, richerThan, quiet, answer)
			if quiet[candidate] < quiet[best] {
				best = candidate
			}
		}
		answer[x] = best
	}
	return answer[x]
}

func loudAndRich(richer [][2]int64, quiet []int64) []int64 {
	n := len(quiet)
	richerThan := make([][]int64, 0, n)
	for i := 0; i < n; i++ {
		richerThan = append(richerThan, nil)
	}
	for _, pair := range richer {
		richerThan[pair[1]] = append(richerThan[pair[1]], pair[0])
	}
	answer := make([]int64, n)
	for x := range answer {
		answer[x] = -1
	}
	for x := 0; x < n; x++ {
		answerFor(int64(x), richerThan, quiet, answer)
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 64, 10000, 500
	var seed int64 = 851
	richers := make([][][2]int64, 0, count)
	quiets := make([][]int64, 0, count)
	for g := 0; g < count; g++ {
		odds := int64(2) << (g % 8)
		rank := make([]int64, n)
		for i := range rank {
			rank[i] = int64(i)
		}
		for i := n - 1; i >= 1; i-- {
			j := nextRandom(&seed) % int64(i+1)
			rank[i], rank[j] = rank[j], rank[i]
		}
		var richer [][2]int64
		for i := 0; i < n; i++ {
			for j := i + 1; j < n; j++ {
				if nextRandom(&seed)%1000 < odds {
					richer = append(richer, [2]int64{rank[i], rank[j]})
				}
			}
		}
		quiet := make([]int64, n)
		for i := range quiet {
			quiet[i] = int64(i)
		}
		for i := n - 1; i >= 1; i-- {
			j := nextRandom(&seed) % int64(i+1)
			quiet[i], quiet[j] = quiet[j], quiet[i]
		}
		richers = append(richers, richer)
		quiets = append(quiets, quiet)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		g := round % count
		answer := loudAndRich(richers[g], quiets[g])
		for _, a := range answer {
			total += quiets[g][a]
			checksum = (checksum*31 + a) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d cases: quietness sums to %d, checksum %d\n", rounds, count, total, checksum)
}
