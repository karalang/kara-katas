// Benchmark mirror of LeetCode #324 — same select arm as
// bench/wiggle_sort.kara.
package main

import "fmt"

const (
	LEN     = 1000000
	PASSES  = 16
	STRIDE  = 9973
	MODULUS = 1073741789
)

func median3(x, y, z int64) int64 {
	if (x <= y && y <= z) || (z <= y && y <= x) {
		return y
	}
	if (y <= x && x <= z) || (z <= x && x <= y) {
		return x
	}
	return z
}

func selectK(a []int64, k int64) int64 {
	lo, hi := int64(0), int64(len(a))-1
	for lo < hi {
		mid := lo + (hi-lo)/2
		pivot := median3(a[lo], a[mid], a[hi])
		lt, i, gt := lo, lo, hi
		for i <= gt {
			if a[i] < pivot {
				a[lt], a[i] = a[i], a[lt]
				lt++
				i++
			} else if a[i] > pivot {
				a[i], a[gt] = a[gt], a[i]
				gt--
			} else {
				i++
			}
		}
		if k < lt {
			hi = lt - 1
		} else if k > gt {
			lo = gt + 1
		} else {
			return pivot
		}
	}
	return a[k]
}

func wiggleSort(nums []int64) {
	n := int64(len(nums))
	median := selectK(nums, n/2)
	m := n | 1
	left, i, right := int64(0), int64(0), n-1
	for i <= right {
		vi := (1 + 2*i) % m
		if nums[vi] > median {
			l := (1 + 2*left) % m
			nums[l], nums[vi] = nums[vi], nums[l]
			left++
			i++
		} else if nums[vi] < median {
			r := (1 + 2*right) % m
			nums[vi], nums[r] = nums[r], nums[vi]
			right--
		} else {
			i++
		}
	}
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func draw(seed *int64, bound int64) int64 {
	hi := next(seed)
	lo := next(seed)
	return (hi*32768 + lo) % bound
}

func refill(nums []int64, k int64, seed *int64) {
	n := int64(len(nums))
	for i := int64(0); i < n; i++ {
		if i%2 == 0 {
			nums[i] = draw(seed, k)
		} else {
			nums[i] = k + draw(seed, k)
		}
	}
	for i := n - 1; i > 0; i-- {
		j := draw(seed, i+1)
		nums[i], nums[j] = nums[j], nums[i]
	}
}

func violations(a []int64) int64 {
	bad := int64(0)
	for i := 1; i < len(a); i++ {
		if i%2 == 1 {
			if a[i] <= a[i-1] {
				bad++
			}
		} else if a[i] >= a[i-1] {
			bad++
		}
	}
	return bad
}

func main() {
	seed, sink, bad := int64(324), int64(0), int64(0)
	ks := [4]int64{2, 3, 50, 2500}
	nums := make([]int64, LEN)
	for p := 0; p < PASSES; p++ {
		refill(nums, ks[p%4], &seed)
		wiggleSort(nums)
		bad = violations(nums)
		probe := int64(0)
		for i := 0; i < LEN; i += STRIDE {
			probe = (probe*31 + nums[i]) % MODULUS
		}
		sink = (sink*131 + bad*7 + probe) % MODULUS
	}
	fmt.Printf("sink %d violations %d\n", sink, bad)
}
