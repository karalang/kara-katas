// LeetCode #2836: Maximize Value of Function in a Ball Passing Game --
// the bench, mirrored from ball.kara: binary lifting over 34 levels.
package main

import "fmt"

const levels = 34

func getMaxFunctionValue(receiver []int64, k int64) int64 {
	n := len(receiver)
	jump := [][]int64{append([]int64(nil), receiver...)}
	gain := [][]int64{append([]int64(nil), receiver...)}
	for j := 1; j < levels; j++ {
		pj, pg := jump[j-1], gain[j-1]
		next := make([]int64, n)
		sum := make([]int64, n)
		for i := 0; i < n; i++ {
			next[i] = pj[pj[i]]
		}
		for i := 0; i < n; i++ {
			sum[i] = pg[i] + pg[pj[i]]
		}
		jump = append(jump, next)
		gain = append(gain, sum)
	}
	var best int64
	for start := 0; start < n; start++ {
		at := int64(start)
		total := int64(start)
		for j := 0; j < levels; j++ {
			if (k>>j)&1 == 1 {
				total += gain[j][at]
				at = jump[j][at]
			}
		}
		if total > best {
			best = total
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

type game struct {
	receiver []int64
	k        int64
}

func main() {
	const count, rounds, n = 10, 3, 100000
	seed := int64(2836)
	games := make([]game, 0, count)
	for c := 0; c < count; c++ {
		receiver := make([]int64, n)
		for i := range receiver {
			receiver[i] = wide(&seed) % n
		}
		w := wide(&seed)
		k := (w*10+nextRandom(&seed))%10000000000 + 1
		games = append(games, game{receiver, k})
	}
	var check int64
	for r := int64(0); r < rounds; r++ {
		for _, g := range games {
			best := getMaxFunctionValue(g.receiver, g.k)
			check = (check*31 + best%1000000007 + r) % 1000000007
		}
	}
	fmt.Printf("%d games of %d, %d rounds: checksum %d\n", count, n, rounds, check)
}
