// LeetCode #2392: Build a Matrix With Conditions -- the bench, the ★ arm
// in Rust: Kahn's algorithm for the rows and again for the columns.

use std::collections::VecDeque;

fn order(k: usize, edges: &[[i64; 2]]) -> Vec<i64> {
    let mut next: Vec<Vec<i64>> = vec![Vec::new(); k + 1];
    let mut into = vec![0i64; k + 1];
    for e in edges {
        next[e[0] as usize].push(e[1]);
        into[e[1] as usize] += 1;
    }
    let mut queue: VecDeque<i64> = VecDeque::new();
    for v in 1..=k {
        if into[v] == 0 {
            queue.push_back(v as i64);
        }
    }
    let mut taken = Vec::new();
    while let Some(v) = queue.pop_front() {
        taken.push(v);
        for &w in &next[v as usize] {
            into[w as usize] -= 1;
            if into[w as usize] == 0 {
                queue.push_back(w);
            }
        }
    }
    taken
}

fn build_matrix(k: usize, rows: &[[i64; 2]], cols: &[[i64; 2]]) -> Vec<Vec<i64>> {
    let by_row = order(k, rows);
    let by_col = order(k, cols);
    if by_row.len() < k || by_col.len() < k {
        return Vec::new();
    }
    let mut col_of = vec![0usize; k + 1];
    for c in 0..k {
        col_of[by_col[c] as usize] = c;
    }
    let mut m = vec![vec![0i64; k]; k];
    for r in 0..k {
        let v = by_row[r];
        m[r][col_of[v as usize]] = v;
    }
    m
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn conditions(seed: &mut i64, k: i64, count: i64) -> Vec<[i64; 2]> {
    let mut order: Vec<i64> = (1..k + 1).collect();
    for i in 1..k {
        let j = next_random(seed) % (i + 1);
        order.swap(i as usize, j as usize);
    }
    (0..count)
        .map(|_| {
            let a = next_random(seed) % k;
            let mut b = next_random(seed) % (k - 1);
            if b >= a {
                b += 1;
            }
            [order[a.min(b) as usize], order[a.max(b) as usize]]
        })
        .collect()
}

fn main() {
    let mut seed = 2392i64;
    let mut cases = Vec::new();
    for _ in 0..20 {
        let rows = conditions(&mut seed, 200, 4000);
        let cols = conditions(&mut seed, 200, 4000);
        cases.push((rows, cols));
    }
    let mut check = 0i64;
    for p in 0..500i64 {
        for (rows, cols) in &cases {
            let m = build_matrix(200, rows, cols);
            for r in 0..200usize {
                for c in 0..200usize {
                    if m[r][c] > 0 {
                        check = (check * 31 + m[r][c] * (r * 200 + c) as i64 + p) % 1000000007;
                    }
                }
            }
        }
    }
    println!("500 passes over 20 matrices of k = 200: checksum {}", check);
}
