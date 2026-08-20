// PARALLEL twin for LeetCode #288 — same algorithm as go-seq/main.go, with the
// punch loop split across goroutines.
//
// The dictionary and index builds stay sequential: they are ~3000 iterations
// writing a map, and threading them would measure lock contention rather than
// the workload. The punch loop is the parallel part — 1,000,000 queries, each a
// pure read of a map nobody writes any more. That is the same region Kara's
// auto-parallelizer selects unaided (parallel_reduction on unique_count), so
// the lanes compare the same decision made two ways.
//
// Each goroutine keeps a private counter and main sums them after the WaitGroup,
// so no mutex or atomic sits in the inner loop. Integer addition is associative,
// so completion order cannot reach the sink.
package main

import (
	"fmt"
	"runtime"
	"strconv"
	"sync"
)

// Sole holds the single word; conflicted marks two-or-more.
type bucket struct {
	word       string
	conflicted bool
}

func abbrev(w string) string {
	n := len(w)
	if n <= 2 {
		return w
	}
	return string(w[0]) + strconv.Itoa(n-2) + string(w[n-1])
}

func nextRand(state int64) int64 {
	return (state*1103515245 + 12345) & 2147483647
}

func main() {
	const letters = "abcdefghijklmnopqrstuvwxyz"
	var dictN, poolN, punches int64 = 3000, 20000, 1000000
	var seed int64 = 12345

	dict := make([]string, 0, dictN)
	for i := int64(0); i < dictN; i++ {
		seed = nextRand(seed)
		n := 3 + ((seed / 65536) % 8)
		buf := make([]byte, 0, n)
		for j := int64(0); j < n; j++ {
			seed = nextRand(seed)
			buf = append(buf, letters[(seed/65536)%26])
		}
		dict = append(dict, string(buf))
	}

	idx := make(map[string]bucket)
	for _, w := range dict {
		a := abbrev(w)
		prev, ok := idx[a]
		if !ok {
			idx[a] = bucket{word: w}
		} else if !prev.conflicted && prev.word != w {
			idx[a] = bucket{conflicted: true}
		}
	}

	pool := make([]string, 0, poolN)
	for i := int64(0); i < poolN; i++ {
		if i%2 == 0 {
			pool = append(pool, dict[(i*7)%dictN])
		} else {
			seed = nextRand(seed)
			n := 3 + ((seed / 65536) % 8)
			buf := make([]byte, 0, n)
			for j := int64(0); j < n; j++ {
				seed = nextRand(seed)
				buf = append(buf, letters[(seed/65536)%26])
			}
			pool = append(pool, string(buf))
		}
	}

	workers := runtime.NumCPU()
	if workers < 1 {
		workers = 1
	}
	counts := make([]int64, workers)
	per := punches / int64(workers)

	var wg sync.WaitGroup
	for w := 0; w < workers; w++ {
		wg.Add(1)
		go func(w int) {
			defer wg.Done()
			lo := int64(w) * per
			hi := lo + per
			if w == workers-1 {
				hi = punches
			}
			var local int64
			for i := lo; i < hi; i++ {
				word := pool[i%poolN]
				b, ok := idx[abbrev(word)]
				var u bool
				switch {
				case !ok:
					u = true
				case b.conflicted:
					u = false
				default:
					u = b.word == word
				}
				if u {
					local++
				}
			}
			counts[w] = local
		}(w)
	}
	wg.Wait()

	var uniqueCount int64
	for _, c := range counts {
		uniqueCount += c // associative: order cannot matter
	}

	fmt.Printf("unique %d\n", uniqueCount)
}
