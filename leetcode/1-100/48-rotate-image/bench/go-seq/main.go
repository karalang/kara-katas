// LeetCode #48 bench mirror — Go, the in-place layer four-way cyclic rotation (★).
//
// Mirrors bench/rotate_image.kara: rotate a fixed n=20 matrix 90° clockwise IN PLACE by cycling
// four cells at a time (one temporary — the four-target parallel assignment is Kāra-only), TOTAL
// times with the state carrying forward; one cell punched per iteration, folding a position-
// weighted per-cell signature into a rolling checksum. Same workload + checksum as every mirror.
package main

import "fmt"

func rotate(m [][]int64) {
	n := len(m)
	for i := 0; i < n/2; i++ {
		for j := i; j < n-1-i; j++ {
			tmp := m[i][j]
			m[i][j] = m[n-1-j][i]
			m[n-1-j][i] = m[n-1-i][n-1-j]
			m[n-1-i][n-1-j] = m[j][n-1-i]
			m[j][n-1-i] = tmp
		}
	}
}

func main() {
	var total int64 = 40000
	var modulus int64 = 1000000007
	n := 20

	m := make([][]int64, n)
	for a := 0; a < n; a++ {
		m[a] = make([]int64, n)
		for b := 0; b < n; b++ {
			m[a][b] = int64((a*7 + b*13) % 97)
		}
	}

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		kk := int(k)
		m[kk%n][(kk*7)%n] = k % 97
		rotate(m)

		var sig int64 = 0
		for i := 0; i < n; i++ {
			row := m[i]
			for j := 0; j < n; j++ {
				sig = (sig*31 + row[j]*int64(i*n+j+1)) % modulus
			}
		}
		acc = (acc*131 + sig) % modulus
	}

	fmt.Println(acc)
}
