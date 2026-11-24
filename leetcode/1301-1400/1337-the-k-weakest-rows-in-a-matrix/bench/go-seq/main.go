// LeetCode #1337 bench, Go mirror of the Kāra bench: the ★ arm on 50
// matrices of 100 by 100 built once, then 2000 passes, each rewriting one
// row of every matrix and choosing k from the checksum so far, answering
// every matrix.
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type pair struct {
	soldiers int
	row      int
}

func soldiers(row []int32) int {
	low, high := 0, len(row)
	for low < high {
		mid := (low + high) / 2
		if row[mid] == 1 {
			low = mid + 1
		} else {
			high = mid
		}
	}
	return low
}

func kWeakestRows(mat [][]int32, k int) []int32 {
	rows := make([]pair, 0, len(mat))
	for i, row := range mat {
		rows = append(rows, pair{soldiers(row), i})
	}
	slices.SortFunc(rows, func(a, b pair) int {
		if c := cmp.Compare(a.soldiers, b.soldiers); c != 0 {
			return c
		}
		return cmp.Compare(a.row, b.row)
	})
	out := make([]int32, 0, k)
	for _, p := range rows[:min(k, len(rows))] {
		out = append(out, int32(p.row))
	}
	return out
}

var seed int64 = 1337

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100
	mats := make([][][]int32, 50)
	for t := range mats {
		mat := make([][]int32, n)
		for r := range mat {
			s := nextRandom() % (n + 1)
			row := make([]int32, n)
			for c := int64(0); c < s; c++ {
				row[c] = 1
			}
			mat[r] = row
		}
		mats[t] = mat
	}
	var check int64
	for pass := int64(0); pass < 2000; pass++ {
		k := int(1 + check%n)
		for t := 0; t < 50; t++ {
			r := check % n
			s := check / 7 % (n + 1)
			for c := int64(0); c < n; c++ {
				if c < s {
					mats[t][r][c] = 1
				} else {
					mats[t][r][c] = 0
				}
			}
			rows := kWeakestRows(mats[t], k)
			check = (check*31 + int64(rows[0]) + int64(rows[len(rows)-1]) + pass) % 1000000007
		}
	}
	fmt.Printf("2000 passes over 50 matrices of 100 by 100: checksum %d\n", check)
}
