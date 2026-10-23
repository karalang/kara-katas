// LeetCode #898 bench: the table arm (the ★ arm with a hash table of its
// own) on 12 arrays of 50,000 numbers, LeetCode's largest, each a random
// number below 2^30 AND-ed with a second, so that about a quarter of the
// bits are set. The ORs ending at each place are kept in a short list,
// and every one is gathered into an open-addressing hash table written
// here, with no library set, map or sort. The same algorithm as
// subarray_bitwise_ors.kara.
package main

import "fmt"

type Table struct {
	slots []int64
	count int64
}

func insert(t *Table, v int64) {
	mask := int64(len(t.slots)) - 1
	i := ((v * 2654435761) % 4294967296) & mask
	for t.slots[i] != -1 {
		if t.slots[i] == v {
			return
		}
		i = (i + 1) & mask
	}
	t.slots[i] = v
	t.count++
	if t.count*2 > int64(len(t.slots)) {
		old := t.slots
		t.slots = make([]int64, len(old)*2)
		for k := range t.slots {
			t.slots[k] = -1
		}
		t.count = 0
		for _, w := range old {
			if w != -1 {
				insert(t, w)
			}
		}
	}
}

func subarrayBitwiseORs(arr []int64) int64 {
	table := &Table{slots: make([]int64, 64)}
	for k := range table.slots {
		table.slots[k] = -1
	}
	var ending []int64
	for _, x := range arr {
		next := []int64{x}
		for _, y := range ending {
			v := y | x
			if v != next[len(next)-1] {
				next = append(next, v)
			}
		}
		for _, v := range next {
			insert(table, v)
		}
		ending = next
	}
	return table.count
}

var seed int64 = 898

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var total, check int64
	for r := 0; r < 12; r++ {
		arr := make([]int64, 0, 50000)
		for i := 0; i < 50000; i++ {
			a := nextRandom() * 32768
			a += nextRandom()
			b := nextRandom() * 32768
			b += nextRandom()
			arr = append(arr, a&b)
		}
		got := subarrayBitwiseORs(arr)
		total += got
		check = (check*131 + got) % 1000000007
	}
	fmt.Printf("12 arrays of 50000 numbers: %d ORs in all, checksum %d\n", total, check)
}
