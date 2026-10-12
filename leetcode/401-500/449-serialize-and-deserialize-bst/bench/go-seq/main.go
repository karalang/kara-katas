// Benchmark for #449: mirror of codec.kara (preorder, rebuilt with
// bounds) on 10 random search trees of 50,000 values, built once, then
// serialized and deserialized 20 times over.
package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

type TreeNode struct {
	val   int64
	left  *TreeNode
	right *TreeNode
}

func writePreorder(node *TreeNode, out *[]byte) {
	if node != nil {
		if len(*out) > 0 {
			*out = append(*out, ',')
		}
		*out = strconv.AppendInt(*out, node.val, 10)
		writePreorder(node.left, out)
		writePreorder(node.right, out)
	}
}

func serialize(root *TreeNode) string {
	out := []byte{}
	writePreorder(root, &out)
	return string(out)
}

// Builds the subtree of values from low to high, both inclusive, taking
// them from values[*at] onward.
func build(values []int64, at *int, low, high int64) *TreeNode {
	if *at == len(values) || values[*at] < low || values[*at] > high {
		return nil
	}
	v := values[*at]
	*at++
	left := build(values, at, low, v-1)
	right := build(values, at, v+1, high)
	return &TreeNode{v, left, right}
}

func deserialize(data string) *TreeNode {
	values := []int64{}
	if len(data) > 0 {
		for _, token := range strings.Split(data, ",") {
			v, err := strconv.ParseInt(token, 10, 64)
			if err != nil {
				panic("a number")
			}
			values = append(values, v)
		}
	}
	at := 0
	return build(values, &at, math.MinInt64, math.MaxInt64)
}

func insert(root *TreeNode, v int64) *TreeNode {
	fresh := &TreeNode{val: v}
	if root == nil {
		return fresh
	}
	node := root
	for {
		if v < node.val {
			if node.left == nil {
				node.left = fresh
				break
			}
			node = node.left
		} else {
			if node.right == nil {
				node.right = fresh
				break
			}
			node = node.right
		}
	}
	return root
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const trees, n, rounds = 10, 50000, 20
	seed := int64(449)
	roots := []*TreeNode{}
	for t := int64(0); t < trees; t++ {
		// A shuffle of 0 to n - 1, spread out and shifted per tree.
		values := make([]int64, n)
		for i := int64(0); i < n; i++ {
			values[i] = i*3 + t
		}
		for i := int64(0); i < n; i++ {
			r := nextRandom(&seed) * 32768
			r += nextRandom(&seed)
			j := i + r%(n-i)
			values[i], values[j] = values[j], values[i]
		}
		var root *TreeNode
		for _, v := range values {
			root = insert(root, v)
		}
		roots = append(roots, root)
	}
	characters, checksum := int64(0), int64(0)
	for round := 0; round < rounds; round++ {
		for _, root := range roots {
			text := serialize(root)
			back := deserialize(text)
			top := int64(-1)
			if back != nil {
				top = back.val
			}
			characters += int64(len(text))
			checksum = (checksum*31 + int64(len(text)) + top) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d trees of %d: %d characters, checksum %d\n", rounds, trees, n, characters, checksum)
}
