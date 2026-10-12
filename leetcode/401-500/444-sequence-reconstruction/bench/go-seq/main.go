// Benchmark for #444: mirror of sequence_reconstruction.kara (positions
// and neighbouring pairs) on 50 random cases of n = 5,000, built once
// and answered 30 times over.
package main

import "fmt"

func sequenceReconstruction(nums []int64, sequences [][]int64) bool {
	n := int64(len(nums))
	position := make([]int64, n+1)
	for i := int64(0); i < n; i++ {
		position[nums[i]] = i
	}
	covered := make([]bool, n)
	for _, s := range sequences {
		for j := 1; j < len(s); j++ {
			a := position[s[j-1]]
			b := position[s[j]]
			if a >= b {
				return false
			}
			if b == a+1 {
				covered[a] = true
			}
		}
	}
	for i := int64(0); i < n-1; i++ {
		if !covered[i] {
			return false
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, n, rounds int64 = 50, 5000, 30
	seed := int64(444)
	casesNums := make([][]int64, 0, count)
	casesSequences := make([][][]int64, 0, count)
	values := int64(0)
	for c := int64(0); c < count; c++ {
		nums := make([]int64, n)
		for v := int64(1); v <= n; v++ {
			nums[v-1] = v
		}
		for i := n - 1; i > 0; i-- {
			j := nextRandom(&seed) % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		sequences := [][]int64{}
		windows := 1 + nextRandom(&seed)%(n*2+2)
		for w := int64(0); w < windows; w++ {
			start := nextRandom(&seed) % n
			length := 1 + nextRandom(&seed)%12
			end := start + length
			if end > n {
				end = n
			}
			s := []int64{}
			for k := start; k < end; k++ {
				if len(s) == 0 || nextRandom(&seed)%10 != 0 {
					s = append(s, nums[k])
				}
			}
			values += int64(len(s))
			sequences = append(sequences, s)
		}
		if c%2 == 0 {
			values += n
			sequences = append(sequences, append([]int64(nil), nums...))
		}
		casesNums = append(casesNums, nums)
		casesSequences = append(casesSequences, sequences)
	}
	trueCount := int64(0)
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		for c := int64(0); c < count; c++ {
			answer := sequenceReconstruction(casesNums[c], casesSequences[c])
			bit := int64(0)
			if answer {
				trueCount++
				bit = 1
			}
			checksum = (checksum*31 + c*2 + bit + round) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d cases of n = %d (%d values in sequences): %d true, checksum %d\n", rounds, count, n, values, trueCount, checksum)
}
