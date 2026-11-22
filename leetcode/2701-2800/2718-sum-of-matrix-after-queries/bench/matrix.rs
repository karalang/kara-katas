// LeetCode #2718: Sum of Matrix After Queries -- the bench (matrix.kara
// in Rust): the queries read from the last back, each row or column not
// set later filling the lines of the other kind not yet taken.

fn matrix_sum_queries(n: i64, queries: &Vec<Vec<i64>>) -> i64 {
    let mut row_taken: Vec<bool> = vec![false; n as usize];
    let mut col_taken: Vec<bool> = vec![false; n as usize];
    let mut rows_left = n;
    let mut cols_left = n;
    let mut sum: i64 = 0;
    for query in queries.iter().rev() {
        let (kind, index, value) = (query[0], query[1] as usize, query[2]);
        if kind == 0 {
            if !row_taken[index] {
                row_taken[index] = true;
                rows_left -= 1;
                sum += value * cols_left;
            }
        } else if !col_taken[index] {
            col_taken[index] = true;
            cols_left -= 1;
            sum += value * rows_left;
        }
    }
    sum
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 40;
    let rounds = 20;
    let mut seed: i64 = 2718;
    let mut problems: Vec<(i64, Vec<Vec<i64>>)> = Vec::new();
    for _ in 0..count {
        let n = 10000;
        let mut queries: Vec<Vec<i64>> = Vec::new();
        for _ in 0..50000 {
            let kind = next_random(&mut seed) % 2;
            let index = wide(&mut seed) % n;
            let value = wide(&mut seed) % 100001;
            queries.push(vec![kind, index, value]);
        }
        problems.push((n, queries));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (n, queries) in problems.iter() {
            let total = matrix_sum_queries(*n, queries);
            sum += total % 1000000007;
            check = (check * 31 + total % 1000000007 + r) % 1000000007;
        }
    }
    println!("{} cases of 50000 queries on 10000 rows, {} rounds: sums mod p sum to {}, checksum {}", count, rounds, sum, check);
}
