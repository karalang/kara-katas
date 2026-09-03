// LeetCode 313 - Super Ugly Number.
//
// Mirror of ugly.kara: the same k-way merge with one pointer per prime and a
// two-pass step (find the minimum, then advance every stream that offered it).
// Same build-once + punch shape, same per-pass prime swap, same masked sink.
// Kept algorithm-for-algorithm so the benchmark lane is honest.
package main

import "fmt"

const (
	terms  = 100000
	passes = 30
	mask   = 1073741823
)

func main() {
	primes := []int64{
		2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
		59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
		127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
	}
	k := int64(len(primes))
	pool := []int64{179, 181, 191, 193, 197, 199, 211, 223}

	ugly := make([]int64, terms)
	idx := make([]int64, k)

	var checksum int64
	for pass := int64(0); pass < passes; pass++ {
		slot := checksum % k
		keep := primes[slot]
		primes[slot] = pool[checksum%int64(len(pool))]

		for i := int64(0); i < k; i++ {
			idx[i] = 0
		}
		ugly[0] = 1
		for m := 1; m < terms; m++ {
			best := primes[0] * ugly[idx[0]]
			for i := int64(1); i < k; i++ {
				c := primes[i] * ugly[idx[i]]
				if c < best {
					best = c
				}
			}
			for i := int64(0); i < k; i++ {
				if primes[i]*ugly[idx[i]] == best {
					idx[i]++
				}
			}
			ugly[m] = best
		}

		checksum = (checksum + ugly[terms-1]) & mask
		primes[slot] = keep
	}

	fmt.Printf("checksum %d\n", checksum)
}
