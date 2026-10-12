// Benchmark for #453: mirror of min_moves.kara (the ★ arm, sum minus n
// times the minimum) on the same workload.
package main

import "fmt"

func minMoves(nums []int64) int64 {
	smallest := nums[0]
	var total int64
	for _, x := range nums {
		smallest = min(smallest, x)
		total += x
	}
	return total - int64(len(nums))*smallest
}

// ---- benchmark --------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomValue(seed *int64) int64 {
	hi := nextRandom(seed)
	lo := nextRandom(seed)
	return (hi*65536+lo)%2000000001 - 1000000000
}

func main() {
	const arrays = 10
	const n = 1000000
	const rounds = 20
	var seed int64 = 453
	all := make([][]int64, 0, arrays)
	for a := 0; a < arrays; a++ {
		nums := make([]int64, 0)
		for i := 0; i < n; i++ {
			nums = append(nums, randomValue(&seed))
		}
		all = append(all, nums)
	}
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		for a := 0; a < arrays; a++ {
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			at := (hi*65536 + lo) % n
			all[a][at] = randomValue(&seed)
			moves := minMoves(all[a])
			total += moves
			checksum = (checksum*31 + moves%1000000007) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d arrays of %d: %d moves, checksum %d\n", rounds, arrays, n, total, checksum)
}
