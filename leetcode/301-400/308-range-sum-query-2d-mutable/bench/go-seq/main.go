// Benchmark mirror — LeetCode 308, Range Sum Query 2D (Mutable).
// Same 2D Fenwick tree, same LCG-generated operation script, same masked sink
// as fenwick2d.kara. See ../../README.md § Benchmarks.
package main

import "fmt"

func main() {
	const n int64 = 256
	const stride int64 = n + 1
	const ops int64 = 100000
	const passes int64 = 54

	tree := make([]int64, (n+1)*stride)
	data := make([]int64, n*n)
	kind := make([]int64, ops)
	o1 := make([]int64, ops)
	o2 := make([]int64, ops)
	o3 := make([]int64, ops)
	o4 := make([]int64, ops)

	state := int64(20308)
	for k := int64(0); k < ops; k++ {
		state = (state*1103515245 + 12345) % 2147483648
		t := state % 2
		state = (state*1103515245 + 12345) % 2147483648
		a := state % n
		state = (state*1103515245 + 12345) % 2147483648
		b := state % n
		state = (state*1103515245 + 12345) % 2147483648
		c := state % n
		state = (state*1103515245 + 12345) % 2147483648
		d := state % n
		kind[k] = t
		if t == 0 {
			o1[k], o2[k], o3[k], o4[k] = a, b, c%2001-1000, 0
		} else {
			if a <= c {
				o1[k], o3[k] = a, c
			} else {
				o1[k], o3[k] = c, a
			}
			if b <= d {
				o2[k], o4[k] = b, d
			} else {
				o2[k], o4[k] = d, b
			}
		}
	}

	var checksum int64
	for p := int64(0); p < passes; p++ {
		for k := int64(0); k < ops; k++ {
			if kind[k] == 0 {
				r, c := o1[k], o2[k]
				delta := o3[k] - data[r*n+c]
				data[r*n+c] = o3[k]
				for x := r + 1; x <= n; x += x & -x {
					for y := c + 1; y <= n; y += y & -y {
						tree[x*stride+y] += delta
					}
				}
			} else {
				r1, c1, r2, c2 := o1[k], o2[k], o3[k]+1, o4[k]+1
				var total int64
				for qi := int64(0); qi < 4; qi++ {
					px, py, sign := r2, c2, int64(1)
					if qi == 1 {
						px, sign = r1, -1
					}
					if qi == 2 {
						py, sign = c1, -1
					}
					if qi == 3 {
						px, py = r1, c1
					}
					var sub int64
					for x := px; x > 0; x -= x & -x {
						for y := py; y > 0; y -= y & -y {
							sub += tree[x*stride+y]
						}
					}
					total += sign * sub
				}
				checksum = (checksum + total) & 0x3FFFFFFF
			}
		}
	}
	fmt.Printf("checksum %d\n", checksum)
}
