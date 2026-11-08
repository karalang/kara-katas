// LeetCode #2003: Smallest Missing Genetic Value in Each Subtree -- the
// benchmark's Rust twin, the same algorithm as genetic.kara here.

fn mark(u: usize, children: &Vec<Vec<i64>>, nums: &Vec<i64>, seen: &mut Vec<bool>, visited: &mut Vec<bool>) {
    visited[u] = true;
    if (nums[u] as usize) < seen.len() {
        seen[nums[u] as usize] = true;
    }
    for &c in &children[u] {
        if !visited[c as usize] {
            mark(c as usize, children, nums, seen, visited);
        }
    }
}

fn smallest_missing(parents: &Vec<i64>, nums: &Vec<i64>) -> Vec<i64> {
    let n = parents.len();
    let mut answer = vec![1i64; n];
    let one = match nums.iter().position(|&v| v == 1) {
        Some(i) => i as i64,
        None => return answer,
    };
    let mut children: Vec<Vec<i64>> = vec![Vec::new(); n];
    for i in 1..n {
        children[parents[i] as usize].push(i as i64);
    }
    let mut seen = vec![false; n + 2];
    let mut visited = vec![false; n];
    let mut missing = 1usize;
    let mut u = one;
    while u != -1 {
        mark(u as usize, &children, nums, &mut seen, &mut visited);
        while seen[missing] {
            missing += 1;
        }
        answer[u as usize] = missing as i64;
        u = parents[u as usize];
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(n: i64, width: i64, extra: i64, seed: &mut i64) -> (Vec<i64>, Vec<i64>) {
    let mut parents = vec![-1i64];
    for i in 1..n {
        let lo = 0.max(i - width);
        parents.push(lo + next_random(seed) % (i - lo));
    }
    let mut values: Vec<i64> = (1..n + extra + 1).collect();
    for i in (1..values.len()).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        values.swap(i, j);
    }
    values.truncate(n as usize);
    (parents, values)
}

fn main() {
    // 40 trees of 20000 nodes built once, then the ★ arm on each, 25 rounds
    let mut seed = 2003i64;
    let mut trees = Vec::new();
    for a in 0..40i64 {
        let width = [2, 5, 50, 20000][(a % 4) as usize];
        trees.push(random_tree(20000, width, a % 2, &mut seed));
    }
    let mut calls = 0i64;
    let mut sum = 0i64;
    let mut check = 0i64;
    for _ in 0..25 {
        for (parents, nums) in trees.iter() {
            let answer = smallest_missing(parents, nums);
            calls += 1;
            for a in answer {
                sum += a;
                check = (check * 31 + a) % 1000000007;
            }
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
