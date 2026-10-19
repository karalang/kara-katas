// LeetCode 797 — All Paths From Source to Target: the bench, in Go.
// Mirrors all_paths_source_target.kara: a depth first search keeping the
// path so far, copying it at node n - 1.
package main

import "fmt"

func walk(graph [][]int64, node int64, path *[]int64, paths *[][]int64) {
	if node == int64(len(graph))-1 {
		cp := make([]int64, len(*path))
		copy(cp, *path)
		*paths = append(*paths, cp)
		return
	}
	for _, next := range graph[node] {
		*path = append(*path, next)
		walk(graph, next, path, paths)
		*path = (*path)[:len(*path)-1]
	}
}

func allPathsSourceTarget(graph [][]int64) [][]int64 {
	var paths [][]int64
	path := []int64{0}
	walk(graph, 0, &path, &paths)
	return paths
}

var seed int64 = 797

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 15
	graphs := make([][][]int64, 0, 1024)
	for g := 0; g < 1024; g++ {
		order := []int64{0}
		for i := int64(1); i < n-1; i++ {
			order = append(order, i)
		}
		for i := int64(2); i < n-1; i++ {
			j := 1 + nextRandom()%i
			order[i], order[j] = order[j], order[i]
		}
		order = append(order, n-1)
		chance := 1 + nextRandom()%4
		graph := make([][]int64, n)
		for a := int64(0); a < n; a++ {
			for b := a + 1; b < n; b++ {
				if nextRandom()%5 < chance {
					graph[order[a]] = append(graph[order[a]], order[b])
				}
			}
		}
		graphs = append(graphs, graph)
	}
	var rounds int64 = 40960
	var count, nodes, check int64
	for r := int64(0); r < rounds; r++ {
		paths := allPathsSourceTarget(graphs[r%1024])
		count += int64(len(paths))
		for _, path := range paths {
			nodes += int64(len(path))
			var h int64
			for _, v := range path {
				h = (h*31 + v + 1) % 1000000007
			}
			check = (check + h) % 1000000007
		}
	}
	fmt.Printf("%d graphs: %d paths through %d nodes, checksum %d\n", rounds, count, nodes, check)
}
