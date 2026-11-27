// LeetCode #1806: Minimum Number of Operations to Reinitialize a
// Permutation -- the bench in Rust: the ★ arm over 3000 calls, each n an
// even number to 1000 drawn from the checksum so far.

fn reinitialize_permutation(n: i32) -> i32 {
    let size = n as usize;
    let start: Vec<i64> = (0..size as i64).collect();
    let mut perm = start.clone();
    let mut ops = 0;
    loop {
        let mut arr: Vec<i64> = vec![0; size];
        for i in 0..size {
            arr[i] = if i % 2 == 0 { perm[i / 2] } else { perm[size / 2 + (i - 1) / 2] };
        }
        perm = arr;
        ops += 1;
        if perm == start {
            return ops;
        }
    }
}

fn main() {
    let mut check: i64 = 0;
    for call in 0..3000i64 {
        let n = 2 * (1 + (check + call) % 500);
        check = (check * 31 + reinitialize_permutation(n as i32) as i64) % 1000000007;
    }
    println!("3000 calls of even n to 1000: checksum {}", check);
}
