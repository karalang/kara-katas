// LeetCode #2477: Minimum Fuel Cost to Report to the Capital -- the bench,
// the ★ arm in Go: a breadth-first order from the capital, walked
// backwards, gives each city its subtree's size, and the road out of it
// carries `ceil(size / seats)` cars.
package main

import "fmt"

func minimumFuelCost(roads [][2]int64, seats int64) int64 {
	n := len(roads) + 1
	adjacent := make([][]int64, n)
	for _, r := range roads {
		adjacent[r[0]] = append(adjacent[r[0]], r[1])
		adjacent[r[1]] = append(adjacent[r[1]], r[0])
	}
	parent := make([]int64, n)
	for i := range parent {
		parent[i] = -1
	}
	parent[0] = 0
	order := []int64{0}
	for next := 0; next < len(order); next++ {
		city := order[next]
		for _, other := range adjacent[city] {
			if parent[other] < 0 {
				parent[other] = city
				order = append(order, other)
			}
		}
	}
	size := make([]int64, n)
	for i := range size {
		size[i] = 1
	}
	var fuel int64
	for k := n - 1; k >= 1; k-- {
		city := order[k]
		fuel += (size[city] + seats - 1) / seats
		size[parent[city]] += size[city]
	}
	return fuel
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2477

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func randomRoads(n int64) [][2]int64 {
	var roads [][2]int64
	for k := int64(1); k < n; k++ {
		other := wideRandom() % k
		if nextRandom()%2 == 0 {
			roads = append(roads, [2]int64{k, other})
		} else {
			roads = append(roads, [2]int64{other, k})
		}
	}
	for i := int64(len(roads)) - 1; i > 0; i-- {
		j := wideRandom() % (i + 1)
		roads[i], roads[j] = roads[j], roads[i]
	}
	return roads
}

func main() {
	// 20 random trees of 10^4 cities built once; then 60 passes, each
	// answering every tree with 1 to 50 seats chosen by the checksum so
	// far, folding the fuel plus the pass into the checksum
	trees := make([][][2]int64, 20)
	for t := range trees {
		trees[t] = randomRoads(10000)
	}
	var check int64
	for p := int64(0); p < 60; p++ {
		for _, roads := range trees {
			seats := 1 + check%50
			check = (check*31 + minimumFuelCost(roads, seats) + p) % 1000000007
		}
	}
	fmt.Printf("60 passes over 20 trees of 10^4: checksum %d\n", check)
}
