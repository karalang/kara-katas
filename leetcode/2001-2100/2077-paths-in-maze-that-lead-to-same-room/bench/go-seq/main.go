// LeetCode #2077: Paths in Maze That Lead to Same Room -- Go mirror of the
// ★ arm's benchmark (maze.kara): 30 mazes of 1000 rooms and about 38000
// corridors; each room's rooms above it a map used as a set, and every
// corridor's triangles the rooms in both its rooms' sets, counted.
package main

import "fmt"

var seed int64 = 2077

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func min(a, b int64) int64 {
	if a < b {
		return a
	}
	return b
}

func max(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func randomMaze(n, count, near int64) [][]int64 {
	seen := map[int64]struct{}{}
	corridors := [][]int64{}
	for i := int64(0); i < count; i++ {
		a := nextRandom()%n + 1
		step := nextRandom()%min(near, n-1) + 1
		b := (a-1+step)%n + 1
		key := min(a, b)*100000 + max(a, b)
		if _, ok := seen[key]; !ok {
			seen[key] = struct{}{}
			if nextRandom()%2 == 0 {
				corridors = append(corridors, []int64{a, b})
			} else {
				corridors = append(corridors, []int64{b, a})
			}
		}
	}
	return corridors
}

func numberOfPaths(n int64, corridors [][]int64) int64 {
	up := make([]map[int64]struct{}, n+1)
	for i := range up {
		up[i] = map[int64]struct{}{}
	}
	for _, c := range corridors {
		up[min(c[0], c[1])][max(c[0], c[1])] = struct{}{}
	}
	var count int64
	for a := int64(1); a <= n; a++ {
		for b := range up[a] {
			for x := range up[a] {
				if _, ok := up[b][x]; ok {
					count++
				}
			}
		}
	}
	return count
}

func main() {
	var total, check int64
	for t := 0; t < 30; t++ {
		corridors := randomMaze(1000, 60000, 60)
		a := numberOfPaths(1000, corridors)
		total += a
		check = (check*31 + a) % 1000000007
	}
	fmt.Printf("30 mazes: sum %d, checksum %d\n", total, check)
}
