// LeetCode #2764: Is Array a Preorder of Some Binary Tree -- the bench
// (preorder.kara in Rust): a stack of the nodes whose subtrees are still
// open, each node closing every subtree above its parent.

fn is_preorder(nodes: &[[i64; 2]]) -> bool {
    let mut stack: Vec<i64> = Vec::new();
    for node in nodes.iter() {
        let (id, parent) = (node[0], node[1]);
        while let Some(&top) = stack.last() {
            if top == parent {
                break;
            }
            stack.pop();
        }
        if stack.is_empty() && parent != -1 {
            return false;
        }
        stack.push(id);
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

// a random binary tree of n nodes, ids spread over 0 to 100000, listed in
// a random preorder; then, half the time, two places swapped
fn tree(n: i64, seed: &mut i64) -> Vec<[i64; 2]> {
    let shift = wide(seed) % 100001;
    let ids: Vec<i64> = (0..n).map(|k| (k * 37 + shift) % 100001).collect();
    let mut kids: Vec<Vec<i64>> = vec![Vec::new(); n as usize];
    for k in 1..n {
        let mut p = wide(seed) % k;
        while kids[p as usize].len() == 2 {
            p = wide(seed) % k;
        }
        kids[p as usize].push(k);
    }
    let mut parent: Vec<i64> = vec![-1; n as usize];
    for p in 0..n as usize {
        for &c in kids[p].iter() {
            parent[c as usize] = p as i64;
        }
    }
    let mut order: Vec<i64> = Vec::new();
    let mut stack: Vec<i64> = vec![0];
    while let Some(u) = stack.pop() {
        order.push(u);
        let mut ks = kids[u as usize].clone();
        if ks.len() == 2 && next_random(seed) % 2 == 1 {
            ks.swap(0, 1);
        }
        for &c in ks.iter().rev() {
            stack.push(c);
        }
    }
    let mut nodes: Vec<[i64; 2]> = order
        .iter()
        .map(|&u| {
            let p = parent[u as usize];
            [ids[u as usize], if p >= 0 { ids[p as usize] } else { -1 }]
        })
        .collect();
    if next_random(seed) % 2 == 1 && n > 1 {
        let i = wide(seed) % n;
        let j = wide(seed) % n;
        nodes.swap(i as usize, j as usize);
    }
    nodes
}

fn main() {
    let count = 20;
    let rounds = 100;
    let mut seed = 2764;
    let cases: Vec<Vec<[i64; 2]>> = (0..count).map(|_| tree(100000, &mut seed)).collect();
    let mut good = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (c, nodes) in cases.iter().enumerate() {
            if is_preorder(nodes) {
                good += 1;
                check = (check * 31 + c as i64 + r) % 1000000007;
            }
        }
    }
    println!("{count} trees of 100000, {rounds} rounds: {good} preorders, checksum {check}");
}
