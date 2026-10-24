// LeetCode #952 bench: Go mirror of largest_component_size.kara (the ★
// arm, union by prime, a map from prime to its first place) on the same
// 20 sets.
package main

import "fmt"

func find(parent []int64, x int64) int64 {
	root := x
	for parent[root] != root {
		root = parent[root]
	}
	y := x
	for parent[y] != root {
		next := parent[y]
		parent[y] = root
		y = next
	}
	return root
}

func largestComponentSize(nums []int64) int64 {
	n := int64(len(nums))
	parent := make([]int64, n)
	size := make([]int64, n)
	for i := int64(0); i < n; i++ {
		parent[i] = i
		size[i] = 1
	}
	first := map[int64]int64{}
	for i := int64(0); i < n; i++ {
		x := nums[i]
		p := int64(2)
		for x > 1 {
			if p*p > x {
				p = x
			}
			if x%p == 0 {
				for x%p == 0 {
					x /= p
				}
				if j, ok := first[p]; ok {
					a := find(parent, i)
					b := find(parent, j)
					if a != b {
						if size[a] < size[b] {
							parent[a] = b
							size[b] += size[a]
						} else {
							parent[b] = a
							size[a] += size[b]
						}
					}
				} else {
					first[p] = i
				}
			}
			p++
		}
	}
	best := int64(0)
	for i := int64(0); i < n; i++ {
		if parent[i] == i && size[i] > best {
			best = size[i]
		}
	}
	return best
}

var seed int64 = 952

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, count, n = 40, 20, 2000
	// 20 sets of 2000 distinct numbers from 1 to 100000
	sets := make([][]int64, 0, count)
	for c := 0; c < count; c++ {
		taken := map[int64]bool{}
		nums := make([]int64, 0, n)
		for len(nums) < n {
			hi := nextRandom()
			v := 1 + (hi*32768+nextRandom())%100000
			if !taken[v] {
				taken[v] = true
				nums = append(nums, v)
			}
		}
		sets = append(sets, nums)
	}
	total, check := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			k := (r + i) % count
			size := largestComponentSize(sets[k])
			total += size
			check = (check*31 + size) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d sets of %d numbers up to 100000: largest components adding to %d, checksum %d\n", rounds, count, n, total, check)
}
