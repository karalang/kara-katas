// Benchmark for #606: Go mirror of the ★ arm (write it out); see
// ../tree2str.kara. The string is a `strings.Builder`, and each value
// is formatted into a string of its own before it is appended, as the
// Kāra arm's `f"{node.val}"` is.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func write(node *TreeNode, out *strings.Builder) {
	out.WriteString(strconv.FormatInt(node.Val, 10))
	if node.Left != nil || node.Right != nil {
		out.WriteByte('(')
		if node.Left != nil {
			write(node.Left, out)
		}
		out.WriteByte(')')
	}
	if node.Right != nil {
		out.WriteByte('(')
		write(node.Right, out)
		out.WriteByte(')')
	}
}

func tree2str(root *TreeNode) string {
	var out strings.Builder
	if root != nil {
		write(root, &out)
	}
	return out.String()
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const trees, rounds = 20, 200
	seed := int64(606)
	all := make([][]*TreeNode, 0, trees)
	for g := int64(0); g < trees; g++ {
		lean := 50 + 2*g
		root := &TreeNode{Val: nextRandom(&seed)%2001 - 1000}
		nodes := []*TreeNode{root}
		for i := 1; i < 10000; i++ {
			c := &TreeNode{Val: nextRandom(&seed)%2001 - 1000}
			node := root
			for {
				if nextRandom(&seed)%100 < lean {
					if node.Left != nil {
						node = node.Left
					} else {
						node.Left = c
						break
					}
				} else {
					if node.Right != nil {
						node = node.Right
					} else {
						node.Right = c
						break
					}
				}
			}
			nodes = append(nodes, c)
		}
		all = append(all, nodes)
	}
	length := 0
	var checksum int64
	for r := int64(0); r < rounds; r++ {
		for t := int64(0); t < trees; t++ {
			k := (r*37 + t*11) % 16
			s := tree2str(all[t][k])
			length += len(s)
			for i := 0; i < len(s); i++ {
				if i%101 == 0 {
					checksum = (checksum*31 + int64(s[i])) % 1000000007
				}
			}
		}
	}
	fmt.Printf("%d trees, %d times each: %d characters, checksum %d\n", trees, rounds, length, checksum)
}
