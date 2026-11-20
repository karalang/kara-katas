// LeetCode #1287 bench, in Rust: the ★ arm (the first i where arr[i] equals
// arr[i + n / 4]) on 100 sorted arrays of 10^5 numbers, built once, 1000
// rounds, every answer folded into a checksum.

fn find_special_integer(arr: &[i64]) -> i64 {
    let quarter = arr.len() / 4;
    for i in 0..(arr.len() - quarter) {
        if arr[i] == arr[i + quarter] {
            return arr[i];
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn problem(seed: &mut i64, n: i64) -> Vec<i64> {
    let planted = next_random(seed) % 100001;
    let times = n / 4 + 1 + next_random(seed) % (n / 4);
    let mut arr: Vec<i64> = vec![planted; times as usize];
    while (arr.len() as i64) < n {
        let x = next_random(seed) % 100001;
        if x != planted {
            arr.push(x);
        }
    }
    arr.sort();
    arr
}

fn main() {
    let mut seed = 1287;
    let mut problems: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100 {
        problems.push(problem(&mut seed, 100000));
    }
    let mut check: i64 = 0;
    for round in 0..1000i64 {
        for arr in problems.iter() {
            check = (check * 131 + find_special_integer(arr) + round) % 1000000007;
        }
    }
    println!("1000 rounds of 100 arrays of 100000 numbers: checksum {}", check);
}
