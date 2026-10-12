// Benchmark for #431: mirror of encode.kara (left child, right sibling).
// The Kāra binary node is a `shared struct`, reference counted, so a
// binary node here is an Rc<RefCell<TreeNode>>; the n-ary tree is owned
// values, as in the Kāra program.
use std::cell::RefCell;
use std::rc::Rc;

struct Node {
    val: i64,
    children: Vec<Node>,
}

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Tree = Rc<RefCell<TreeNode>>;

fn encode_node(node: &Node) -> Tree {
    let t = Rc::new(RefCell::new(TreeNode { val: node.val, left: None, right: None }));
    let mut prev: Option<Tree> = None;
    for child in &node.children {
        let c = encode_node(child);
        match &prev {
            Some(p) => p.borrow_mut().right = Some(c.clone()),
            None => t.borrow_mut().left = Some(c.clone()),
        }
        prev = Some(c);
    }
    t
}

fn decode_node(t: &Tree) -> Node {
    let mut children = Vec::new();
    let mut child = t.borrow().left.clone();
    while let Some(c) = child {
        children.push(decode_node(&c));
        child = c.borrow().right.clone();
    }
    Node { val: t.borrow().val, children }
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn build_random(i: usize, vals: &[i64], kids: &[Vec<usize>]) -> Node {
    let mut children = Vec::new();
    for &k in &kids[i] {
        children.push(build_random(k, vals, kids));
    }
    Node { val: vals[i], children }
}

fn fold(node: &Node, count: &mut i64, checksum: &mut i64) {
    *count += 1;
    *checksum = (*checksum * 31 + node.val) % 1000000007;
    for child in &node.children {
        fold(child, count, checksum);
    }
}

fn main() {
    let n: usize = 10000;
    let rounds: i64 = std::env::args().nth(1).map_or(100, |a| a.parse().unwrap());
    let mut seed: i64 = 431;
    let mut count = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let reach = 10 + step(&mut seed) % 1000;
        let mut vals = Vec::new();
        let mut kids: Vec<Vec<usize>> = Vec::new();
        for i in 0..n {
            vals.push(step(&mut seed) % 10001);
            kids.push(Vec::new());
            if i > 0 {
                let back = 1 + step(&mut seed) % (i as i64).min(reach);
                kids[i - back as usize].push(i);
            }
        }
        let root = build_random(0, &vals, &kids);
        let bin = encode_node(&root);
        let back = decode_node(&bin);
        fold(&back, &mut count, &mut checksum);
    }
    println!("{} rounds of {} nodes: {} decoded, checksum {}", rounds, n, count, checksum);
}
