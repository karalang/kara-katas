// LeetCode #1310 bench, Rust: the ★ arm (a prefix XOR, each answer the XOR
// of the prefixes at the range's two ends) on the same 10 arrays and 100
// passes.

fn xor_queries(arr: &[i64], queries: &[Vec<i64>]) -> Vec<i64> {
    let mut prefix = vec![0i64; arr.len() + 1];
    for i in 0..arr.len() {
        prefix[i + 1] = prefix[i] ^ arr[i];
    }
    queries.iter().map(|q| prefix[q[1] as usize + 1] ^ prefix[q[0] as usize]).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 30000;
    let m: i64 = 30000;
    let mut seed = 1310;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut ranges: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..10 {
        let mut arr = Vec::new();
        for _ in 0..n {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            arr.push(1 + (hi * 65536 + lo) % 1000000000);
        }
        arrays.push(arr);
        let mut queries = Vec::new();
        for _ in 0..m {
            let a = next_random(&mut seed) % n;
            let b = next_random(&mut seed) % n;
            queries.push(if a <= b { vec![a, b] } else { vec![b, a] });
        }
        ranges.push(queries);
    }
    let mut check: i64 = 0;
    for pass in 0..100 {
        for a in 0..10 {
            arrays[a][(check % n) as usize] = 1 + (check / 7) % 1000000000;
            let x = (check / 11) % n;
            let y = (check / 13) % n;
            ranges[a][(check % m) as usize] = if x <= y { vec![x, y] } else { vec![y, x] };
            let got = xor_queries(&arrays[a], &ranges[a]);
            check = (check * 31 + got[((check / 3) % m) as usize]) % 1000000007;
            check = (check * 31 + got[((check / 17) % m) as usize] + pass) % 1000000007;
        }
    }
    println!("100 passes over 10 arrays of 3 * 10^4: checksum {}", check);
}
