// LeetCode #1054: Distant Barcodes -- Rust mirror of bench/barcodes.kara.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn rearrange_barcodes(barcodes: &[i64]) -> Vec<i64> {
    let n = barcodes.len();
    let top = *barcodes.iter().max().unwrap() as usize;
    let mut counts = vec![0i64; top + 1];
    for &b in barcodes {
        counts[b as usize] += 1;
    }
    let mut most = 0;
    for v in 1..top + 1 {
        if counts[v] > counts[most] {
            most = v;
        }
    }
    let mut answer = vec![0i64; n];
    let mut place = 0;
    let mut v = most;
    let mut next = 1;
    for _ in 0..n {
        while counts[v] == 0 {
            v = next;
            next += 1;
        }
        answer[place] = v as i64;
        counts[v] -= 1;
        place += 2;
        if place >= n {
            place = 1;
        }
    }
    answer
}

fn main() {
    let count = 200;
    let n = 20000;
    let rounds = 25;
    let mut seed = 1054;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let common = next_random(&mut seed) % 10000 + 1;
        let copies = next_random(&mut seed) % 9000 + 1;
        let mut barcodes: Vec<i64> = Vec::new();
        for _ in 0..copies {
            barcodes.push(common);
        }
        for _ in copies..n {
            barcodes.push(next_random(&mut seed) % 10000 + 1);
        }
        all.push(barcodes);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for barcodes in all.iter() {
            let answer = rearrange_barcodes(barcodes);
            let mut h: i64 = 0;
            let mut k: usize = 0;
            while k < n as usize {
                h = (h * 10007 + answer[k]) % 1000000007;
                k += 97;
            }
            total += answer[1];
            check = (check * 131 + h) % 1000000007;
        }
    }
    println!("{count} arrays of {n} barcodes, {rounds} rounds: total {total}, checksum {check}");
}
