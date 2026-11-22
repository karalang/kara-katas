// LeetCode #2840: Check if Strings Can be Made Equal With Operations II
// -- the bench, mirrored from strings.kara: counts in one table of
// 2 x 26, s1 up and s2 down.

fn check_strings(s1: &str, s2: &str) -> bool {
    let mut count: Vec<i64> = vec![0; 52];
    for (i, (a, b)) in s1.bytes().zip(s2.bytes()).enumerate() {
        let side = i % 2 * 26;
        count[side + (a - b'a') as usize] += 1;
        count[side + (b - b'a') as usize] -= 1;
    }
    count.iter().all(|&n| n == 0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 200;
    let n: usize = 100000;
    let rounds = 20;
    let mut seed = 2840;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for c in 0..count {
        let a: Vec<u8> = (0..n).map(|_| (97 + next_random(&mut seed) % 26) as u8).collect();
        let mut b = a.clone();
        for i in (2..n).rev() {
            let j = i % 2 + 2 * (next_random(&mut seed) as usize % (i / 2 + 1));
            if j <= i {
                b.swap(i, j);
            }
        }
        if c % 2 == 1 {
            let k = next_random(&mut seed) as usize % n;
            b[k] = (97 + next_random(&mut seed) % 26) as u8;
        }
        pairs.push((String::from_utf8(a).unwrap(), String::from_utf8(b).unwrap()));
    }
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (s1, s2) in pairs.iter() {
            let same = check_strings(s1, s2);
            if same {
                yes += 1;
            }
            check = (check * 31 + if same { 2 } else { 1 } + r) % 1000000007;
        }
    }
    println!("{count} pairs of {n}, {rounds} rounds: {yes} true, checksum {check}");
}
