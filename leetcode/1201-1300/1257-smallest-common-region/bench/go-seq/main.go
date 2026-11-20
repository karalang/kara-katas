// LeetCode #1257 bench, in Go: the ★ arm (each region's parent in a map,
// the regions holding `region1` in a set, then a walk up from `region2`
// until it meets one of them) on 20 random trees of 10000 regions built
// once, each nested broadly or deeply, with 250 random pairs asked of
// each; every region found folded into a checksum.
package main

import "fmt"

var seed int64 = 1257

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func name(i int64) string {
	return fmt.Sprintf("r%d", i)
}

func findSmallestRegion(regions [][]string, region1, region2 string) string {
	parent := make(map[string]string)
	for _, list := range regions {
		for _, child := range list[1:] {
			parent[child] = list[0]
		}
	}
	holding := make(map[string]struct{})
	at := region1
	holding[at] = struct{}{}
	for {
		up, ok := parent[at]
		if !ok {
			break
		}
		at = up
		holding[at] = struct{}{}
	}
	at = region2
	for {
		if _, ok := holding[at]; ok {
			break
		}
		at = parent[at]
	}
	return at
}

func randomRegions(n, spread int64) [][]string {
	children := make([][]int64, n)
	for i := int64(1); i < n; i++ {
		lo := i - spread
		if lo < 0 {
			lo = 0
		}
		p := lo + nextRandom()%(i-lo)
		children[p] = append(children[p], i)
	}
	regions := make([][]string, 0)
	for p := int64(0); p < n; p++ {
		if len(children[p]) > 0 {
			list := []string{name(p)}
			for _, c := range children[p] {
				list = append(list, name(c))
			}
			regions = append(regions, list)
		}
	}
	for i := len(regions) - 1; i > 0; i-- {
		j := nextRandom() % int64(i+1)
		regions[i], regions[j] = regions[j], regions[i]
	}
	return regions
}

func main() {
	trees := make([][][]string, 0, 20)
	for t := 0; t < 20; t++ {
		spread := []int64{3, 30, 1000000, 10}[t%4]
		trees = append(trees, randomRegions(10000, spread))
	}
	var check int64
	for _, regions := range trees {
		for k := 0; k < 250; k++ {
			x := name(nextRandom() % 10000)
			y := name(nextRandom() % 10000)
			found := findSmallestRegion(regions, x, y)
			for i := 0; i < len(found); i++ {
				check = (check*131 + int64(found[i])) % 1000000007
			}
		}
	}
	fmt.Printf("20 trees of 10000 regions, 250 pairs each: checksum %d\n", check)
}
