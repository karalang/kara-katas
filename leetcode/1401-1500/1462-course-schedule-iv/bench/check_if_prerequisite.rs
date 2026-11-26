// LeetCode #1462 bench in Rust: the ★ arm (the closure of the
// prerequisites by Floyd-Warshall) on the same 400 cases of 100 courses and
// 10^4 queries.

fn check_if_prerequisite(num_courses: i32, prerequisites: &[Vec<i32>], queries: &[Vec<i32>]) -> Vec<bool> {
    let n = num_courses as usize;
    let mut before = vec![vec![false; n]; n];
    for p in prerequisites {
        before[p[0] as usize][p[1] as usize] = true;
    }
    for k in 0..n {
        for u in 0..n {
            if before[u][k] {
                for v in 0..n {
                    if before[k][v] {
                        before[u][v] = true;
                    }
                }
            }
        }
    }
    queries.iter().map(|q| before[q[0] as usize][q[1] as usize]).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1462i64;
    let mut cases: Vec<(Vec<Vec<i32>>, Vec<Vec<i32>>)> = Vec::new();
    for _ in 0..400 {
        let mut order: Vec<i64> = (0..100).collect();
        for i in (1..100usize).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            order.swap(i, j);
        }
        let mut pre: Vec<Vec<i32>> = Vec::new();
        for i in 0..100 {
            for j in i + 1..100 {
                if next_random(&mut seed) % 20 == 0 {
                    pre.push(vec![order[i] as i32, order[j] as i32]);
                }
            }
        }
        let mut qs: Vec<Vec<i32>> = Vec::new();
        while qs.len() < 10000 {
            let u = next_random(&mut seed) % 100;
            let v = next_random(&mut seed) % 100;
            if u != v {
                qs.push(vec![u as i32, v as i32]);
            }
        }
        cases.push((pre, qs));
    }
    let mut check: i64 = 0;
    for (pre, qs) in &cases {
        for a in check_if_prerequisite(100, pre, qs) {
            check = (check * 3 + if a { 2 } else { 1 }) % 1000000007;
        }
    }
    println!("400 cases of 100 courses and 10^4 queries: checksum {check}");
}
