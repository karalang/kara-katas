// Benchmark for #845: Longest Mountain in Array -- Go twin of the Kāra ★ arm
// (one pass with two counters).
package main

import "fmt"

func longestMountain(arr []int64) int64 {
	var best, up, down int64
	for i := 1; i < len(arr); i++ {
		if (down > 0 && arr[i-1] < arr[i]) || arr[i-1] == arr[i] {
			up = 0
			down = 0
		}
		if arr[i-1] < arr[i] {
			up++
		} else if arr[i-1] > arr[i] {
			down++
		}
		if up > 0 && down > 0 && up+down+1 > best {
			best = up + down + 1
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 64, 20000, 10000
	seed := int64(845)
	arrays := make([][]int64, 0, count)
	for g := 0; g < count; g++ {
		arr := make([]int64, 0, n)
		if g%3 == 0 {
			for i := 0; i < n; i++ {
				arr = append(arr, nextRandom(&seed)%10001)
			}
		} else if g%3 == 1 {
			v := int64(5000)
			for i := 0; i < n; i++ {
				arr = append(arr, v)
				v += nextRandom(&seed)%3 - 1
			}
		} else {
			for len(arr) < n {
				up := nextRandom(&seed) % 40
				down := nextRandom(&seed) % 40
				base := nextRandom(&seed) % 100
				for k := int64(0); k < up+1; k++ {
					if len(arr) < n {
						arr = append(arr, base+k)
					}
				}
				for k := int64(0); k < down; k++ {
					if len(arr) < n {
						arr = append(arr, base+up-k-1)
					}
				}
			}
		}
		arrays = append(arrays, arr)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		m := longestMountain(arrays[round%count])
		total += m
		checksum = (checksum*31 + m) % 1000000007
	}
	fmt.Printf("%d rounds of %d arrays: lengths sum to %d, checksum %d\n", rounds, count, total, checksum)
}
