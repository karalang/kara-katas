// LeetCode #1640: Check Array Formation Through Concatenation -- the
// bench's Go mirror: the ★ arm on 50000 random cases of the values 1 to
// 100 in a random order, cut into pieces of 1 to 3 and shuffled, every
// third one with two values swapped, all drawn first.
package main

import "fmt"

func canFormArray(arr []int32, pieces [][]int32) bool {
	starting := map[int32]int{}
	for k, piece := range pieces {
		starting[piece[0]] = k
	}
	i := 0
	for i < len(arr) {
		k, ok := starting[arr[i]]
		if !ok {
			return false
		}
		for _, value := range pieces[k] {
			if i >= len(arr) || arr[i] != value {
				return false
			}
			i++
		}
	}
	return true
}

var seed int64 = 1640

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type testCase struct {
		arr    []int32
		pieces [][]int32
	}
	cases := make([]testCase, 0, 50000)
	for c := 0; c < 50000; c++ {
		arr := make([]int32, 100)
		for i := range arr {
			arr[i] = int32(i + 1)
		}
		for k := 99; k >= 1; k-- {
			j := nextRandom() % int64(k+1)
			arr[k], arr[j] = arr[j], arr[k]
		}
		var pieces [][]int32
		start := 0
		for start < 100 {
			end := min(100, start+int(nextRandom()%3+1))
			pieces = append(pieces, append([]int32(nil), arr[start:end]...))
			start = end
		}
		for k := len(pieces) - 1; k >= 1; k-- {
			j := nextRandom() % int64(k+1)
			pieces[k], pieces[j] = pieces[j], pieces[k]
		}
		if c%3 == 2 {
			a, b := nextRandom()%100, nextRandom()%100
			arr[a], arr[b] = arr[b], arr[a]
		}
		cases = append(cases, testCase{arr, pieces})
	}
	var check int64
	trues := 0
	for _, tc := range cases {
		formed := canFormArray(tc.arr, tc.pieces)
		bit := int64(1)
		if formed {
			trues++
			bit = 2
		}
		check = (check*31 + bit) % 1000000007
	}
	fmt.Printf("50000 cases of 100 values: %d can be formed, checksum %d\n", trues, check)
}
