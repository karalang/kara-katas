// LeetCode #1377 bench -- Rust: the ★ arm: the chance of the frog being on
// each vertex, moved one second at a time, a vertex with unvisited
// neighbours handing its chance to them in equal shares.

fn frog_position(n: i32, edges: &[Vec<i32>], t: i32, target: i32) -> f64 {
    let n = n as usize;
    let mut adjacent: Vec<Vec<usize>> = vec![Vec::new(); n + 1];
    for e in edges {
        adjacent[e[0] as usize].push(e[1] as usize);
        adjacent[e[1] as usize].push(e[0] as usize);
    }
    let mut seen = vec![false; n + 1];
    seen[1] = true;
    let mut chance = vec![0.0f64; n + 1];
    chance[1] = 1.0;
    let mut level: Vec<usize> = vec![1];
    for _ in 0..t {
        let mut next: Vec<usize> = Vec::new();
        for &u in &level {
            let ahead: Vec<usize> = adjacent[u].iter().copied().filter(|&v| !seen[v]).collect();
            if ahead.is_empty() {
                continue;
            }
            let share = chance[u] / ahead.len() as f64;
            for &v in &ahead {
                seen[v] = true;
                chance[v] = share;
                next.push(v);
            }
            chance[u] = 0.0;
        }
        level = next;
    }
    chance[target as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 50 trees of 100 vertices built once; then 100000 rounds, each asking
    // one tree, a time and a target drawn from the checksum so far for the
    // frog's chance, counted in units of 2^-20 (see the Kāra bench)
    let n = 100i64;
    let mut seed = 1377i64;
    let mut trees: Vec<Vec<Vec<i32>>> = Vec::new();
    for c in 0..50 {
        let mut order: Vec<i64> = (1..n + 1).collect();
        for i in (1..n).rev() {
            let j = next_random(&mut seed) % (i + 1);
            order.swap(i as usize, j as usize);
        }
        let mut edges: Vec<Vec<i32>> = Vec::new();
        for k in 1..n {
            let back = if c % 2 == 0 { next_random(&mut seed) % k } else { k - 1 - next_random(&mut seed) % k.min(3) };
            edges.push(vec![order[k as usize] as i32, order[back as usize] as i32]);
        }
        trees.push(edges);
    }
    let mut check: i64 = 0;
    for r in 0..100000i64 {
        let c = (check % 50) as usize;
        let t = 1 + (check / 50) % 50;
        let target = 1 + (check / 2500 + r) % n;
        let p = frog_position(n as i32, &trees[c], t as i32, target as i32);
        check = (check * 31 + (p * 1048576.0 + 0.5).floor() as i64 + r) % 1000000007;
    }
    println!("100000 rounds over 50 trees of 100 vertices: checksum {check}");
}
