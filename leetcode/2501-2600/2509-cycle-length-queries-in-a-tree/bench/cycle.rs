// LeetCode #2509: Cycle Length Queries in a Tree -- Rust mirror of the
// benchmark (cycle.kara): the same queries, passes and checksum.

fn cycle_length_queries(_n: i64, queries: &[Vec<i64>]) -> Vec<i64> {
    let mut answer = Vec::new();
    for q in queries {
        let (mut a, mut b) = (q[0], q[1]);
        let mut length = 1;
        while a != b {
            if a > b {
                a /= 2;
            } else {
                b /= 2;
            }
            length += 1;
        }
        answer.push(length);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn below(top: i64, seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    (hi * 32768 + next_random(seed)) % top
}

fn main() {
    let size: i64 = (1 << 30) - 1;
    let mut seed = 2509;
    let mut queries: Vec<Vec<i64>> = Vec::new();
    while queries.len() < 100000 {
        let a = below(size, &mut seed) + 1;
        let b = below(size, &mut seed) + 1;
        if a != b {
            queries.push(vec![a, b]);
        }
    }
    let passes = 34;
    let mut check: i64 = 0;
    for p in 0..passes {
        let at = (check % queries.len() as i64) as usize;
        let kept = queries[at][1];
        let mut b = (check + p) % size + 1;
        if b == queries[at][0] {
            b = b % size + 1;
        }
        queries[at][1] = b;
        for x in cycle_length_queries(30, &queries) {
            check = (check * 31 + x + p) % 1000000007;
        }
        queries[at][1] = kept;
    }
    println!("{} passes over 10^5 queries on 30 levels: checksum {}", passes, check);
}
