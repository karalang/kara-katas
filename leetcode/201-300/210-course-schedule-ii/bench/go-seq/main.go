package main

import "fmt"

// Benchmark workload for LeetCode #210 — Course Schedule II.
const MOD int64 = 1000000007
const BIG int64 = 1000000

func main() {
	var n int64 = 20000
	var e int64 = 80000
	var passes int64 = 800

	eb := make([]int64, 0, e)
	ea := make([]int64, 0, e)
	outdeg := make([]int64, n)
	indeg0 := make([]int64, n)

	var state int64 = 12345
	for i := int64(0); i < e; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		b := state % (n - 1) // 0 .. n-2
		state = (state*1103515245 + 12345) & 2147483647
		a := b + 1 + state%(n-1-b) // b+1 .. n-1 (b < a => DAG)
		eb = append(eb, b)
		ea = append(ea, a)
		outdeg[b]++
		indeg0[a]++
	}

	// CSR build.
	adjStart := make([]int64, n+1)
	for i := int64(0); i < n; i++ {
		adjStart[i+1] = adjStart[i] + outdeg[i]
	}
	adjFlat := make([]int64, e)
	cursor := make([]int64, n)
	for i := int64(0); i < n; i++ {
		cursor[i] = adjStart[i]
	}
	for i := int64(0); i < e; i++ {
		src := eb[i]
		adjFlat[cursor[src]] = ea[i]
		cursor[src]++
	}

	indeg := make([]int64, n)
	queue := make([]int64, n)

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		for i := int64(0); i < n; i++ {
			indeg[i] = indeg0[i]
		}
		blocked := p % n
		indeg[blocked] += BIG

		var head, tail int64 = 0, 0
		for c := int64(0); c < n; c++ {
			if indeg[c] == 0 {
				queue[tail] = c
				tail++
			}
		}
		var checksum, cnt int64 = 0, 0
		for head < tail {
			node := queue[head]
			head++
			checksum = (checksum + node*(cnt+1)) % MOD
			cnt++
			start := adjStart[node]
			end := adjStart[node+1]
			for j := start; j < end; j++ {
				nb := adjFlat[j]
				indeg[nb]--
				if indeg[nb] == 0 {
					queue[tail] = nb
					tail++
				}
			}
		}
		sink += cnt + checksum
	}

	fmt.Println(sink)
}
