// LeetCode #1562: Find Latest Group of Size M -- bench: the ★ arm (group
// lengths kept at both ends, a count of groups of length m) over 20 random
// orders of 100000 positions, built once, each asked for m from 1 to 10.
// Go mirror of latest.kara.
package main

import "fmt"

func findLatestStep(arr []int64, m int64) int64 {
	n := int64(len(arr))
	length := make([]int64, n+2)
	var groupsOfM int64
	latest := int64(-1)
	for step, a := range arr {
		left := length[a-1]
		right := length[a+1]
		total := left + right + 1
		if left == m {
			groupsOfM--
		}
		if right == m {
			groupsOfM--
		}
		if total == m {
			groupsOfM++
		}
		length[a-left] = total
		length[a+right] = total
		if groupsOfM > 0 {
			latest = int64(step) + 1
		}
	}
	return latest
}

var seed int64 = 1562

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 100000
	orders := make([][]int64, 20)
	for o := range orders {
		arr := make([]int64, n)
		for i := range arr {
			arr[i] = int64(i) + 1
		}
		for i := int64(n - 1); i >= 1; i-- {
			j := nextRandom() * 32768
			j = (j + nextRandom()) % (i + 1)
			arr[i], arr[j] = arr[j], arr[i]
		}
		orders[o] = arr
	}
	var check, total int64
	for m := int64(1); m <= 10; m++ {
		for _, arr := range orders {
			step := findLatestStep(arr, m)
			total += step
			check = mix(check, step)
		}
	}
	fmt.Printf("m from 1 to 10 over 20 orders of 100000 positions: steps sum %d, checksum %d\n", total, check)
}
