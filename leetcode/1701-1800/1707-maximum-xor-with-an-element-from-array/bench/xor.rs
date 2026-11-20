// LeetCode #1707: Maximum XOR With an Element From Array -- the bench's
// Rust mirror: the ★ arm on 4 random problems of 100000 values and 100000
// queries, all drawn first, each answered 3 times.

// the queries offline by limit, against a 30-bit trie of the values allowed
fn maximize_xor(nums: &[i32], queries: &[Vec<i32>]) -> Vec<i32> {
    let mut values = nums.to_vec();
    values.sort();
    let mut order: Vec<usize> = (0..queries.len()).collect();
    order.sort_by_key(|&i| queries[i][1]);
    // children of each node, 0 for none: the root is node 0
    let mut trie: Vec<[usize; 2]> = vec![[0, 0]];
    let mut next = 0;
    let mut answer: Vec<i32> = vec![-1; queries.len()];
    for &i in order.iter() {
        let (x, m) = (queries[i][0], queries[i][1]);
        while next < values.len() && values[next] <= m {
            let mut node = 0;
            for bit in (0..30).rev() {
                let b = (values[next] >> bit & 1) as usize;
                if trie[node][b] == 0 {
                    trie.push([0, 0]);
                    let last = trie.len() - 1;
                    trie[node][b] = last;
                }
                node = trie[node][b];
            }
            next += 1;
        }
        if next == 0 {
            continue;
        }
        let mut node = 0;
        let mut best = 0;
        for bit in (0..30).rev() {
            let want = ((x >> bit & 1) ^ 1) as usize;
            if trie[node][want] != 0 {
                best |= 1 << bit;
                node = trie[node][want];
            } else {
                node = trie[node][want ^ 1];
            }
        }
        answer[i] = best;
    }
    answer
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// a random value below 10^9, from two draws
fn value(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    (a * 32768 + next_random(seed)) % 1000000000
}

fn main() {
    let count = 4;
    let rounds = 3;
    let n = 100000;
    let mut seed = 1707;
    let mut problems: Vec<(Vec<i32>, Vec<Vec<i32>>)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i32> = (0..n).map(|_| value(&mut seed) as i32).collect();
        let mut queries: Vec<Vec<i32>> = Vec::new();
        for _ in 0..n {
            let x = value(&mut seed) as i32;
            queries.push(vec![x, value(&mut seed) as i32]);
        }
        problems.push((nums, queries));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, queries) in problems.iter() {
            for &a in maximize_xor(nums, queries).iter() {
                sum += a as i64;
                check = (check * 31 + a as i64 + 1 + r) % 1000000007;
            }
        }
    }
    println!("{count} problems of {n} values and {n} queries, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
