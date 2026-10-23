// LeetCode #913: Cat and Mouse -- bench: Go mirror of the retrograde
// analysis with a queue in cat_mouse_game.kara.
package main

import "fmt"

func catMouseGame(graph [][]int64) int64 {
	n := int64(len(graph))
	result := make([]int64, n*n*2)
	left := make([]int64, n*n*2)
	for m := int64(0); m < n; m++ {
		for c := int64(1); c < n; c++ {
			left[(m*n+c)*2] = int64(len(graph[m]))
			moves := int64(0)
			for _, d := range graph[c] {
				if d != 0 {
					moves++
				}
			}
			left[(m*n+c)*2+1] = moves
		}
	}
	queue := []int64{}
	for c := int64(1); c < n; c++ {
		for t := int64(0); t < 2; t++ {
			result[c*2+t] = 1
			queue = append(queue, c*2+t)
			result[(c*n+c)*2+t] = 2
			queue = append(queue, (c*n+c)*2+t)
		}
	}
	for head := 0; head < len(queue); head++ {
		s := queue[head]
		t := s % 2
		c := s / 2 % n
		m := s / 2 / n
		won := result[s]
		if t == 1 {
			for _, pm := range graph[m] {
				p := (pm*n + c) * 2
				if result[p] == 0 {
					if won == 1 {
						result[p] = 1
						queue = append(queue, p)
					} else {
						left[p]--
						if left[p] == 0 {
							result[p] = 2
							queue = append(queue, p)
						}
					}
				}
			}
		} else {
			for _, pc := range graph[c] {
				if pc != 0 {
					p := (m*n+pc)*2 + 1
					if result[p] == 0 {
						if won == 2 {
							result[p] = 2
							queue = append(queue, p)
						} else {
							left[p]--
							if left[p] == 0 {
								result[p] = 1
								queue = append(queue, p)
							}
						}
					}
				}
			}
		}
	}
	return result[(n+2)*2]
}

var seed int64 = 913

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomGraph(n, per int64) [][]int64 {
	adj := make([]bool, n*n)
	for u := int64(0); u < n; u++ {
		for v := u + 1; v < n; v++ {
			chance := per
			if u == 0 {
				chance = per / 4
			}
			if nextRandom()%1000 < chance {
				adj[u*n+v] = true
				adj[v*n+u] = true
			}
		}
	}
	for v := int64(1); v < n; v++ {
		alone := true
		for u := int64(1); u < n; u++ {
			if adj[v*n+u] {
				alone = false
			}
		}
		if alone {
			u := 1 + nextRandom()%(n-2)
			if u >= v {
				u++
			}
			adj[u*n+v] = true
			adj[v*n+u] = true
		}
	}
	holeAlone := true
	for u := int64(1); u < n; u++ {
		if adj[u] {
			holeAlone = false
		}
	}
	if holeAlone {
		u := 1 + nextRandom()%(n-1)
		adj[u] = true
		adj[u*n] = true
	}
	graph := make([][]int64, 0, n)
	for v := int64(0); v < n; v++ {
		near := []int64{}
		for u := int64(0); u < n; u++ {
			if adj[v*n+u] {
				near = append(near, u)
			}
		}
		graph = append(graph, near)
	}
	return graph
}

func main() {
	rounds := 4000
	wins := [3]int64{}
	check := int64(0)
	for r := 0; r < rounds; r++ {
		per := int64(400)
		switch r % 4 {
		case 0:
			per = 20
		case 1:
			per = 60
		case 2:
			per = 150
		}
		outcome := catMouseGame(randomGraph(50, per))
		wins[outcome]++
		check = (check*7 + outcome) % 1000000007
	}
	fmt.Printf("%d graphs of 50 nodes: %d draws, %d mouse wins, %d cat wins, checksum %d\n", rounds, wins[0], wins[1], wins[2], check)
}
