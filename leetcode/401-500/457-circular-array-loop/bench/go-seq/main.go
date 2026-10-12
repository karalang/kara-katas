// Benchmark for #457: mirror of circular_loop.kara (the ★ arm, slow and
// fast pointers) on the same workload.
package main

import "fmt"

func nextIndex(a []int64, i int64) int64 {
	n := int64(len(a))
	return ((i+a[i])%n + n) % n
}

func circularArrayLoop(nums []int64) bool {
	a := make([]int64, len(nums))
	copy(a, nums)
	n := int64(len(a))
	for start := int64(0); start < n; start++ {
		if a[start] == 0 {
			continue
		}
		forward := a[start] > 0
		slow, fast := start, start
		for {
			s := nextIndex(a, slow)
			f1 := nextIndex(a, fast)
			if a[f1] == 0 || (a[f1] > 0) != forward {
				break
			}
			f2 := nextIndex(a, f1)
			if a[f2] == 0 || (a[f2] > 0) != forward {
				break
			}
			slow, fast = s, f2
			if slow == fast {
				if nextIndex(a, slow) != slow {
					return true
				}
				break
			}
		}
		// Nothing on this path reaches a valid cycle: clear it.
		i := start
		for a[i] != 0 && (a[i] > 0) == forward {
			next := nextIndex(a, i)
			a[i] = 0
			i = next
		}
	}
	return false
}

// ---- benchmark --------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const arrays = 10
	const n = 1000000
	const rounds = 5
	var seed int64 = 457
	all := make([][]int64, 0, arrays)
	for a := 0; a < arrays; a++ {
		nums := make([]int64, 0)
		for i := 0; i < n; i++ {
			step := 1 + nextRandom(&seed)%1000
			if nextRandom(&seed)%2 == 0 {
				nums = append(nums, step)
			} else {
				nums = append(nums, -step)
			}
		}
		all = append(all, nums)
	}
	found := 0
	var checksum int64
	for r := 0; r < rounds; r++ {
		for a := 0; a < arrays; a++ {
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			k := (hi*65536 + lo) % (n - 1)
			one, two := all[a][k], all[a][k+1]
			if nextRandom(&seed)%2 == 0 {
				all[a][k] = 1
				all[a][k+1] = n - 1
			}
			has := circularArrayLoop(all[a])
			all[a][k], all[a][k+1] = one, two
			var mark int64
			if has {
				found++
				mark = k + 1
			}
			checksum = (checksum*31 + mark) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d arrays of %d: %d with a loop, checksum %d\n", rounds, arrays, n, found, checksum)
}
