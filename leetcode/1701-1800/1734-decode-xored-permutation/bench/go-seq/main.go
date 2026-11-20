// LeetCode #1734: Decode XORed Permutation -- the bench (decode.kara): the
// first value from the XOR of 1 to n less that of the codes at odd places,
// then each next value the last XORed with its code.
package main

import "fmt"

func decode(encoded []int32) []int32 {
	n := len(encoded) + 1
	var all int32
	for v := 1; v <= n; v++ {
		all ^= int32(v)
	}
	var rest int32
	for i := 1; i < n-1; i += 2 {
		rest ^= encoded[i]
	}
	perm := make([]int32, 0, n)
	perm = append(perm, all^rest)
	for _, code := range encoded {
		perm = append(perm, perm[len(perm)-1]^code)
	}
	return perm
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
	count := 50
	var rounds int64 = 40
	n := 99999
	var seed int64 = 1734
	problems := make([][]int32, 0, count)
	for p := 0; p < count; p++ {
		perm := make([]int32, n)
		for v := 0; v < n; v++ {
			perm[v] = int32(v + 1)
		}
		for i := n - 1; i >= 1; i-- {
			j := wide(&seed) % int64(i+1)
			perm[i], perm[j] = perm[j], perm[i]
		}
		encoded := make([]int32, n-1)
		for i := 0; i < n-1; i++ {
			encoded[i] = perm[i] ^ perm[i+1]
		}
		problems = append(problems, encoded)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, encoded := range problems {
			perm := decode(encoded)
			sum += int64(perm[0])
			check = (check*31 + int64(perm[0]) + int64(perm[n/2]) + int64(perm[n-1]) + r) % 1000000007
		}
	}
	fmt.Printf("%d permutations of %d, %d rounds: first values sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
