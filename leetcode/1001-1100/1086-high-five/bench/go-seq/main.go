// Benchmark: LeetCode #1086 High Five -- mirrors high_five.kara: the
// scores grouped by student (a map, its ids sorted, as Go has no ordered
// map), each student's sorted high to low and the first five averaged,
// over 200 lists of 1000 items built once.
package main

import (
	"fmt"
	"sort"
)

func highFive(items [][]int64) [][]int64 {
	scores := map[int64][]int64{}
	for _, item := range items {
		scores[item[0]] = append(scores[item[0]], item[1])
	}
	ids := make([]int64, 0, len(scores))
	for id := range scores {
		ids = append(ids, id)
	}
	sort.Slice(ids, func(a, b int) bool { return ids[a] < ids[b] })
	out := make([][]int64, 0, len(ids))
	for _, id := range ids {
		list := scores[id]
		sorted := make([]int64, len(list))
		copy(sorted, list)
		sort.Slice(sorted, func(a, b int) bool { return sorted[a] > sorted[b] })
		var top int64
		for j := 0; j < 5 && j < len(sorted); j++ {
			top += sorted[j]
		}
		out = append(out, []int64{id, top / 5})
	}
	return out
}

var seed int64 = 1086

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := int64(50)
	lists := make([][][]int64, 0, 200)
	for t := int64(0); t < 200; t++ {
		k := 50 + t%150
		ids := []int64{}
		taken := make([]bool, 1001)
		for int64(len(ids)) < k {
			id := nextRandom()%1000 + 1
			if !taken[id] {
				taken[id] = true
				ids = append(ids, id)
			}
		}
		items := make([][]int64, 0, 1000)
		for i := int64(0); i < 1000; i++ {
			var id int64
			if i < 5*k {
				id = ids[i%k]
			} else {
				id = ids[nextRandom()%k]
			}
			items = append(items, []int64{id, nextRandom() % 101})
		}
		for i := int64(len(items)) - 1; i >= 1; i-- {
			j := nextRandom() % (i + 1)
			items[i], items[j] = items[j], items[i]
		}
		lists = append(lists, items)
	}
	var students, check int64
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < 200; i++ {
			out := highFive(lists[(r*7+i)%200])
			students += int64(len(out))
			for _, row := range out {
				check = (check*31 + row[0]*101 + row[1]) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over 200 lists of 1000 items: %d students, checksum %d\n", rounds, students, check)
}
