// LeetCode #1506: Find Root of N-Ary Tree -- the benchmark, the same
// algorithm as root.kara: all values less all children's values, nodes
// shared by reference count as Kāra's `shared struct` is.

use std::collections::HashSet;
use std::rc::Rc;

struct Node {
    val: i64,
    children: Vec<Rc<Node>>,
}

fn find_root(nodes: Vec<Rc<Node>>) -> Rc<Node> {
    let mut total = 0;
    for node in &nodes {
        total += node.val;
        for child in &node.children {
            total -= child.val;
        }
    }
    for node in &nodes {
        if node.val == total {
            return node.clone();
        }
    }
    nodes[0].clone()
}

fn build(vals: Vec<i64>, kids: Vec<Vec<usize>>) -> Vec<Rc<Node>> {
    let n = vals.len();
    let mut made: Vec<Option<Rc<Node>>> = vec![None; n];
    for i in (0..n).rev() {
        let children = kids[i].iter().map(|&c| made[c].clone().unwrap()).collect();
        made[i] = Some(Rc::new(Node { val: vals[i], children }));
    }
    made.into_iter().map(|m| m.unwrap()).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn random_tree(most: i64, seed: &mut i64) -> Vec<Rc<Node>> {
    let n = (next_random(seed) % most + 1) as usize;
    let mut vals = Vec::new();
    let mut seen = HashSet::new();
    while vals.len() < n {
        let v = (next_random(seed) * 65536 + next_random(seed)) % 50001;
        if seen.insert(v) {
            vals.push(v);
        }
    }
    let mut kids: Vec<Vec<usize>> = vec![Vec::new(); n];
    for i in 1..n {
        kids[(next_random(seed) % i as i64) as usize].push(i);
    }
    let mut nodes = build(vals, kids);
    for i in (1..n).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        nodes.swap(i, j);
    }
    nodes
}

fn main() {
    let mut seed = 1506;
    let trees: Vec<Vec<Rc<Node>>> = (0..20).map(|_| random_tree(50000, &mut seed)).collect();
    let mut check = 0;
    for _ in 0..10 {
        for nodes in &trees {
            let root = find_root(nodes.clone());
            check = mix(check, root.val);
        }
    }
    println!("200 roots over 20 trees of up to 50000 nodes: checksum {check}");
}
