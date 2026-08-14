// Benchmark workload for LeetCode #272 — Closest Binary Search Tree Value II.
//
// Algorithm-for-algorithm mirror of ../k_closest.kara. See that file's header
// for what this lane measures and for the three parity decisions (hoisted
// stacks, each language's own absolute value, targets that span the value
// range).
package main

import (
	"fmt"
	"math"
)

func main() {
	const nodeCount int64 = 30000
	const targetCount int64 = 100000
	const k int64 = 8
	const rounds int64 = 10
	const span int64 = 1000000

	val := make([]int64, 0, nodeCount)
	left := make([]int64, 0, nodeCount)
	right := make([]int64, 0, nodeCount)
	var state int64 = 272272
	var placed, tries int64
	for placed < nodeCount && tries < nodeCount*4 {
		state = (state*1103515245 + 12345) & 2147483647
		v := (state / 256) % span
		tries++
		if len(val) == 0 {
			val = append(val, v)
			left = append(left, -1)
			right = append(right, -1)
			placed++
		} else {
			var cur int64 = 0
			dup, done := false, false
			for !done {
				if v == val[cur] {
					dup = true
					done = true
				} else if v < val[cur] {
					if left[cur] < 0 {
						val = append(val, v)
						left = append(left, -1)
						right = append(right, -1)
						left[cur] = int64(len(val)) - 1
						done = true
					} else {
						cur = left[cur]
					}
				} else if right[cur] < 0 {
					val = append(val, v)
					left = append(left, -1)
					right = append(right, -1)
					right[cur] = int64(len(val)) - 1
					done = true
				} else {
					cur = right[cur]
				}
			}
			if !dup {
				placed++
			}
		}
	}
	n := int64(len(val))

	targets := make([]float64, 0, targetCount)
	var tmin, tmax float64
	for t := int64(0); t < targetCount; t++ {
		state = (state*1103515245 + 12345) & 2147483647
		whole := (state / 256) % span
		state = (state*1103515245 + 12345) & 2147483647
		frac := float64((state/256)%1000) / 1000.0
		x := float64(whole) + frac
		if t == 0 {
			tmin, tmax = x, x
		}
		if x < tmin {
			tmin = x
		}
		if x > tmax {
			tmax = x
		}
		targets = append(targets, x)
	}

	const depthCap = 256
	pred := make([]int64, depthCap)
	succ := make([]int64, depthCap)
	lower := make([]int64, k)
	upper := make([]int64, k)
	outv := make([]int64, k)

	var sink int64
	for r := int64(0); r < rounds; r++ {
		for q := int64(0); q < targetCount; q++ {
			target := targets[q]

			var pt, st, cur int64
			for cur >= 0 {
				if float64(val[cur]) < target {
					pred[pt] = cur
					pt++
					cur = right[cur]
				} else {
					succ[st] = cur
					st++
					cur = left[cur]
				}
			}

			var nl, nu, taken int64
			for taken < k && (pt > 0 || st > 0) {
				takePred := pt > 0
				if pt > 0 && st > 0 {
					dp := math.Abs(float64(val[pred[pt-1]]) - target)
					ds := math.Abs(float64(val[succ[st-1]]) - target)
					takePred = dp <= ds
				}
				if takePred {
					pt--
					node := pred[pt]
					c := left[node]
					for c >= 0 {
						pred[pt] = c
						pt++
						c = right[c]
					}
					lower[nl] = val[node]
					nl++
				} else {
					st--
					node := succ[st]
					c := right[node]
					for c >= 0 {
						succ[st] = c
						st++
						c = left[c]
					}
					upper[nu] = val[node]
					nu++
				}
				taken++
			}

			var w int64
			for i := nl - 1; i >= 0; i-- {
				outv[w] = lower[i]
				w++
			}
			for j := int64(0); j < nu; j++ {
				outv[w] = upper[j]
				w++
			}

			var acc int64
			for p := int64(0); p < w; p++ {
				acc = (acc*31 + outv[p]) % 1000000007
			}
			sink = (sink*131 + acc) % 1000000007
		}
	}

	vlo, vhi := val[0], val[0]
	for m := int64(1); m < n; m++ {
		if val[m] < vlo {
			vlo = val[m]
		}
		if val[m] > vhi {
			vhi = val[m]
		}
	}
	fmt.Println(sink)
	fmt.Printf("nodes %d values %d..%d targets %d..%d\n", n, vlo, vhi, int64(tmin), int64(tmax))
}
