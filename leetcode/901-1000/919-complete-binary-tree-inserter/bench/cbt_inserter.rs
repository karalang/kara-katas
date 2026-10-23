// LeetCode #919: Complete Binary Tree Inserter -- bench: a queue of the
// nodes with a free child slot. Mirrors cbt_inserter.kara, with LeetCode's
// Rc<RefCell<TreeNode>> nodes.
use std::cell::RefCell;
use std::collections::VecDeque;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn new_node(val: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

struct CBTInserter {
    root: Rc<RefCell<TreeNode>>,
    open: VecDeque<Rc<RefCell<TreeNode>>>,
}

impl CBTInserter {
    fn new(root: Rc<RefCell<TreeNode>>) -> Self {
        let mut open = VecDeque::new();
        let mut walk = VecDeque::new();
        walk.push_back(root.clone());
        while let Some(node) = walk.pop_front() {
            let n = node.borrow();
            if let Some(l) = &n.left {
                walk.push_back(l.clone());
            }
            if let Some(r) = &n.right {
                walk.push_back(r.clone());
            }
            if n.left.is_none() || n.right.is_none() {
                open.push_back(node.clone());
            }
        }
        CBTInserter { root, open }
    }

    fn insert(&mut self, val: i64) -> i64 {
        let child = new_node(val);
        let parent = self.open.front().unwrap().clone();
        let mut p = parent.borrow_mut();
        if p.left.is_none() {
            p.left = Some(child.clone());
        } else {
            p.right = Some(child.clone());
            self.open.pop_front();
        }
        self.open.push_back(child);
        p.val
    }

    fn get_root(&self) -> Rc<RefCell<TreeNode>> {
        self.root.clone()
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// A complete tree holding vals in level order.
fn complete_tree(vals: &[i64]) -> Rc<RefCell<TreeNode>> {
    let nodes: Vec<_> = vals.iter().map(|&v| new_node(v)).collect();
    for i in 1..nodes.len() {
        let mut parent = nodes[(i - 1) / 2].borrow_mut();
        if i % 2 == 1 {
            parent.left = Some(nodes[i].clone());
        } else {
            parent.right = Some(nodes[i].clone());
        }
    }
    nodes[0].clone()
}

fn main() {
    let rounds = 200;
    let n = 1000;
    let m = 50000;
    let mut seed = 919;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        // a fresh tree of n values, then m inserts into it
        let vals: Vec<i64> = (0..n).map(|_| next_random(&mut seed) % 100000).collect();
        let mut inserter = CBTInserter::new(complete_tree(&vals));
        let mut parents = 0;
        for _ in 0..m {
            parents += inserter.insert(next_random(&mut seed) % 100000);
        }
        let root = inserter.get_root();
        total += parents;
        check = (check * 1000003 + parents + root.borrow().val) % 1000000007;
    }
    println!("{rounds} rounds of {m} inserts into trees of {n}: parents summing to {total}, checksum {check}");
}
