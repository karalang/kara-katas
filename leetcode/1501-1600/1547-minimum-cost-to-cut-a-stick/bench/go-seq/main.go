// LeetCode #1547: Minimum Cost to Cut a Stick -- bench: the ★ arm (interval
// DP) over 100 sticks of 2 to 1000000 with 1 to 100 distinct cuts, built
// once, each asked 4 times. Go mirror of cut.kara.
package main

import (
	"fmt"
	"math"
	"sort"
)

func minCost(n int64, cuts []int64) int64 {
	points := append(append([]int64{}, cuts...), 0, n)
	sort.Slice(points, func(a, b int) bool { return points[a] < points[b] })
	m := len(points)
	cost := make([][]int64, m)
	for i := range cost {
		cost[i] = make([]int64, m)
	}
	for gap := 2; gap < m; gap++ {
		for i := 0; i+gap < m; i++ {
			j := i + gap
			best := int64(math.MaxInt64)
			for k := i + 1; k < j; k++ {
				if here := cost[i][k] + cost[k][j]; here < best {
					best = here
				}
			}
			cost[i][j] = best + points[j] - points[i]
		}
	}
	return cost[0][m-1]
}

var seed int64 = 1547

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	type stick struct {
		n    int64
		cuts []int64
	}
	sticks := make([]stick, 0, 100)
	for s := 0; s < 100; s++ {
		a := nextRandom()
		n := (a*32768+nextRandom())%999999 + 2
		want := nextRandom()%100 + 1
		if want > n-1 {
			want = n - 1
		}
		taken := map[int64]bool{}
		cuts := []int64{}
		for int64(len(cuts)) < want {
			b := nextRandom()
			c := (b*32768+nextRandom())%(n-1) + 1
			if !taken[c] {
				taken[c] = true
				cuts = append(cuts, c)
			}
		}
		sticks = append(sticks, stick{n, cuts})
	}
	check := int64(0)
	for p := 0; p < 4; p++ {
		for _, s := range sticks {
			check = mix(check, minCost(s.n, s.cuts))
		}
	}
	fmt.Printf("4 passes over 100 sticks of up to 1000000 with up to 100 cuts: checksum %d\n", check)
}
