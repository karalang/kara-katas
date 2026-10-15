// Benchmark for #663: the subtree sums, listed, as the Kara ★ arm.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Node>,
    right: Option<Node>,
}

type Node = Rc<RefCell<TreeNode>>;

fn check_equal_tree(root: &Option<Node>) -> bool {
    let mut sums: Vec<i64> = Vec::new();
    let total = subtree_sum(root, &mut sums);
    if total % 2 != 0 {
        return false;
    }
    sums.pop();
    sums.iter().any(|&s| s == total / 2)
}

fn subtree_sum(node: &Option<Node>, sums: &mut Vec<i64>) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let b = n.borrow();
            let s = b.val + subtree_sum(&b.left, sums) + subtree_sum(&b.right, sums);
            sums.push(s);
            s
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaf(v: i64) -> Node {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn grown_tree(count: i64, seed: &mut i64) -> Node {
    let root = leaf(next_random(seed) % 200001 - 100000);
    for _ in 1..count {
        let mut at = root.clone();
        let mut placed = false;
        while !placed {
            if next_random(seed) % 2 == 0 {
                let l = at.borrow().left.clone();
                match l {
                    Some(l) => at = l,
                    None => {
                        at.borrow_mut().left = Some(leaf(next_random(seed) % 200001 - 100000));
                        placed = true;
                    }
                }
            } else {
                let r = at.borrow().right.clone();
                match r {
                    Some(r) => at = r,
                    None => {
                        at.borrow_mut().right = Some(leaf(next_random(seed) % 200001 - 100000));
                        placed = true;
                    }
                }
            }
        }
    }
    root
}

fn copy(node: &Option<Node>) -> Option<Node> {
    node.as_ref().map(|n| {
        let b = n.borrow();
        Rc::new(RefCell::new(TreeNode { val: b.val, left: copy(&b.left), right: copy(&b.right) }))
    })
}

fn main() {
    let mut seed: i64 = 663;
    let mut trees: Vec<Option<Node>> = Vec::new();
    for _ in 0..4 {
        trees.push(Some(grown_tree(10000, &mut seed)));
        let root = leaf(0);
        let half = Some(grown_tree(4999, &mut seed));
        let other = copy(&half);
        root.borrow_mut().left = half;
        root.borrow_mut().right = other;
        trees.push(Some(root));
    }
    let rounds = 4000i64;
    let mut split = 0;
    let mut sum = 0i64;
    for r in 0..rounds {
        let ok = check_equal_tree(&trees[(r % 8) as usize]);
        if ok {
            split += 1;
        }
        sum = (sum * 31 + r * 2 + if ok { 1 } else { 0 }) % 1000000007;
    }
    println!("8 trees of 10000 nodes, {} rounds: {} split, checksum {}", rounds, split, sum);
}
