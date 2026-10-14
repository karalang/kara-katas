// Benchmark for #565: Go mirror of the ★ arm (walk each cycle once); see
// ../array_nesting.kara.
package main

import "fmt"

func arrayNesting(nums []int64) int64 {
	n := len(nums)
	visited := make([]bool, n)
	var best int64
	for start := 0; start < n; start++ {
		if visited[start] {
			continue
		}
		var length int64
		i := int64(start)
		for !visited[i] {
			visited[i] = true
			i = nums[i]
			length++
		}
		best = max(best, length)
	}
	return best
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := int64(20)
	rounds := int64(100)
	n := int64(100000)
	seed := int64(565)
	perms := make([][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = int64(i)
		}
		if g%2 == 0 {
			for i := n - 1; i > 0; i-- {
				hi := step(&seed)
				j := (hi*32768 + step(&seed)) % (i + 1)
				nums[i], nums[j] = nums[j], nums[i]
			}
		} else {
			start := int64(0)
			for start < n {
				length := min(1+step(&seed)%2000, n-start)
				for j := int64(0); j < length; j++ {
					nums[start+j] = start + (j+1)%length
				}
				start += length
			}
		}
		perms = append(perms, nums)
	}
	var total, checksum int64
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			got := arrayNesting(perms[(round*7+g)%count])
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d permutations of %d, %d rounds: total %d, checksum %d\n", count, n, rounds, total, checksum)
}
