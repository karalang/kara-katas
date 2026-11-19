// LeetCode #1659: Maximize Grid Happiness -- the bench's Go mirror: the ★
// arm on 2000 random problems on grids of 4 to 5 rows by 4 to 5 columns
// with up to 6 introverts and 6 extroverts, all drawn first.
package main

import "fmt"

const (
	introvert = 1
	extrovert = 2
)

func pair(a, b int64) int64 {
	if a == 0 || b == 0 {
		return 0
	}
	var score int64
	for _, p := range [2]int64{a, b} {
		if p == introvert {
			score -= 30
		} else {
			score += 20
		}
	}
	return score
}

type grid struct {
	m, n, top int64
	memo      []int64
}

func (g *grid) best(cell, introverts, extroverts, last int64) int64 {
	if cell == g.m*g.n || (introverts == 0 && extroverts == 0) {
		return 0
	}
	key := ((cell*7+introverts)*7+extroverts)*g.top + last
	if g.memo[key] >= 0 {
		return g.memo[key]
	}
	up := last / (g.top / 3)
	var left int64
	if cell%g.n != 0 {
		left = last % 3
	}
	shifted := last % (g.top / 3) * 3
	best := g.best(cell+1, introverts, extroverts, shifted)
	if introverts > 0 {
		gain := 120 + pair(introvert, up) + pair(introvert, left)
		best = max(best, gain+g.best(cell+1, introverts-1, extroverts, shifted+introvert))
	}
	if extroverts > 0 {
		gain := 40 + pair(extrovert, up) + pair(extrovert, left)
		best = max(best, gain+g.best(cell+1, introverts, extroverts-1, shifted+extrovert))
	}
	g.memo[key] = best
	return best
}

func getMaxGridHappiness(m, n, introvertsCount, extrovertsCount int32) int32 {
	top := int64(1)
	for i := int32(0); i < n; i++ {
		top *= 3
	}
	g := grid{int64(m), int64(n), top, make([]int64, int64(m)*int64(n)*49*top)}
	for i := range g.memo {
		g.memo[i] = -1
	}
	return int32(g.best(0, int64(introvertsCount), int64(extrovertsCount), 0))
}

var seed int64 = 1659

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	problems := make([][4]int32, 0, 2000)
	for p := 0; p < 2000; p++ {
		m := int32(nextRandom()%2 + 4)
		n := int32(nextRandom()%2 + 4)
		i := int32(nextRandom() % 7)
		e := int32(nextRandom() % 7)
		problems = append(problems, [4]int32{m, n, i, e})
	}
	var check, total int64
	for _, p := range problems {
		answer := int64(getMaxGridHappiness(p[0], p[1], p[2], p[3]))
		total += answer
		check = (check*31 + answer + 1) % 1000000007
	}
	fmt.Printf("2000 grids of 4 to 5 by 4 to 5: happiness sums to %d, checksum %d\n", total, check)
}
