// LeetCode #1791: Find Center of Star Graph -- the bench in Go, mirroring
// find_center.kara: the node the first two edges share.
package main

import "fmt"

func findCenter(edges [][]int32) int32 {
	a, b := edges[0][0], edges[0][1]
	if a == edges[1][0] || a == edges[1][1] {
		return a
	}
	return b
}

var seed int64 = 1791

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	stars := make([][][]int32, 0, 2000)
	for s := 0; s < 2000; s++ {
		center := 1 + nextRandom()%100
		edges := make([][]int32, 0, 99)
		for leaf := int64(1); leaf <= 100; leaf++ {
			if leaf == center {
				continue
			}
			if nextRandom()%2 == 0 {
				edges = append(edges, []int32{int32(center), int32(leaf)})
			} else {
				edges = append(edges, []int32{int32(leaf), int32(center)})
			}
		}
		for i := len(edges) - 1; i >= 1; i-- {
			j := nextRandom() % int64(i+1)
			edges[i], edges[j] = edges[j], edges[i]
		}
		stars = append(stars, edges)
	}
	var check int64
	for call := int64(0); call < 20000000; call++ {
		edges := stars[(check+call)%2000]
		check = (check*41 + int64(findCenter(edges))) % 1000000007
	}
	fmt.Printf("20000000 calls over 2000 stars: checksum %d\n", check)
}
