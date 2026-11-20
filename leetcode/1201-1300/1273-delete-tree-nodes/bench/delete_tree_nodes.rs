// LeetCode #1273 bench, in Rust: the ★ arm (the children listed from the
// parents, then a depth-first search returning each subtree's sum and the
// nodes it keeps) on 20 random trees of 10,000 nodes with values from -3
// to 3, drawn once, 60 rounds; every answer folded into a checksum.

fn subtree(node: usize, children: &[Vec<usize>], value: &[i64]) -> (i64, i64) {
    let mut sum = value[node];
    let mut kept = 1;
    for &child in &children[node] {
        let (s, k) = subtree(child, children, value);
        sum += s;
        kept += k;
    }
    if sum == 0 {
        (0, 0)
    } else {
        (sum, kept)
    }
}

fn delete_tree_nodes(nodes: usize, parent: &[i64], value: &[i64]) -> i64 {
    let mut children: Vec<Vec<usize>> = vec![Vec::new(); nodes];
    for i in 1..nodes {
        children[parent[i] as usize].push(i);
    }
    subtree(0, &children, value).1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_parents(n: i64, reach: i64, seed: &mut i64) -> Vec<i64> {
    let mut order: Vec<i64> = (0..n).collect();
    for i in (2..n).rev() {
        let j = 1 + next_random(seed) % i;
        order.swap(i as usize, j as usize);
    }
    let mut parent = vec![-1i64; n as usize];
    for i in 1..n {
        let back = 1 + next_random(seed) % reach.min(i);
        parent[order[i as usize] as usize] = order[(i - back) as usize];
    }
    parent
}

fn main() {
    let mut seed = 1273;
    let mut trees: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..20 {
        let parent = random_parents(10000, 1000, &mut seed);
        let value: Vec<i64> = (0..10000).map(|_| next_random(&mut seed) % 7 - 3).collect();
        trees.push((parent, value));
    }
    let mut check: i64 = 0;
    for round in 0..60 {
        for (parent, value) in &trees {
            check = (check * 131 + delete_tree_nodes(10000, parent, value) + round) % 1000000007;
        }
    }
    println!("60 rounds of 20 trees of 10000 nodes: checksum {}", check);
}
