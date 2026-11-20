// LeetCode #1720: Decode XORed Array -- the bench (decode.kara): each
// value the one before it XORed with the code between them.
package main

import "fmt"

func decode(encoded []int32, first int32) []int32 {
	arr := make([]int32, 0, len(encoded)+1)
	arr = append(arr, first)
	for _, e := range encoded {
		arr = append(arr, arr[len(arr)-1]^e)
	}
	return arr
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func main() {
	count := 200
	var rounds int64 = 100
	n := 10000
	var seed int64 = 1720
	encoded := make([][]int32, count)
	firsts := make([]int32, count)
	for c := 0; c < count; c++ {
		encoded[c] = make([]int32, n)
		for i := range encoded[c] {
			encoded[c][i] = int32(wide(&seed) % 100001)
		}
		firsts[c] = int32(wide(&seed) % 100001)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			arr := decode(encoded[c], firsts[c])
			sum += int64(arr[n])
			check = (check*31 + int64(arr[n/2]) + int64(arr[n]) + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d codes, %d rounds: last values sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
