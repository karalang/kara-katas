// Benchmark for #590: Rust mirror of the ★ arm (recursion); see
// postorder.kara. The trees are borrowed by the walk, as Kāra's bare
// parameter borrows, and each call returns a fresh `Vec`.

struct Node {
    val: i64,
    children: Vec<Node>,
}

fn walk(node: &Node, out: &mut Vec<i64>) {
    for child in &node.children {
        walk(child, out);
    }
    out.push(node.val);
}

fn postorder(root: &Option<Node>) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    if let Some(node) = root {
        walk(node, &mut out);
    }
    out
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
    let rounds: usize = 30;
    let mut seed: i64 = 590;
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
    let mut total: usize = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let got = postorder(&trees[(round * 7 + g) % count]);
            total += got.len();
            for v in got {
                checksum = (checksum * 31 + v) % 1000000007;
            }
        }
    }
    println!("{} trees of {} nodes, {} rounds: {} values listed, checksum {}", count, n, rounds, total, checksum);
}
