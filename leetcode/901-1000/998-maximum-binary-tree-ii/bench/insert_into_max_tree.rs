// Benchmark: LeetCode #998 Maximum Binary Tree II -- the ★ arm, down the
// right spine by recursion, on maximum trees of 99 values, LeetCode's
// largest. Mirrors insert_into_max_tree.kara, .c, .py and go-seq/. The
// tree is LeetCode's Rust shape, `Option<Rc<RefCell<TreeNode>>>`,
// reference counted as Kāra's `shared struct` is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;
type Tree = Option<Node>;

fn new_node(val: i64, left: Tree, right: Tree) -> Node {
    Rc::new(RefCell::new(TreeNode { val, left, right }))
}

fn insert_into_max_tree(root: Tree, val: i64) -> Tree {
    match root {
        Some(node) => {
            if val > node.borrow().val {
                Some(new_node(val, Some(node), None))
            } else {
                let right = node.borrow_mut().right.take();
                node.borrow_mut().right = insert_into_max_tree(right, val);
                Some(node)
            }
        }
        None => Some(new_node(val, None, None)),
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn build(a: &[i64], lo: usize, hi: usize) -> Tree {
    if lo >= hi {
        return None;
    }
    let mut m = lo;
    for i in lo + 1..hi {
        if a[i] > a[m] {
            m = i;
        }
    }
    Some(new_node(a[m], build(a, lo, m), build(a, m + 1, hi)))
}

// Take val out again, from where the insert put it on the right spine,
// and return the tree as it was with how deep val sat.
fn take_out(root: Node, val: i64) -> (Node, i64) {
    if root.borrow().val == val {
        let left = root.borrow_mut().left.take().unwrap();
        return (left, 0);
    }
    let mut above = root.clone();
    let mut depth = 1;
    loop {
        let next = above.borrow().right.clone().unwrap();
        if next.borrow().val == val {
            let below = next.borrow_mut().left.take();
            above.borrow_mut().right = below;
            return (root, depth);
        }
        above = next;
        depth += 1;
    }
}

fn main() {
    let rounds: i64 = 100000;
    let mut seed = 998;
    // 20 trees of the 99 values from 1 to 100 but one: the even ones in a
    // random order, the odd ones falling, which makes a chain of 99
    let mut trees: Vec<Node> = Vec::new();
    let mut vals: Vec<i64> = Vec::new();
    for t in 0..20 {
        let val = 1 + next_random(&mut seed) % 100;
        let mut a: Vec<i64> = (0..100).map(|v| 100 - v).filter(|&v| v != val).collect();
        if t % 2 == 0 {
            let mut i = 98;
            while i > 0 {
                let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
                a.swap(i, j);
                i -= 1;
            }
        }
        trees.push(build(&a, 0, 99).unwrap());
        vals.push(val);
    }
    let mut depths: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let k = ((r + i) % 20) as usize;
            let got = insert_into_max_tree(Some(trees[k].clone()), vals[k]).unwrap();
            let (tree, depth) = take_out(got, vals[k]);
            trees[k] = tree;
            depths += depth;
            check = (check * 31 + depth + 1) % 1000000007;
        }
    }
    println!("{} rounds over 20 trees of 99 values: depth total {}, checksum {}", rounds, depths, check);
}
