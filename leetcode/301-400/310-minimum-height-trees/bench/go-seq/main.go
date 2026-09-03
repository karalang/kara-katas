// Benchmark mirror — LeetCode 310, Minimum Height Trees.
// Same four CSR trees, same LCG, same leaf-peeling, same checksum-driven tree
// selection and masked sink as peel.kara. See ../../README.md § Benchmarks.
package main

import "fmt"

func main() {
	const n int64 = 60000
	const trees int64 = 4
	const passes int64 = 950

	allOff := make([]int64, 0, trees*(n+1))
	allNbr := make([]int64, 0, trees*2*(n-1)+16)
	state := int64(20310)
	deg := make([]int64, n)
	pa := make([]int64, n)
	cursor := make([]int64, n)

	for t := int64(0); t < trees; t++ {
		window := 1 + t*3
		for i := int64(0); i < n; i++ { deg[i] = 0 }
		pa[0] = 0
		for i := int64(1); i < n; i++ {
			w := window
			if w > i { w = i }
			state = (state*1103515245 + 12345) % 2147483648
			p := i - 1 - state%w
			pa[i] = p; deg[i]++; deg[p]++
		}
		base := int64(len(allOff))
		running := int64(len(allNbr))
		for k := int64(0); k < n; k++ { allOff = append(allOff, running); running += deg[k] }
		allOff = append(allOff, running)
		for k := int64(0); k < n; k++ { cursor[k] = allOff[base+k] }
		for int64(len(allNbr)) < running { allNbr = append(allNbr, 0) }
		for i := int64(1); i < n; i++ {
			p := pa[i]
			allNbr[cursor[i]] = p; cursor[i]++
			allNbr[cursor[p]] = i; cursor[p]++
		}
	}

	var checksum int64
	degree := make([]int64, n)
	alive := make([]int64, n)
	layer := make([]int64, n)
	next := make([]int64, n)

	for p := int64(0); p < passes; p++ {
		which := (p + checksum) % trees
		base := which * (n + 1)

		var lcount int64
		for i := int64(0); i < n; i++ {
			d := allOff[base+i+1] - allOff[base+i]
			degree[i] = d; alive[i] = 1
			if d == 1 { layer[lcount] = i; lcount++ }
		}

		remaining := n
		for remaining > 2 {
			remaining -= lcount
			var ncount int64
			for k := int64(0); k < lcount; k++ {
				v := layer[k]
				alive[v] = 0
				for j := allOff[base+v]; j < allOff[base+v+1]; j++ {
					w := allNbr[j]
					if alive[w] == 1 {
						degree[w]--
						if degree[w] == 1 { next[ncount] = w; ncount++ }
					}
				}
			}
			for c := int64(0); c < ncount; c++ { layer[c] = next[c] }
			lcount = ncount
		}

		var acc int64
		for i := int64(0); i < n; i++ { if alive[i] == 1 { acc += i } }
		checksum = (checksum + acc) & 0x3FFFFFFF
	}
	fmt.Printf("checksum %d\n", checksum)
}
