// Benchmark for #433: mirror of min_mutation.kara (breadth first,
// generating neighbours).
package main

import (
	"fmt"
	"os"
	"strconv"
)

func minMutation(startGene, endGene string, bank []string) int64 {
	unreached := map[string]bool{}
	for _, gene := range bank {
		unreached[gene] = true
	}
	if !unreached[endGene] {
		return -1
	}
	delete(unreached, startGene)
	level := []string{startGene}
	var steps int64
	letters := []byte{'A', 'C', 'G', 'T'}
	for len(level) > 0 {
		var next []string
		for _, gene := range level {
			if gene == endGene {
				return steps
			}
			for i := 0; i < len(gene); i++ {
				for _, c := range letters {
					if c != gene[i] {
						b := []byte(gene)
						b[i] = c
						mutant := string(b)
						if unreached[mutant] {
							delete(unreached, mutant)
							next = append(next, mutant)
						}
					}
				}
			}
		}
		level = next
		steps++
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func mutate(gene string, seed *int64) string {
	at := nextRandom(seed) % 8
	shift := 1 + nextRandom(seed)%3
	letters := "ACGT"
	b := []byte(gene)
	k := int64(0)
	switch b[at] {
	case 'C':
		k = 1
	case 'G':
		k = 2
	case 'T':
		k = 3
	}
	b[at] = letters[(k+shift)%4]
	return string(b)
}

func main() {
	size := int64(1000)
	searches := int64(2000)
	if len(os.Args) > 1 {
		searches, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	seed := int64(433)
	bank := []string{"ACGTACGT"}
	for int64(len(bank)) < size {
		parent := bank[nextRandom(&seed)%int64(len(bank))]
		bank = append(bank, mutate(parent, &seed))
	}
	var reachable, checksum int64
	for s := int64(0); s < searches; s++ {
		start := mutate(bank[nextRandom(&seed)%size], &seed)
		end := bank[nextRandom(&seed)%size]
		answer := minMutation(start, end, bank)
		if answer >= 0 {
			reachable++
		}
		checksum = (checksum*31 + answer + 2) % 1000000007
	}
	fmt.Printf("%d searches in a bank of %d: %d reachable, checksum %d\n", searches, size, reachable, checksum)
}
