// Benchmark for #559: Rust mirror of the ★ arm (recursion); see
// maximum_depth.kara. The trees are borrowed by the walk, as Kāra's
// bare parameter borrows.

struct Node {
    #[allow(dead_code)]
    val: i64,
    children: Vec<Node>,
}

fn depth(node: &Node) -> i64 {
    let mut deepest = 0;
    for child in &node.children {
        deepest = deepest.max(depth(child));
    }
    deepest + 1
}

fn max_depth(root: &Option<Node>) -> i64 {
    match root {
        Some(node) => depth(node),
        None => 0,
    }
}

// ---- benchmark --------------------------------------------------------------

fn build_random(i: usize, vals: &[i64], kids: &[Vec<usize>]) -> Node {
    let mut children: Vec<Node> = Vec::new();
    for &k in &kids[i] {
        children.push(build_random(k, vals, kids));
    }
    Node { val: vals[i], children }
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: usize = 10000;
    let count: usize = 100;
    let rounds: usize = 50;
    let mut seed: i64 = 559;
    let mut trees: Vec<Option<Node>> = Vec::new();
    for _ in 0..count {
        let reach = 2 + step(&mut seed) % 1000;
        let mut vals: Vec<i64> = Vec::new();
        let mut kids: Vec<Vec<usize>> = Vec::new();
        for i in 0..n {
            vals.push(step(&mut seed) % 10001);
            kids.push(Vec::new());
            if i > 0 {
                let back = 1 + (step(&mut seed) % (i as i64).min(reach)) as usize;
                kids[i - back].push(i);
            }
        }
        trees.push(Some(build_random(0, &vals, &kids)));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let d = max_depth(&trees[(round * 7 + g) % count]);
            total += d;
            checksum = (checksum * 31 + d) % 1000000007;
        }
    }
    println!("{} trees of {} nodes, {} rounds: depths sum to {}, checksum {}", count, n, rounds, total, checksum);
}
