// Benchmark workload — Sort Colors (LeetCode #75), seq lane.
// Go single-threaded mirror of bench/sort_colors.{kara,rs,c}. A batch of K=2000
// independent Dutch National Flag sorts of n=59999 {0,1,2} arrays (each grown by
// append from empty, matching Kāra's Vec.new()+push), each hashed, combined
// through a plain associative sum. Single-threaded baseline; go-par/ is the
// goroutine parallel comparator for Kāra's auto-par. See ../README.md.

package main

import "fmt"

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
	var sum int64 = 0
	for i := int64(0); i < total; i++ {
		sum += sortAndHash(i)
	}
	fmt.Println(sum)
}
