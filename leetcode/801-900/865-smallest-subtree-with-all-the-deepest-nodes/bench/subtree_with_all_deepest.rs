// LeetCode #865: Smallest Subtree with all the Deepest Nodes -- Rust
// mirror of the bench program (the ★ arm, one recursive pass), on
// LeetCode's Rust tree type, `Option<Rc<RefCell<TreeNode>>>`.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Node>,
    right: Option<Node>,
}

type Node = Rc<RefCell<TreeNode>>;

fn subtree_with_all_deepest(root: &Option<Node>) -> Option<Node> {
    deepest(root).1
}

fn deepest(node: &Option<Node>) -> (i64, Option<Node>) {
    match node {
        None => (0, None),
        Some(n) => {
            let b = n.borrow();
            let (dl, l) = deepest(&b.left);
            let (dr, r) = deepest(&b.right);
            if dl == dr {
                (dl + 1, Some(n.clone()))
            } else if dl > dr {
                (dl + 1, l)
            } else {
                (dr + 1, r)
            }
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(seed: &mut i64, n: i64) -> Option<Node> {
    let mut vals: Vec<i64> = (0..n).collect();
    for i in 1..n {
        let j = next_random(seed) % (i + 1);
        vals.swap(i as usize, j as usize);
    }
    let mut nodes: Vec<Node> = Vec::new();
    for k in 0..n as usize {
        let node = Rc::new(RefCell::new(TreeNode { val: vals[k], left: None, right: None }));
        if k > 0 {
            loop {
                let parent = nodes[(next_random(seed) % nodes.len() as i64) as usize].clone();
                let mut p = parent.borrow_mut();
                if next_random(seed) % 2 == 0 {
                    if p.left.is_none() {
                        p.left = Some(node.clone());
                        break;
                    }
                } else if p.right.is_none() {
                    p.right = Some(node.clone());
                    break;
                }
            }
        }
        nodes.push(node);
    }
    if n == 0 { None } else { Some(nodes[0].clone()) }
}

fn main() {
    let n = 500;
    let rounds = 300000;
    let mut seed = 865;
    let root = random_tree(&mut seed, n);
    let mut nodes: Vec<Node> = Vec::new();
    let mut stack: Vec<Node> = Vec::new();
    if let Some(r) = &root {
        stack.push(r.clone());
    }
    while let Some(node) = stack.pop() {
        let b = node.borrow();
        if let Some(child) = &b.left {
            stack.push(child.clone());
        }
        if let Some(child) = &b.right {
            stack.push(child.clone());
        }
        drop(b);
        nodes.push(node);
    }
    let leaf = Rc::new(RefCell::new(TreeNode { val: n, left: None, right: None }));
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        let mut at = nodes[(next_random(&mut seed) % n) as usize].clone();
        while at.borrow().left.is_some() && at.borrow().right.is_some() {
            at = nodes[(next_random(&mut seed) % n) as usize].clone();
        }
        let on_left = at.borrow().left.is_none();
        if on_left {
            at.borrow_mut().left = Some(leaf.clone());
        } else {
            at.borrow_mut().right = Some(leaf.clone());
        }
        let found = match subtree_with_all_deepest(&root) {
            Some(f) => f.borrow().val,
            None => -1,
        };
        if on_left {
            at.borrow_mut().left = None;
        } else {
            at.borrow_mut().right = None;
        }
        total += found;
        check = (check * 31 + found + 1) % 1000000007;
    }
    println!("{rounds} rounds on {n} nodes: answers sum to {total}, checksum {check}");
}
