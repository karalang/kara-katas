// LeetCode #75 — goroutine-parallel Go mirror (par lane).
// Same batch of K=2000 independent Dutch National Flag sorts as ../go-seq/main.go;
// the associative sum reduction is split across GOMAXPROCS goroutines (chunked
// seed range, WaitGroup join, merge). Hand-tuned-parallel comparator for Kāra's
// auto-par. Sink matches the seq mirrors.

package main

import (
	"fmt"
	"runtime"
	"sync"
)

const n int64 = 59999

func sortAndHash(seed int64) int64 {
	var a []int64
	for j := int64(0); j < n; j++ {
		a = append(a, (j*7+seed)%3)
	}
	low, mid, high := int64(0), int64(0), n-1
	for mid <= high {
		if a[mid] == 0 {
			a[low], a[mid] = a[mid], a[low]
			low++
			mid++
		} else if a[mid] == 1 {
			mid++
		} else {
			a[mid], a[high] = a[high], a[mid]
			high--
		}
	}
	var acc int64 = 0
	for j := int64(0); j < n; j++ {
		acc = (acc*131 + a[j]) % 1000000007
	}
	return acc
}

func main() {
	const total int64 = 2000
	nw := int64(runtime.GOMAXPROCS(0))
	if nw < 1 {
		nw = 1
	}
	if nw > total {
		nw = total
	}
	partials := make([]int64, nw)
	chunk := total / nw
	var wg sync.WaitGroup
	for w := int64(0); w < nw; w++ {
		start := w * chunk
		end := (w + 1) * chunk
		if w == nw-1 {
			end = total
		}
		wg.Add(1)
		go func(idx, s, e int64) {
			defer wg.Done()
			var sum int64 = 0
			for i := s; i < e; i++ {
				sum += sortAndHash(i)
			}
			partials[idx] = sum
		}(w, start, end)
	}
	wg.Wait()
	var total_sum int64 = 0
	for _, p := range partials {
		total_sum += p
	}
	fmt.Println(total_sum)
}
