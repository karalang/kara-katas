// Benchmark: LeetCode #958 Check Completeness of a Binary Tree -- the ★
// arm, the first gap, on trees of 100 nodes, LeetCode's largest. Mirrors
// is_complete_tree.kara, .c, .py and go-seq/. The tree is LeetCode's Rust
// shape, `Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
// `shared struct` is.
use std::cell::RefCell;
use std::collections::VecDeque;
use std::rc::Rc;

struct TreeNode {
    #[allow(dead_code)]
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;
type Tree = Option<Node>;

fn is_complete_tree(root: &Tree) -> bool {
    let mut queue: VecDeque<Tree> = VecDeque::new();
    queue.push_back(root.clone());
    let mut gap = false;
    while let Some(slot) = queue.pop_front() {
        match slot {
            None => gap = true,
            Some(node) => {
                if gap {
                    return false;
                }
                let n = node.borrow();
                queue.push_back(n.left.clone());
                queue.push_back(n.right.clone());
            }
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(seed: &mut i64) -> Node {
    Rc::new(RefCell::new(TreeNode {
        val: 1 + next_random(seed) % 1000,
        left: None,
        right: None,
    }))
}

// Node i of the complete tree is a left child (side 0) when i is odd.
fn side_of(i: usize) -> usize {
    (i + 1) % 2
}

fn set_child(parent: &Node, side: usize, child: Tree) {
    if side == 0 {
        parent.borrow_mut().left = child;
    } else {
        parent.borrow_mut().right = child;
    }
}

fn complete_tree(n: usize, seed: &mut i64) -> Tree {
    if n == 0 {
        return None;
    }
    let nodes: Vec<Node> = (0..n).map(|_| new_node(seed)).collect();
    for i in 1..n {
        set_child(&nodes[(i - 1) / 2], side_of(i), Some(nodes[i].clone()));
    }
    Some(nodes[0].clone())
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
                set_child(&cur, if go_left { 0 } else { 1 }, Some(node));
                return;
            }
        }
    }
}

fn random_tree(n: usize, seed: &mut i64) -> Tree {
    if n == 0 {
        return None;
    }
    let root = new_node(seed);
    for _ in 1..n {
        let node = new_node(seed);
        attach(&root, node, seed);
    }
    Some(root)
}

fn in_order(root: &Node) -> Vec<Node> {
    let mut out = vec![root.clone()];
    let mut i = 0;
    while i < out.len() {
        let (l, r) = {
            let node = out[i].borrow();
            (node.left.clone(), node.right.clone())
        };
        if let Some(l) = l {
            out.push(l);
        }
        if let Some(r) = r {
            out.push(r);
        }
        i += 1;
    }
    out
}

fn make_tree(kind: i64, n: usize, seed: &mut i64) -> Tree {
    if kind == 3 {
        return random_tree(n, seed);
    }
    let t = complete_tree(n, seed);
    if n < 2 {
        return t;
    }
    let nodes = in_order(t.as_ref().unwrap());
    if kind == 1 {
        let last = nodes[n - 1].clone();
        set_child(&nodes[(n - 2) / 2], side_of(n - 1), None);
        let mut parents: Vec<Node> = Vec::new();
        let mut sides: Vec<usize> = Vec::new();
        for node in &nodes[..n - 1] {
            if node.borrow().left.is_none() {
                parents.push(node.clone());
                sides.push(0);
            }
            if node.borrow().right.is_none() {
                parents.push(node.clone());
                sides.push(1);
            }
        }
        let k = (next_random(seed) as usize) % parents.len();
        set_child(&parents[k], sides[k], Some(last));
    } else if kind == 2 {
        let leaves: Vec<usize> = (1..n)
            .filter(|&i| {
                let node = nodes[i].borrow();
                node.left.is_none() && node.right.is_none()
            })
            .collect();
        let i = leaves[(next_random(seed) as usize) % leaves.len()];
        set_child(&nodes[(i - 1) / 2], side_of(i), None);
    } else if kind == 4 {
        let k = (next_random(seed) as usize) % n;
        let mut node = nodes[k].borrow_mut();
        let node = &mut *node;
        std::mem::swap(&mut node.left, &mut node.right);
    }
    t
}

fn main() {
    let rounds = 4000;
    let mut seed = 958;
    let trees: Vec<Tree> = (0..200).map(|i| make_tree(i % 5, 100, &mut seed)).collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..200 {
            let bit = if is_complete_tree(&trees[(r + i) % 200]) {
                1
            } else {
                0
            };
            total += bit;
            check = (check * 31 + bit + 1 + i as i64) % 1000000007;
        }
    }
    println!(
        "{rounds} rounds over 200 trees of up to 100 nodes: {total} complete, checksum {check}"
    );
}
