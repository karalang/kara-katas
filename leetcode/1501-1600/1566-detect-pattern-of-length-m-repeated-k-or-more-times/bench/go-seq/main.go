// LeetCode #1566: Detect Pattern of Length M Repeated K or More Times --
// bench: the ★ arm (a run of agreements m apart) over 20 arrays of 100000
// values of 1 to 100, built once, half with a pattern planted near the
// end, each asked for m from 1 to 50 with k of 3.
// Go mirror of pattern.kara.
package main

import "fmt"

func containsPattern(arr []int64, m, k int64) bool {
	var run int64
	for i := int64(0); i < int64(len(arr))-m; i++ {
		if arr[i] == arr[i+m] {
			run++
			if run == m*(k-1) {
				return true
			}
		} else {
			run = 0
		}
	}
	return false
}

var seed int64 = 1566

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 100000
	arrays := make([][]int64, 20)
	for a := int64(0); a < 20; a++ {
		arr := make([]int64, n)
		for i := range arr {
			arr[i] = nextRandom()%100 + 1
		}
		if a%2 == 1 {
			m := 1 + a%50
			start := n - 3*m - nextRandom()%100
			for i := m; i < 3*m; i++ {
				arr[start+i] = arr[start+i%m]
			}
		}
		arrays[a] = arr
	}
	var check, found int64
	for m := int64(1); m <= 50; m++ {
		for a, arr := range arrays {
			yes := containsPattern(arr, m, 3)
			if yes {
				found++
				check = mix(check, m*100+int64(a))
			} else {
				check = mix(check, 0)
			}
		}
	}
	fmt.Printf("m from 1 to 50 over 20 arrays of 100000 values: %d with a pattern, checksum %d\n", found, check)
}
