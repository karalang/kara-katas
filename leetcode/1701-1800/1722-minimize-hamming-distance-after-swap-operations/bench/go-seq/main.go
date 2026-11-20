// LeetCode #1722: Minimize Hamming Distance After Swap Operations -- the
// bench (hamming.kara): the swaps joined into groups with a union-find,
// each group's source values counted, and each target value matched from
// its group's counts.
package main

import "fmt"

type key struct {
	group int64
	value int32
}

func find(parent []int64, x int64) int64 {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func minimumHammingDistance(source, target []int32, allowed [][2]int32) int32 {
	n := int64(len(source))
	parent := make([]int64, n)
	size := make([]int64, n)
	for i := range parent {
		parent[i] = int64(i)
		size[i] = 1
	}
	for _, s := range allowed {
		a := find(parent, int64(s[0]))
		b := find(parent, int64(s[1]))
		if a == b {
			continue
		}
		if size[a] < size[b] {
			a, b = b, a
		}
		parent[b] = a
		size[a] += size[b]
	}
	counts := make(map[key]int64)
	for i := int64(0); i < n; i++ {
		counts[key{find(parent, i), source[i]}]++
	}
	var distance int32
	for i := int64(0); i < n; i++ {
		k := key{find(parent, i), target[i]}
		if counts[k] > 0 {
			counts[k]--
		} else {
			distance++
		}
	}
	return distance
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func main() {
	count := 10
	var rounds int64 = 5
	var n int64 = 100000
	var seed int64 = 1722
	sources := make([][]int32, count)
	targets := make([][]int32, count)
	alloweds := make([][][2]int32, count)
	for c := 0; c < count; c++ {
		sources[c] = make([]int32, n)
		for i := range sources[c] {
			sources[c][i] = int32(wide(&seed)%100000 + 1)
		}
		targets[c] = make([]int32, n)
		for i := range targets[c] {
			targets[c][i] = int32(wide(&seed)%100000 + 1)
		}
		alloweds[c] = make([][2]int32, n)
		for i := range alloweds[c] {
			a := wide(&seed) % n
			b := wide(&seed) % (n - 1)
			if b >= a {
				b++
			}
			alloweds[c][i] = [2]int32{int32(a), int32(b)}
		}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			answer := int64(minimumHammingDistance(sources[c], targets[c], alloweds[c]))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d values and %d swaps, %d rounds: distances sum to %d, checksum %d\n", count, n, n, rounds, sum, check)
}
