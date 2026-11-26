// LeetCode #1418: the bench in Go, mirroring display_table.kara. Go has
// no ordered map: each table's counts in a map, the tables and the dishes
// then sorted.
package main

import (
	"fmt"
	"sort"
	"strconv"
)

func displayTable(orders [][]string) [][]string {
	tables := map[int64]map[string]int64{}
	foods := map[string]bool{}
	for _, order := range orders {
		table, _ := strconv.ParseInt(order[1], 10, 64)
		foods[order[2]] = true
		counts, ok := tables[table]
		if !ok {
			counts = map[string]int64{}
			tables[table] = counts
		}
		counts[order[2]]++
	}
	names := make([]string, 0, len(foods))
	for f := range foods {
		names = append(names, f)
	}
	sort.Strings(names)
	numbers := make([]int64, 0, len(tables))
	for t := range tables {
		numbers = append(numbers, t)
	}
	sort.Slice(numbers, func(i, j int) bool { return numbers[i] < numbers[j] })
	header := append([]string{"Table"}, names...)
	out := [][]string{header}
	for _, t := range numbers {
		counts := tables[t]
		row := []string{strconv.FormatInt(t, 10)}
		for _, f := range names {
			row = append(row, strconv.FormatInt(counts[f], 10))
		}
		out = append(out, row)
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var seed int64 = 1418
	letters := []byte("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
	dishes := []string{}
	for i := 0; i < 30; i++ {
		n := 1 + nextRandom(&seed)%20
		s := []byte{}
		for j := int64(0); j < n; j++ {
			r := nextRandom(&seed)
			if r%6 == 0 {
				s = append(s, ' ')
			} else {
				s = append(s, letters[r/6%52])
			}
		}
		dishes = append(dishes, string(s))
	}
	pool := make([][]string, 0, 200000)
	for i := 0; i < 200000; i++ {
		r := nextRandom(&seed)
		food := dishes[nextRandom(&seed)%30]
		pool = append(pool, []string{fmt.Sprintf("guest%d", r%100), strconv.FormatInt(1+r/100%500, 10), food})
	}
	var check int64
	for i := 0; i < 100; i++ {
		start := nextRandom(&seed) % 150001
		table := displayTable(pool[start : start+50000])
		for _, row := range table {
			for _, cell := range row {
				for j := 0; j < len(cell); j++ {
					check = (check*131 + int64(cell[j])) % 1000000007
				}
				check = (check*131 + 7) % 1000000007
			}
		}
	}
	fmt.Printf("100 windows of 5 * 10^4 orders: checksum %d\n", check)
}
