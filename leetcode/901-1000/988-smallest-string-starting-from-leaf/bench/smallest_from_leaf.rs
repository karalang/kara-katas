// Benchmark: LeetCode #988 Smallest String Starting From Leaf -- the ★
// arm, a walk carrying the path, on random trees of 8500 nodes,
// LeetCode's largest. Mirrors smallest_from_leaf.kara, .c, .py and
// go-seq/. The tree is LeetCode's Rust shape,
// `Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
// `shared struct` is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn walk(t: &Node, path: &mut Vec<char>, best: &mut Option<String>) {
    let n = t.borrow();
    path.push((97 + n.val) as u8 as char);
    if n.left.is_none() && n.right.is_none() {
        let s: String = path.iter().rev().collect();
        let smaller = match best {
            Some(b) => s < *b,
            None => true,
        };
        if smaller {
            *best = Some(s);
        }
    } else {
        if let Some(l) = &n.left {
            walk(l, path, best);
        }
        if let Some(r) = &n.right {
            walk(r, path, best);
        }
    }
    path.pop();
}

fn smallest_from_leaf(root: &Node) -> String {
    let mut path: Vec<char> = Vec::new();
    let mut best: Option<String> = None;
    walk(root, &mut path, &mut best);
    best.unwrap()
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

fn random_tree(n: usize, seed: &mut i64) -> Node {
    let root = new_node(next_random(seed) % 4);
    for _ in 1..n {
        let node = new_node(next_random(seed) % 4);
        attach(&root, node, seed);
    }
    root
}

fn main() {
    let rounds = 100;
    let mut seed = 988;
    let trees: Vec<Node> = (0..20).map(|_| random_tree(8500, &mut seed)).collect();
    let mut letters: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let s = smallest_from_leaf(&trees[(r + i) % 20]);
            letters += s.len() as i64;
            for b in s.bytes() {
                check = (check * 31 + b as i64) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over 20 trees of 8500 nodes: {letters} letters, checksum {check}");
}
