// LeetCode 306 - Additive Number.
//
// Mirror of additive.kara: the same O(n^3) scan (two prefix lengths, then
// verification by exact digit-list addition) over the same flat digit array,
// with the same planted positives, the same per-pass perturbation and the same
// masked sink. Kept algorithm-for-algorithm so the benchmark lane is honest.

fn add_digits(a: &[i64], b: &[i64]) -> Vec<i64> {
    let mut rev: Vec<i64> = Vec::new();
    let (mut i, mut j) = (a.len() as i64 - 1, b.len() as i64 - 1);
    let mut carry = 0i64;
    while i >= 0 || j >= 0 || carry > 0 {
        let mut s = carry;
        if i >= 0 { s += a[i as usize]; i -= 1; }
        if j >= 0 { s += b[j as usize]; j -= 1; }
        rev.push(s % 10);
        carry = s / 10;
    }
    let mut out: Vec<i64> = Vec::with_capacity(rev.len());
    for k in (0..rev.len()).rev() { out.push(rev[k]); }
    out
}

fn matches_at(flat: &[i64], base: usize, n: usize, pos: usize, num: &[i64]) -> bool {
    if pos + num.len() > n { return false; }
    for k in 0..num.len() { if flat[base + pos + k] != num[k] { return false; } }
    true
}

fn no_lead_zero(flat: &[i64], base: usize, lo: usize, hi: usize) -> bool {
    hi - lo == 1 || flat[base + lo] != 0
}

fn is_additive(flat: &[i64], base: usize, n: usize) -> bool {
    if n < 3 { return false; }
    for len1 in 1..(n - 1) {
        if !no_lead_zero(flat, base, 0, len1) { break; }
        for len2 in 1..(n - len1) {
            if !no_lead_zero(flat, base, len1, len1 + len2) { break; }
            let mut a: Vec<i64> = flat[base..base + len1].to_vec();
            let mut b: Vec<i64> = flat[base + len1..base + len1 + len2].to_vec();
            let mut pos = len1 + len2;
            let mut ok = true;
            let mut steps = 0;
            while pos < n && ok {
                let c = add_digits(&a, &b);
                if matches_at(flat, base, n, pos, &c) {
                    pos += c.len();
                    a = b;
                    b = c;
                    steps += 1;
                } else { ok = false; }
            }
            if ok && pos == n && steps > 0 { return true; }
        }
    }
    false
}

fn main() {
    let planted: [&str; 8] = ["022461016264268110", "020204060100160260", "021214263105168273", "022224466110176286", "023234669115184299", "024244872120192312", "025255075125200325", "026265278130208338"];
    const CASES: usize = 220;
    const WIDTH: usize = 18;
    const PASSES: i64 = 90;
    const MASK: i64 = 1073741823;

    let mut flat: Vec<i64> = Vec::with_capacity(CASES * WIDTH);
    let mut seed: i64 = 7;
    for c in 0..CASES {
        if c % 25 == 0 {
            let p = planted[(c / 25) % planted.len()].as_bytes();
            for i in 0..WIDTH { flat.push((p[i] - b'0') as i64); }
        } else {
            for _ in 0..WIDTH {
                seed = (seed * 1103515245 + 12345) % 2147483647;
                flat.push(seed % 10);
            }
        }
    }

    let mut checksum: i64 = 1;
    for pass in 0..PASSES {
        let site = ((checksum * 31 + pass * 7919) % (CASES as i64 * WIDTH as i64)) as usize;
        flat[site] = (flat[site] + 1) % 10;
        let mut hits: i64 = 0;
        for c in 0..CASES { if is_additive(&flat, c * WIDTH, WIDTH) { hits += 1; } }
        checksum = (checksum * 131 + hits * 7919 + site as i64) & MASK;
    }
    println!("checksum {}", checksum);
}
