// Benchmark for #666: a map of places, walked from the root, as the Kara
// ★ arm.
package main

import "fmt"

func walk(values map[int64]int64, key, above int64) int64 {
	v, ok := values[key]
	if !ok {
		return 0
	}
	sum := above + v
	depth := key / 10
	position := key % 10
	left := (depth+1)*10 + 2*position - 1
	right := left + 1
	_, hasLeft := values[left]
	_, hasRight := values[right]
	if !hasLeft && !hasRight {
		return sum
	}
	return walk(values, left, sum) + walk(values, right, sum)
}

func pathSum(nums []int64) int64 {
	values := make(map[int64]int64)
	for _, x := range nums {
		values[x/10] = x % 10
	}
	return walk(values, 11, 0)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomTree(levels, chance int64, seed *int64) []int64 {
	nums := []int64{110 + nextRandom(seed)%10}
	level := []int64{1}
	for depth := int64(2); depth <= levels; depth++ {
		var next []int64
		for _, p := range level {
			for c := 2*p - 1; c < 2*p+1; c++ {
				if nextRandom(seed)%100 < chance {
					next = append(next, c)
					nums = append(nums, depth*100+c*10+nextRandom(seed)%10)
				}
			}
		}
		level = next
	}
	return nums
}

func main() {
	seed := int64(666)
	trees := make([][]int64, 0, 256)
	for i := 0; i < 256; i++ {
		chance := 50 + nextRandom(&seed)%51
		trees = append(trees, randomTree(4, chance, &seed))
	}
	rounds := int64(1000000)
	var sum int64
	for r := int64(0); r < rounds; r++ {
		sum = (sum*31 + pathSum(trees[r%256]) + r) % 1000000007
	}
	fmt.Printf("256 trees, %d rounds: checksum %d\n", rounds, sum)
}
