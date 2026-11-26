package main

import "fmt"

// The Go mirror of count_triplets.kara: a fresh map for every array, as the
// Kara arm makes a fresh Map.
func countTriplets(arr []int32) int32 {
	seen := map[int32][2]int64{0: {1, 0}}
	x := int32(0)
	count := int64(0)
	for k, a := range arr {
		x ^= a
		got := seen[x]
		count += got[0]*int64(k) - got[1]
		seen[x] = [2]int64{got[0] + 1, got[1] + int64(k) + 1}
	}
	return int32(count)
}

func main() {
	seed := int64(1442)
	arrays := make([][]int32, 2000)
	for a := range arrays {
		arr := make([]int32, 300)
		for i := range arr {
			seed = (seed*1103515245 + 12345) % 2147483648
			arr[i] = int32(1 + seed/65536%1023)
		}
		arrays[a] = arr
	}
	check := int64(0)
	for r := 0; r < 50; r++ {
		for _, arr := range arrays {
			check = (check*131 + int64(countTriplets(arr))) % 1000000007
		}
	}
	fmt.Printf("10^5 arrays of 300: checksum %d\n", check)
}
