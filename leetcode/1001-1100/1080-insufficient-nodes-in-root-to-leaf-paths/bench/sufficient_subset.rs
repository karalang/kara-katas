// Benchmark: LeetCode #1080 Insufficient Nodes in Root to Leaf Paths --
// the ★ arm. Mirrors sufficient_subset.kara, .c, .py and go-seq/. The
// tree is LeetCode's Rust shape, `Option<Rc<RefCell<TreeNode>>>`,
// reference counted as Kāra's `shared struct` is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Tree = Option<Rc<RefCell<TreeNode>>>;

fn prune(node: Tree, need: i64) -> Tree {
    let n = node?;
    {
        let mut b = n.borrow_mut();
        if b.left.is_none() && b.right.is_none() {
            return if b.val as i64 >= need { drop(b); Some(n) } else { None };
        }
        let rest = need - b.val as i64;
        b.left = prune(b.left.take(), rest);
        b.right = prune(b.right.take(), rest);
        if b.left.is_none() && b.right.is_none() {
            return None;
        }
    }
    Some(n)
}

fn sufficient_subset(root: Tree, limit: i64) -> Tree {
    prune(root, limit)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

struct Shape {
    val: Vec<i32>,
    left: Vec<i64>,
    right: Vec<i64>,
}

fn random_shape(n: i64, seed: &mut i64) -> Shape {
    let mut s = Shape { val: Vec::new(), left: Vec::new(), right: Vec::new() };
    for k in 0..n {
        s.val.push((next_random(seed) % 201 - 100) as i32);
        s.left.push(-1);
        s.right.push(-1);
        if k > 0 {
            let mut at = 0usize;
            loop {
                if next_random(seed) % 2 == 0 {
                    if s.left[at] < 0 {
                        s.left[at] = k;
                        break;
                    }
                    at = s.left[at] as usize;
                } else {
                    if s.right[at] < 0 {
                        s.right[at] = k;
                        break;
                    }
                    at = s.right[at] as usize;
                }
            }
        }
    }
    s
}

fn build(s: &Shape, k: i64) -> Tree {
    if k < 0 {
        return None;
    }
    let k = k as usize;
    Some(Rc::new(RefCell::new(TreeNode {
        val: s.val[k],
        left: build(s, s.left[k]),
        right: build(s, s.right[k]),
    })))
}

fn count(t: &Tree) -> i64 {
    match t {
        None => 0,
        Some(n) => {
            let b = n.borrow();
            1 + count(&b.left) + count(&b.right)
        }
    }
}

fn main() {
    let rounds: i64 = 100;
    let mut seed = 1080;
    let shapes: Vec<Shape> = (0..200).map(|_| random_shape(1000, &mut seed)).collect();
    let mut kept: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..200i64 {
            let limit = (r * 37 + i * 11) % 401 - 200;
            let k = count(&sufficient_subset(build(&shapes[i as usize], 0), limit));
            kept += k;
            check = (check * 31 + k + i) % 1000000007;
        }
    }
    println!("{rounds} rounds over 200 trees of 1000 nodes: {kept} nodes kept, checksum {check}");
}
