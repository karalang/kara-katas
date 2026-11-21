// LeetCode #1649: Create Sorted Array through Instructions -- the bench's
// Go mirror: the ★ arm on 60 random lists of 100000 instructions from 1
// to 100000, all drawn first.
package main

import "fmt"

const mod = 1_000_000_007

func prefix(tree []int64, v int64) int64 {
	var total int64
	for i := v; i > 0; i -= i & -i {
		total += tree[i]
	}
	return total
}

func createSortedArray(instructions []int32) int32 {
	var top int64
	for _, v := range instructions {
		if int64(v) > top {
			top = int64(v)
		}
	}
	tree := make([]int64, top+1)
	var cost int64
	for inserted, v32 := range instructions {
		v := int64(v32)
		less := prefix(tree, v-1)
		greater := int64(inserted) - prefix(tree, v)
		cost = (cost + min(less, greater)) % mod
		for i := v; i <= top; i += i & -i {
			tree[i]++
		}
	}
	return int32(cost)
}

var seed int64 = 1649

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int32, 60)
	for l := range lists {
		lists[l] = make([]int32, 100000)
		for i := range lists[l] {
			lists[l][i] = int32((nextRandom() * 32768 + nextRandom())%100000 + 1)
		}
	}
	var check, total int64
	for _, instructions := range lists {
		cost := int64(createSortedArray(instructions))
		total += cost
		check = (check*31 + cost + 1) % 1000000007
	}
	fmt.Printf("60 lists of 100000 instructions: costs sum to %d, checksum %d\n", total, check)
}
