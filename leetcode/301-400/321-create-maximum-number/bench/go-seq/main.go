// Benchmark mirror of LeetCode #321 — same split-shrink-merge as
// bench/create_max_number.kara.
package main

import "fmt"

const (
	LEN1    = 1500
	LEN2    = 1700
	PASSES  = 24
	MODULUS = 1073741789
)

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func shrink(nums []int64, keep int64, out []int64) {
	var top int64
	drop := int64(len(nums)) - keep
	for _, d := range nums {
		for drop > 0 && top > 0 && out[top-1] < d {
			top--
			drop--
		}
		if top < keep {
			out[top] = d
			top++
		} else {
			drop--
		}
	}
}

func suffixGreater(a []int64, alen, i int64, b []int64, blen, j int64) bool {
	x, y := i, j
	for x < alen && y < blen && a[x] == b[y] {
		x++
		y++
	}
	if y == blen {
		return x < alen
	}
	if x == alen {
		return false
	}
	return a[x] > b[y]
}

func merge(a []int64, alen int64, b []int64, blen int64, out []int64) {
	var i, j, t int64
	for i < alen || j < blen {
		if suffixGreater(a, alen, i, b, blen, j) {
			out[t] = a[i]
			i++
		} else {
			out[t] = b[j]
			j++
		}
		t++
	}
}

func main() {
	var seed int64 = 321
	var sink, digitsOut int64

	left := make([]int64, LEN1+LEN2)
	right := make([]int64, LEN1+LEN2)
	cand := make([]int64, LEN1+LEN2)
	best := make([]int64, LEN1+LEN2)

	for p := int64(0); p < PASSES; p++ {
		nums1 := make([]int64, LEN1)
		nums2 := make([]int64, LEN2)
		for x := range nums1 {
			nums1[x] = next(&seed) % 10
		}
		for x := range nums2 {
			nums2[x] = next(&seed) % 10
		}

		ks := [3]int64{LEN1 / 3, (LEN1 + LEN2) / 2, LEN1 + LEN2 - 7*(p+1)}
		for _, k := range ks {
			lo := k - LEN2
			if lo < 0 {
				lo = 0
			}
			hi := k
			if hi > LEN1 {
				hi = LEN1
			}
			have := false
			for i := lo; i <= hi; i++ {
				shrink(nums1, i, left)
				shrink(nums2, k-i, right)
				merge(left, i, right, k-i, cand)
				if !have || suffixGreater(cand, k, 0, best, k, 0) {
					copy(best[:k], cand[:k])
					have = true
				}
			}

			var acc int64
			for x := int64(0); x < k; x++ {
				acc = (acc*131 + best[x] + 1) % MODULUS
			}
			sink = (sink*1000003 + acc) % MODULUS
			digitsOut += k
		}
	}

	fmt.Printf("sink %d digits %d\n", sink, digitsOut)
}
