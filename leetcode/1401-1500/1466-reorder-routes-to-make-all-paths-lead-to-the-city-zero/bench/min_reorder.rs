// LeetCode #1466 bench in Rust: the ★ arm (a breadth-first search out of
// city 0 over the roads taken both ways) on the same 10 trees of 50000
// cities and 20 passes.

use std::collections::VecDeque;

fn min_reorder(n: i32, connections: &[Vec<i32>]) -> i32 {
    let mut roads: Vec<Vec<(i32, i32)>> = vec![Vec::new(); n as usize];
    for c in connections {
        roads[c[0] as usize].push((c[1], 1));
        roads[c[1] as usize].push((c[0], 0));
    }
    let mut seen = vec![false; n as usize];
    let mut queue: VecDeque<i32> = VecDeque::new();
    seen[0] = true;
    queue.push_back(0);
    let mut turned = 0;
    while let Some(city) = queue.pop_front() {
        for &(next, away) in &roads[city as usize] {
            if !seen[next as usize] {
                seen[next as usize] = true;
                turned += away;
                queue.push_back(next);
            }
        }
    }
    turned
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1466i64;
    let n: i64 = 50000;
    let mut trees: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..10 {
        let mut label: Vec<i32> = (0..n).map(|c| c as i32).collect();
        for i in (1..n).rev() {
            let j = next_random(&mut seed) % (i + 1);
            label.swap(i as usize, j as usize);
        }
        let mut roads: Vec<Vec<i32>> = Vec::new();
        for i in 1..n {
            let p = next_random(&mut seed) % i;
            if next_random(&mut seed) % 2 == 0 {
                roads.push(vec![label[i as usize], label[p as usize]]);
            } else {
                roads.push(vec![label[p as usize], label[i as usize]]);
            }
        }
        trees.push(roads);
    }
    let mut check: i64 = 0;
    for pass in 0..20 {
        for t in 0..10 {
            let k = (check % (n - 1)) as usize;
            trees[t][k].swap(0, 1);
            let got = min_reorder(n as i32, &trees[t]);
            check = (check * 31 + got as i64 + pass) % 1000000007;
        }
    }
    println!("20 passes over 10 trees of 50000 cities: checksum {check}");
}
