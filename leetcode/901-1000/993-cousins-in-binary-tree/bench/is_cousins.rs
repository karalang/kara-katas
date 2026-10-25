// Benchmark: LeetCode #993 Cousins in Binary Tree -- the ★ arm, a
// breadth-first search a level at a time, on random trees of 100 nodes,
// LeetCode's largest. Mirrors is_cousins.kara, .c, .py and go-seq/. The
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

fn is_cousins(root: &Tree, x: i64, y: i64) -> bool {
    let mut level: Vec<(Node, i64)> = vec![(root.clone().unwrap(), -1)];
    while !level.is_empty() {
        let mut px = -1;
        let mut py = -1;
        let mut next: Vec<(Node, i64)> = Vec::new();
        for (node, parent) in level.iter() {
            let n = node.borrow();
            if n.val == x {
                px = *parent;
            }
            if n.val == y {
                py = *parent;
            }
            if let Some(l) = &n.left {
                next.push((l.clone(), n.val));
            }
            if let Some(r) = &n.right {
                next.push((r.clone(), n.val));
            }
        }
        if px >= 0 && py >= 0 {
            return px != py;
        }
        if px >= 0 || py >= 0 {
            return false;
        }
        level = next;
    }
    false
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

fn random_tree(n: i64, seed: &mut i64) -> Tree {
    let mut vals: Vec<i64> = (1..n + 1).collect();
    let mut i = n - 1;
    while i > 0 {
        let j = next_random(seed) % (i + 1);
        vals.swap(i as usize, j as usize);
        i -= 1;
    }
    let root = new_node(vals[0]);
    for k in 1..n as usize {
        attach(&root, new_node(vals[k]), seed);
    }
    Some(root)
}

fn main() {
    let rounds = 500;
    let mut seed = 993;
    let trees: Vec<Tree> = (0..20).map(|_| random_tree(100, &mut seed)).collect();
    let mut found: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for t in 0..20 {
            let d = 1 + (r * 7 + t) % 99;
            for x in 1..101 {
                let y = 1 + (x - 1 + d) % 100;
                let got = is_cousins(&trees[((r + t) % 20) as usize], x, y);
                if got {
                    found += 1;
                }
                check = (check * 31 + if got { 2 } else { 1 }) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over 20 trees of 100 nodes: {found} cousin pairs, checksum {check}");
}
