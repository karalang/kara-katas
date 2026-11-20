// LeetCode #1274 bench, in Go: the ★ arm (divide and conquer by
// quarters through the sea's interface) on 500 random seas of 10 ships in
// the whole 1001-by-1001 square and 10 more in a corner, drawn once, 30
// rounds; every count, and the number of questions asked, folded into a
// checksum.
package main

import "fmt"

type Sea interface {
	hasShips(topRight, bottomLeft []int64) bool
}

type point struct{ x, y int64 }

type ocean struct {
	ships []point
	calls int64
}

func (o *ocean) hasShips(topRight, bottomLeft []int64) bool {
	o.calls++
	for _, p := range o.ships {
		if bottomLeft[0] <= p.x && p.x <= topRight[0] && bottomLeft[1] <= p.y && p.y <= topRight[1] {
			return true
		}
	}
	return false
}

func countShips(sea Sea, topRight, bottomLeft []int64) int64 {
	if bottomLeft[0] > topRight[0] || bottomLeft[1] > topRight[1] {
		return 0
	}
	if !sea.hasShips(topRight, bottomLeft) {
		return 0
	}
	if topRight[0] == bottomLeft[0] && topRight[1] == bottomLeft[1] {
		return 1
	}
	mx := (topRight[0] + bottomLeft[0]) / 2
	my := (topRight[1] + bottomLeft[1]) / 2
	return countShips(sea, []int64{mx, my}, bottomLeft) +
		countShips(sea, []int64{topRight[0], my}, []int64{mx + 1, bottomLeft[1]}) +
		countShips(sea, []int64{mx, topRight[1]}, []int64{bottomLeft[0], my + 1}) +
		countShips(sea, topRight, []int64{mx + 1, my + 1})
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1274)
	seas := make([][]point, 500)
	for s := range seas {
		for i := 0; i < 20; i++ {
			span := int64(1001)
			if i >= 10 {
				span = 30
			}
			x := nextRandom(&seed) % span
			p := point{x, nextRandom(&seed) % span}
			seen := false
			for _, q := range seas[s] {
				if q == p {
					seen = true
				}
			}
			if !seen {
				seas[s] = append(seas[s], p)
			}
		}
	}
	var check int64
	for round := int64(0); round < 30; round++ {
		for _, ships := range seas {
			sea := &ocean{ships: append([]point(nil), ships...)}
			n := countShips(sea, []int64{1000, 1000}, []int64{0, 0})
			check = (check*131 + n + round) % 1000000007
			check = (check*131 + sea.calls) % 1000000007
		}
	}
	fmt.Printf("30 rounds of 500 seas: checksum %d\n", check)
}
