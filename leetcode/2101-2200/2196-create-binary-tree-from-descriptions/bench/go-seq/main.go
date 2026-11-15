// benchmark's Go mirror of create.kara (LeetCode #2196, the ★ arm): a map
// of nodes made as named, a set of children.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func nodeOf(nodes map[int64]*TreeNode, v int64) *TreeNode {
	if n, ok := nodes[v]; ok {
		return n
	}
	n := &TreeNode{val: v}
	nodes[v] = n
	return n
}

func createBinaryTree(descriptions [][3]int64) *TreeNode {
	nodes := map[int64]*TreeNode{}
	children := map[int64]struct{}{}
	for _, d := range descriptions {
		parent := nodeOf(nodes, d[0])
		child := nodeOf(nodes, d[1])
		if d[2] == 1 {
			parent.left = child
		} else {
			parent.right = child
		}
		children[d[1]] = struct{}{}
	}
	for _, d := range descriptions {
		if _, ok := children[d[0]]; !ok {
			return nodes[d[0]]
		}
	}
	return nil
}

var seed int64 = 2196

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func randomDescriptions() [][3]int64 {
	n := 10001
	values := make([]int64, 100000)
	for i := range values {
		values[i] = int64(i + 1)
	}
	for i := 0; i < n; i++ {
		j := i + int(wideRandom()%int64(100000-i))
		values[i], values[j] = values[j], values[i]
	}
	type slot struct {
		p    int
		side int64
	}
	free := []slot{{0, 1}, {0, 0}}
	descriptions := [][3]int64{}
	for k := 1; k < n; k++ {
		pick := int(wideRandom() % int64(len(free)))
		s := free[pick]
		free[pick] = free[len(free)-1]
		free = free[:len(free)-1]
		descriptions = append(descriptions, [3]int64{values[s.p], values[k], s.side})
		free = append(free, slot{k, 1}, slot{k, 0})
	}
	for i := len(descriptions) - 1; i > 0; i-- {
		j := int(wideRandom() % int64(i+1))
		descriptions[i], descriptions[j] = descriptions[j], descriptions[i]
	}
	return descriptions
}

func weigh(root *TreeNode) (int64, int64) {
	type entry struct {
		n     *TreeNode
		depth int64
	}
	stack := []entry{}
	if root != nil {
		stack = append(stack, entry{root, 1})
	}
	var count, weight int64
	for len(stack) > 0 {
		e := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		count++
		weight += e.n.val * e.depth
		if e.n.left != nil {
			stack = append(stack, entry{e.n.left, e.depth + 1})
		}
		if e.n.right != nil {
			stack = append(stack, entry{e.n.right, e.depth + 1})
		}
	}
	return count, weight
}

func main() {
	sets := [][][3]int64{}
	for i := 0; i < 20; i++ {
		sets = append(sets, randomDescriptions())
	}
	var check int64
	for pass := 0; pass < 50; pass++ {
		for _, d := range sets {
			count, weight := weigh(createBinaryTree(d))
			check = (check*31 + count + weight%1000000007) % 1000000007
		}
	}
	fmt.Printf("50 passes over 20 trees: checksum %d\n", check)
}
