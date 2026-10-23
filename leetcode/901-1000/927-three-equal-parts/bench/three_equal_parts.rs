// LeetCode #927: Three Equal Parts -- bench: three pointers.
// Mirrors three_equal_parts.kara.

fn three_equal_parts(arr: &[i64]) -> Vec<i64> {
    let n = arr.len();
    let ones: i64 = arr.iter().sum();
    if ones == 0 {
        return vec![0, n as i64 - 1];
    }
    if ones % 3 != 0 {
        return vec![-1, -1];
    }
    let third = ones / 3;
    let mut starts: Vec<usize> = Vec::new();
    let mut seen = 0;
    for k in 0..n {
        if arr[k] == 1 {
            if seen % third == 0 {
                starts.push(k);
            }
            seen += 1;
        }
    }
    let (mut a, mut b, mut c) = (starts[0], starts[1], starts[2]);
    while c < n && arr[a] == arr[b] && arr[b] == arr[c] {
        a += 1;
        b += 1;
        c += 1;
    }
    if c == n {
        vec![a as i64 - 1, b as i64]
    } else {
        vec![-1, -1]
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count) = (30, 100);
    let mut seed = 927;
    // count arrays of 30000 digits, built once: a value of 9000 digits
    // written three times, each copy after up to 1000 leading 0s and the
    // array filled up with 0s in front, and every other array with one
    // digit flipped
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..count {
        let value: Vec<i64> = (0..9000).map(|_| next_random(&mut seed) % 2).collect();
        let mut parts: Vec<i64> = Vec::new();
        for _ in 0..3 {
            for _ in 0..next_random(&mut seed) % 1001 {
                parts.push(0);
            }
            parts.extend_from_slice(&value);
        }
        let mut arr = vec![0i64; 30000 - parts.len()];
        arr.extend_from_slice(&parts);
        if a % 2 == 1 {
            let at = (next_random(&mut seed) % 30000) as usize;
            arr[at] = 1 - arr[at];
        }
        arrays.push(arr);
    }
    let mut found = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round visits every array, starting from a different one
        for i in 0..count {
            let got = three_equal_parts(&arrays[(r + i) % count]);
            if got[0] >= 0 {
                found += 1;
            }
            check = (check * 1000003 + got[0] + 1) % 1000000007;
            check = (check * 1000003 + got[1] + 1) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} arrays of 30000: {found} split, checksum {check}");
}
