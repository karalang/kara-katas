// LeetCode #1177: Can Make Palindrome from Substring -- the ★ arm's bench
// in Rust: the parity masks of every prefix, each query's odd letters
// counted with `count_ones()` on two masks XORed. The same string, the
// same queries and the same 200 calls.

fn can_make_pali_queries(s: &str, queries: &[Vec<i64>]) -> Vec<bool> {
    let mut masks: Vec<i64> = vec![0];
    for c in s.bytes() {
        let m = masks[masks.len() - 1] ^ (1 << (c - b'a'));
        masks.push(m);
    }
    queries
        .iter()
        .map(|q| ((masks[q[1] as usize + 1] ^ masks[q[0] as usize]).count_ones() / 2) as i64 <= q[2])
        .collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1177;
    let bytes: Vec<u8> = (0..100000).map(|_| b'a' + (next_random(&mut seed) % 26) as u8).collect();
    let s = String::from_utf8(bytes).unwrap();
    let mut queries: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100000 {
        let a = next_random(&mut seed) % 100000;
        let b = next_random(&mut seed) % 100000;
        queries.push(vec![a.min(b), a.max(b), next_random(&mut seed) % 14]);
    }
    let calls = 200;
    let mut check: i64 = 0;
    for _ in 0..calls {
        for &a in can_make_pali_queries(&s, &queries).iter() {
            check = (check * 3 + if a { 2 } else { 1 }) % 1000000007;
        }
    }
    println!("{} calls: checksum {}", calls, check);
}
