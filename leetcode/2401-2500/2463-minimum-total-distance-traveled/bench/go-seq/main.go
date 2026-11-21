// LeetCode #2463: Minimum Total Distance Traveled -- the bench, the ★ arm
// in Go: a table over the sorted robots and factories, each factory
// either skipped or given the next run of robots up to its limit.
package main

import (
	"fmt"
	"slices"
)

const none int64 = 9000000000000000000

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func minimumTotalDistance(robot []int64, factory [][]int64) int64 {
	robots := slices.Clone(robot)
	slices.Sort(robots)
	factories := slices.Clone(factory)
	slices.SortFunc(factories, func(a, b []int64) int { return slices.Compare(a, b) })
	n, m := len(robots), len(factories)
	best := make([][]int64, n+1)
	for i := range best {
		best[i] = make([]int64, m+1)
		for j := range best[i] {
			best[i][j] = none
		}
	}
	for j := 0; j <= m; j++ {
		best[n][j] = 0
	}
	for j := m - 1; j >= 0; j-- {
		at, limit := factories[j][0], int(factories[j][1])
		for i := n - 1; i >= 0; i-- {
			least := best[i][j+1]
			run := int64(0)
			for t := 1; t <= min(limit, n-i); t++ {
				run += abs(robots[i+t-1] - at)
				if best[i+t][j+1] < none {
					least = min(least, run+best[i+t][j+1])
				}
			}
			best[i][j] = least
		}
	}
	return best[0][0]
}

var seed int64 = 2463

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func randomCase(n, m int, top, cap int64) ([]int64, [][]int64) {
	taken := map[int64]bool{}
	robot := []int64{}
	for len(robot) < n {
		p := wideRandom()%(2*top+1) - top
		if !taken[p] {
			taken[p] = true
			robot = append(robot, p)
		}
	}
	places := map[int64]bool{}
	factory := [][]int64{}
	for len(factory) < m {
		p := wideRandom()%(2*top+1) - top
		if !places[p] {
			places[p] = true
			factory = append(factory, []int64{p, nextRandom() % (cap + 1)})
		}
	}
	room := int64(0)
	for _, f := range factory {
		room += f[1]
	}
	for j := 0; room < int64(n); j, room = j+1, room+1 {
		factory[j%m][1]++
	}
	return robot, factory
}

func main() {
	// 40 cases of 100 robots and 100 factories over 2 10^9 places, limits
	// up to 2, built once; then 72 passes, each raising one limit of every
	// case, chosen by the checksum so far, then answering every case and
	// folding the answer plus the pass into the checksum
	robots := make([][]int64, 40)
	factories := make([][][]int64, 40)
	for c := range robots {
		robots[c], factories[c] = randomCase(100, 100, 1000000000, 2)
	}
	check := int64(0)
	for p := int64(0); p < 72; p++ {
		for c := range robots {
			factories[c][(check+int64(c))%100][1]++
			check = (check*31 + minimumTotalDistance(robots[c], factories[c])%1000000007 + p) % 1000000007
		}
	}
	fmt.Printf("72 passes over 40 cases of 100 robots: checksum %d\n", check)
}
