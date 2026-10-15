// Benchmark for #662: level by level, as the Kara ★ arm.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    #[allow(dead_code)]
    val: i64,
    left: Option<Node>,
    right: Option<Node>,
}

type Node = Rc<RefCell<TreeNode>>;

fn width_of_binary_tree(root: &Option<Node>) -> i64 {
    let mut best = 0;
    let mut level: Vec<(Node, i64)> = Vec::new();
    if let Some(r) = root {
        level.push((r.clone(), 0));
    }
    while !level.is_empty() {
        let first = level[0].1;
        let last = level[level.len() - 1].1;
        best = best.max(last - first + 1);
        let mut next: Vec<(Node, i64)> = Vec::new();
        for (node, place) in level.iter() {
            let p = (place - first) * 2;
            let b = node.borrow();
            if let Some(l) = &b.left {
                next.push((l.clone(), p));
            }
            if let Some(r) = &b.right {
                next.push((r.clone(), p + 1));
            }
        }
        level = next;
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaf(v: i64) -> Node {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn grown_tree(count: i64, levels: i64, seed: &mut i64) -> Option<Node> {
    let root = leaf(next_random(seed) % 201 - 100);
    let mut made = 1;
    while made < count {
        let mut at = root.clone();
        let mut depth = 1;
        let mut placed = false;
        while !placed && depth < levels {
            if next_random(seed) % 2 == 0 {
                let l = at.borrow().left.clone();
                match l {
                    Some(l) => at = l,
                    None => {
                        at.borrow_mut().left = Some(leaf(next_random(seed) % 201 - 100));
                        placed = true;
                    }
                }
            } else {
                let r = at.borrow().right.clone();
                match r {
                    Some(r) => at = r,
                    None => {
                        at.borrow_mut().right = Some(leaf(next_random(seed) % 201 - 100));
                        placed = true;
                    }
                }
            }
            depth += 1;
        }
        if placed {
            made += 1;
        }
    }
    Some(root)
}

fn main() {
    let mut seed: i64 = 662;
    let mut trees: Vec<Option<Node>> = Vec::new();
    for _ in 0..8 {
        trees.push(grown_tree(3000, 31, &mut seed));
    }
    let rounds = 20000;
    let mut sum = 0i64;
    for r in 0..rounds {
        let w = width_of_binary_tree(&trees[(r % 8) as usize]);
        sum = (sum * 31 + w + r) % 1000000007;
    }
    println!("8 trees of 3000 nodes, {} rounds: checksum {}", rounds, sum);
}
