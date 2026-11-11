// LeetCode #2111: Minimum Operations to Make the Array K-Increasing -- the
// benchmark, the same algorithm as increasing.kara: each chain's patience
// tails, the first tail above each value found with `partition_point`.

fn k_increasing(arr: &[i64], k: usize) -> i64 {
    let mut changes = 0i64;
    for r in 0..k {
        let mut tails: Vec<i64> = Vec::new();
        let mut len = 0i64;
        let mut i = r;
        while i < arr.len() {
            let x = arr[i];
            let at = tails.partition_point(|&t| t <= x);
            if at == tails.len() {
                tails.push(x);
            } else {
                tails[at] = x;
            }
            len += 1;
            i += k;
        }
        changes += len - tails.len() as i64;
    }
    changes
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2111i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut arr: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            arr.push((hi * 32768 + lo) % 100000 + 1);
        }
        arrays.push(arr);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..10usize {
        for a in 0..10usize {
            let at = round * 9973 + a;
            arrays[a][at] = arrays[a][at] % 100000 + 1;
            let got = k_increasing(&arrays[a], round + 1);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("100 solves: {} operations, checksum {}", total, check);
}
