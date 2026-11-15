// benchmark's Go mirror of dig.kara (LeetCode #2201, the ★ arm): the dug
// cells in a map used as a set, each as r * n + c.
package main

import "fmt"

func digArtifacts(n int64, artifacts [][4]int64, dig [][2]int64) int64 {
	dug := map[int64]struct{}{}
	for _, d := range dig {
		dug[d[0]*n+d[1]] = struct{}{}
	}
	var count int64
	for _, a := range artifacts {
		whole := true
		for r := a[0]; r <= a[2]; r++ {
			for c := a[1]; c <= a[3]; c++ {
				if _, ok := dug[r*n+c]; !ok {
					whole = false
				}
			}
		}
		if whole {
			count++
		}
	}
	return count
}

var seed int64 = 2201

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func site(n, tries int64, digs int) ([][4]int64, [][2]int64) {
	shapes := [8][2]int64{{1, 1}, {1, 2}, {2, 1}, {2, 2}, {1, 3}, {3, 1}, {1, 4}, {4, 1}}
	taken := make([]bool, n*n)
	artifacts := [][4]int64{}
	for t := int64(0); t < tries; t++ {
		sh := shapes[nextRandom()%8]
		h, w := sh[0], sh[1]
		r := wideRandom() % (n - h + 1)
		c := wideRandom() % (n - w + 1)
		free := true
		for i := r; i < r+h; i++ {
			for j := c; j < c+w; j++ {
				if taken[i*n+j] {
					free = false
				}
			}
		}
		if free {
			for i := r; i < r+h; i++ {
				for j := c; j < c+w; j++ {
					taken[i*n+j] = true
				}
			}
			artifacts = append(artifacts, [4]int64{r, c, r + h - 1, c + w - 1})
		}
	}
	dug := make([]bool, n*n)
	dig := [][2]int64{}
	for len(dig) < digs {
		cell := wideRandom() % (n * n)
		if !dug[cell] {
			dug[cell] = true
			dig = append(dig, [2]int64{cell / n, cell % n})
		}
	}
	return artifacts, dig
}

func main() {
	type siteT struct {
		artifacts [][4]int64
		dig       [][2]int64
	}
	sites := []siteT{}
	for i := 0; i < 8; i++ {
		a, d := site(1000, 20000, 300000)
		sites = append(sites, siteT{a, d})
	}
	var check int64
	for p := 0; p < 10; p++ {
		for _, s := range sites {
			count := digArtifacts(1000, s.artifacts, s.dig)
			check = (check*31 + count + int64(len(s.artifacts))) % 1000000007
		}
	}
	fmt.Printf("10 passes over 8 sites: checksum %d\n", check)
}
