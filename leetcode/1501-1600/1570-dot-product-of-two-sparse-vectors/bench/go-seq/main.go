// LeetCode #1570: Dot Product of Two Sparse Vectors -- bench: the ★ arm
// (index-ordered pairs merged by two pointers) over 20 vectors of 500000
// values, one in 10 of them from 1 to 100 and the rest 0, each made sparse
// once; then the product of every ordered pair of them, 400 products.
package main

import "fmt"

type pair struct{ index, value int64 }

type sparseVector struct{ pairs []pair }

func newSparseVector(nums []int64) sparseVector {
	v := sparseVector{}
	for i, x := range nums {
		if x != 0 {
			v.pairs = append(v.pairs, pair{int64(i), x})
		}
	}
	return v
}

func (v *sparseVector) dotProduct(other *sparseVector) int64 {
	i, j := 0, 0
	var total int64
	for i < len(v.pairs) && j < len(other.pairs) {
		a, b := v.pairs[i], other.pairs[j]
		if a.index == b.index {
			total += a.value * b.value
			i++
			j++
		} else if a.index < b.index {
			i++
		} else {
			j++
		}
	}
	return total
}

var seed int64 = 1570

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 500000
	vectors := make([]sparseVector, 0, 20)
	for v := 0; v < 20; v++ {
		nums := make([]int64, n)
		for i := range nums {
			draw := nextRandom()
			if draw%10 == 0 {
				nums[i] = draw/10%100 + 1
			}
		}
		vectors = append(vectors, newSparseVector(nums))
	}
	var check, total int64
	for i := range vectors {
		for j := range vectors {
			product := vectors[i].dotProduct(&vectors[j])
			total += product
			check = mix(check, product)
		}
	}
	fmt.Printf("400 products of 20 vectors of 500000 values: products sum %d, checksum %d\n", total, check)
}
