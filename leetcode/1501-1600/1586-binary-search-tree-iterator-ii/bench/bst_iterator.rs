// LeetCode #1586: Binary Search Tree Iterator II -- the bench in Rust,
// mirroring bst_iterator.kara: the lazy in-order stack and the list of
// values met. Each node is an `Rc<RefCell<TreeNode>>`, as in LeetCode's
// template and as Kāra's `shared struct` is counted.

use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

struct BSTIterator {
    spine: Vec<Node>,
    seen: Vec<i32>,
    at: i64,
}

impl BSTIterator {
    fn new(root: Option<Node>) -> Self {
        let mut it = BSTIterator { spine: Vec::new(), seen: Vec::new(), at: -1 };
        it.push_left(root);
        it
    }

    fn push_left(&mut self, mut node: Option<Node>) {
        while let Some(n) = node {
            node = n.borrow().left.clone();
            self.spine.push(n);
        }
    }

    fn has_next(&self) -> bool {
        self.at + 1 < self.seen.len() as i64 || !self.spine.is_empty()
    }

    fn next(&mut self) -> i32 {
        self.at += 1;
        if self.at == self.seen.len() as i64 {
            let n = self.spine.pop().unwrap();
            self.seen.push(n.borrow().val);
            let right = n.borrow().right.clone();
            self.push_left(right);
        }
        self.seen[self.at as usize]
    }

    fn has_prev(&self) -> bool {
        self.at > 0
    }

    fn prev(&mut self) -> i32 {
        self.at -= 1;
        self.seen[self.at as usize]
    }
}

fn leaf(v: i32) -> Node {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn insert(root: &Node, v: i32) -> bool {
    let mut node = root.clone();
    loop {
        let val = node.borrow().val;
        if v == val {
            return false;
        }
        let child = if v < val { node.borrow().left.clone() } else { node.borrow().right.clone() };
        match child {
            Some(c) => node = c,
            None => {
                if v < val {
                    node.borrow_mut().left = Some(leaf(v));
                } else {
                    node.borrow_mut().right = Some(leaf(v));
                }
                return true;
            }
        }
    }
}

fn build(values: &[i32]) -> (Option<Node>, i64) {
    if values.is_empty() {
        return (None, 0);
    }
    let root = leaf(values[0]);
    let mut n = 1;
    for &v in &values[1..] {
        if insert(&root, v) {
            n += 1;
        }
    }
    (Some(root), n)
}

fn drive(root: &Option<Node>, calls: &[i64]) -> Vec<i64> {
    let mut it = BSTIterator::new(root.clone());
    let mut out = Vec::new();
    for &c in calls {
        let answer = match c {
            0 => it.has_next() as i64,
            1 => it.next() as i64,
            2 => it.has_prev() as i64,
            _ => it.prev() as i64,
        };
        out.push(answer);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn draw_calls(n: i64, count: i64, seed: &mut i64) -> Vec<i64> {
    let mut at = -1;
    let mut calls = Vec::new();
    for _ in 0..count {
        let r = next_random(seed) % 6;
        let call = if (2..=4).contains(&r) && at + 1 < n {
            at += 1;
            1
        } else if r == 5 && at > 0 {
            at -= 1;
            3
        } else {
            r % 2 * 2
        };
        calls.push(call);
    }
    calls
}

fn main() {
    let mut seed = 1586;
    let mut problems = Vec::new();
    let mut nodes = 0;
    for _ in 0..20 {
        let values: Vec<i32> = (0..100000)
            .map(|_| ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000) as i32)
            .collect();
        let (root, n) = build(&values);
        nodes += n;
        let calls = draw_calls(n, 300000, &mut seed);
        problems.push((root, calls));
    }
    let mut check = 0;
    for (root, calls) in &problems {
        for &answer in &drive(root, calls) {
            check = mix(check, answer);
        }
    }
    println!("20 trees of 100000 values: {} nodes, 6000000 calls, checksum {}", nodes, check);
}
