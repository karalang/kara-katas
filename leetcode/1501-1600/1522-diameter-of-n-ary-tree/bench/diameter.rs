// LeetCode #1522: Diameter of N-Ary Tree -- bench: the ★ arm over 1000
// random trees of 1 to 2000 nodes, built once and answered 20 times.
// Nodes are shared (`Rc`), as Kāra's `shared struct` is.

use std::rc::Rc;

#[allow(dead_code)]
struct Node {
    val: i64,
    children: Vec<Rc<Node>>,
}

fn height(node: &Node, best: &mut i64) -> i64 {
    let mut first = 0;
    let mut second = 0;
    for child in &node.children {
        let h = height(child, best) + 1;
        if h > first {
            second = first;
            first = h;
        } else if h > second {
            second = h;
        }
    }
    *best = (*best).max(first + second);
    first
}

fn diameter(root: &Node) -> i64 {
    let mut best = 0;
    height(root, &mut best);
    best
}

fn build(vals: &[i64], kids: &[Vec<usize>]) -> Rc<Node> {
    let n = vals.len();
    let mut made: Vec<Option<Rc<Node>>> = vec![None; n];
    for i in (0..n).rev() {
        let children: Vec<Rc<Node>> = kids[i].iter().map(|&c| made[c].clone().unwrap()).collect();
        made[i] = Some(Rc::new(Node { val: vals[i], children }));
    }
    made[0].clone().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let count = 1000;
    let mut seed = 1522i64;
    let mut trees: Vec<Rc<Node>> = Vec::new();
    for _ in 0..count {
        let n = (next_random(&mut seed) % 2000 + 1) as usize;
        let window = (next_random(&mut seed) % 64 + 1) as usize;
        let mut vals: Vec<i64> = Vec::new();
        let mut kids: Vec<Vec<usize>> = vec![Vec::new(); n];
        for i in 0..n {
            vals.push(next_random(&mut seed) % 1000);
            if i > 0 {
                let back = next_random(&mut seed) as usize % i.min(window);
                kids[i - 1 - back].push(i);
            }
        }
        trees.push(build(&vals, &kids));
    }
    let mut check = 0;
    let mut total = 0i64;
    for _ in 0..20 {
        for tree in &trees {
            let d = diameter(tree);
            total += d;
            check = mix(check, d);
        }
    }
    println!("20 passes over 1000 trees of up to 2000 nodes: diameters sum to {}, checksum {}", total, check);
}
