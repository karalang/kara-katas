// LeetCode #1299 bench: the ★ arm (one walk from the right end, each place
// given the greatest seen so far) over 50 arrays of 10^4 numbers up to 10^5,
// built once; then 1000 passes, each setting one number of every array from the
// checksum so far, answering it, and folding two of its answers, chosen by the
// checksum, into the checksum.
package main

import "fmt"

func replaceElements(arr []int64) []int64 {
	n := len(arr)
	out := make([]int64, n)
	var greatest int64 = -1
	for i := n - 1; i >= 0; i-- {
		out[i] = greatest
		if arr[i] > greatest {
			greatest = arr[i]
		}
	}
	return out
}

var seed int64 = 1299

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := [][]int64{}
	for t := 0; t < 50; t++ {
		arr := []int64{}
		for j := 0; j < 10000; j++ {
			hi := nextRandom()
			arr = append(arr, 1+(hi*32768+nextRandom())%100000)
		}
		arrays = append(arrays, arr)
	}
	var check int64
	for p := int64(0); p < 1000; p++ {
		for _, arr := range arrays {
			arr[check%10000] = 1 + check*7919%100000
			out := replaceElements(arr)
			check = (check*31 + out[check%10000] + out[(check/7)%10000] + p) % 1000000007
		}
	}
	fmt.Printf("1000 passes over 50 arrays of 10^4: checksum %d\n", check)
}
