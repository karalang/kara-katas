// LeetCode #1053: Previous Permutation With One Swap -- Go mirror of
// bench/prev_perm.kara.
package main

import "fmt"

var seed int64 = 1053

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func prevPermOpt1(arr []int64) []int64 {
	out := make([]int64, len(arr))
	copy(out, arr)
	n := len(out)
	i := n - 2
	for i >= 0 && out[i] <= out[i+1] {
		i--
	}
	if i < 0 {
		return out
	}
	j := n - 1
	for out[j] >= out[i] {
		j--
	}
	for out[j-1] == out[j] {
		j--
	}
	out[i], out[j] = out[j], out[i]
	return out
}

type entry struct {
	arr  []int64
	from int
}

func main() {
	const count, n, rounds = 200, 20000, 25
	all := make([]entry, 0, count)
	for a := 0; a < count; a++ {
		run := nextRandom()%(n-1) + 1
		arr := make([]int64, 0, n)
		for k := int64(0); k < n-run; k++ {
			arr = append(arr, nextRandom()%10000+1)
		}
		v := nextRandom()%1000 + 1
		for r := int64(0); r < run; r++ {
			arr = append(arr, v)
			v += nextRandom() % 3
		}
		all = append(all, entry{arr, int(n - run - 1)})
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, e := range all {
			answer := prevPermOpt1(e.arr)
			var h int64
			for k := e.from; k < n; k++ {
				h = (h*10007 + answer[k]) % 1000000007
			}
			total += answer[e.from]
			check = (check*131 + h) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: total %d, checksum %d\n", count, n, rounds, total, check)
}
