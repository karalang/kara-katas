// Benchmark: LeetCode #965 Univalued Binary Tree -- the ★ arm, depth
// first, on trees of 100 nodes, LeetCode's largest. Mirrors
// is_unival_tree.kara, .c, .py and go-seq/. The tree is LeetCode's Rust
// shape, `Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
// `shared struct` is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;
type Tree = Option<Node>;

fn holds(t: &Tree, v: i64) -> bool {
    match t {
        None => true,
        Some(node) => {
            let n = node.borrow();
            n.val == v && holds(&n.left, v) && holds(&n.right, v)
        }
    }
}

fn is_unival_tree(root: &Tree) -> bool {
    match root {
        None => true,
        Some(node) => {
            let n = node.borrow();
            holds(&n.left, n.val) && holds(&n.right, n.val)
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(val: i64) -> Node {
    Rc::new(RefCell::new(TreeNode {
        val,
        left: None,
        right: None,
    }))
}

fn attach(root: &Node, node: Node, seed: &mut i64) {
    let mut cur = root.clone();
    loop {
        let go_left = next_random(seed) % 2 == 0;
        let next = if go_left {
            cur.borrow().left.clone()
        } else {
            cur.borrow().right.clone()
        };
        match next {
            Some(child) => cur = child,
            None => {
                if go_left {
                    cur.borrow_mut().left = Some(node);
                } else {
                    cur.borrow_mut().right = Some(node);
                }
                return;
            }
        }
    }
}

fn make_tree(kind: i64, n: usize, seed: &mut i64) -> Tree {
    let v = next_random(seed) % 100;
    let mut vals = vec![v; n];
    if kind == 3 {
        for val in vals.iter_mut() {
            *val = next_random(seed) % 2;
        }
    } else {
        for _ in 0..kind {
            let k = (next_random(seed) as usize) % n;
            vals[k] = next_random(seed) % 100;
        }
    }
    let root = new_node(vals[0]);
    for &val in &vals[1..] {
        attach(&root, new_node(val), seed);
    }
    Some(root)
}

fn main() {
    let rounds = 4000;
    let mut seed = 965;
    let trees: Vec<Tree> = (0..200).map(|i| make_tree(i % 4, 100, &mut seed)).collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..200 {
            let bit = if is_unival_tree(&trees[(r + i) % 200]) {
                1
            } else {
                0
            };
            total += bit;
            check = (check * 31 + bit + 1 + i as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds over 200 trees of 100 nodes: {total} univalued, checksum {check}");
}
