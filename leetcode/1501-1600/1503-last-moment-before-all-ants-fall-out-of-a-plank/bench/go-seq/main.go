// LeetCode #1503: Last Moment Before All Ants Fall Out of a Plank -- the
// benchmark, the same algorithm as ants.kara: the statement simulated with
// doubled positions and half-unit ticks.
package main

import "fmt"

func lastMoment(n int64, left, right []int64) int64 {
	pos := []int64{}
	dir := []int64{}
	for _, p := range left {
		pos = append(pos, 2*p)
		dir = append(dir, -1)
	}
	for _, p := range right {
		pos = append(pos, 2*p)
		dir = append(dir, 1)
	}
	on := make([]bool, len(pos))
	for i := range on {
		on[i] = true
	}
	alive := len(pos)
	at := make([]int64, 2*n+1)
	for i := range at {
		at[i] = -1
	}
	var tick, last int64
	for alive > 0 {
		for i := range pos {
			if on[i] && ((pos[i] == 0 && dir[i] == -1) || (pos[i] == 2*n && dir[i] == 1)) {
				on[i] = false
				alive--
				last = tick
			}
		}
		for i := range pos {
			if on[i] {
				other := at[pos[i]]
				if other >= 0 {
					dir[i] = -dir[i]
					dir[other] = -dir[other]
				} else {
					at[pos[i]] = int64(i)
				}
			}
		}
		for i := range pos {
			if on[i] {
				at[pos[i]] = -1
				pos[i] += dir[i]
			}
		}
		tick++
	}
	return last / 2
}

var seed int64 = 1503

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

type plank struct {
	n           int64
	left, right []int64
}

func randomPlank(most int64) plank {
	n := nextRandom()%most + 1
	fill := nextRandom()%100 + 1
	p := plank{n: n}
	for q := int64(0); q <= n; q++ {
		if nextRandom()%100 < fill {
			if nextRandom()%2 == 0 {
				p.left = append(p.left, q)
			} else {
				p.right = append(p.right, q)
			}
		}
	}
	return p
}

func main() {
	planks := make([]plank, 300)
	for i := range planks {
		planks[i] = randomPlank(1000)
	}
	var total, check int64
	for _, p := range planks {
		answer := lastMoment(p.n, p.left, p.right)
		total += answer
		check = mix(check, answer)
	}
	fmt.Printf("300 planks of 1 to 1000 units simulated: sum %d, checksum %d\n", total, check)
}
