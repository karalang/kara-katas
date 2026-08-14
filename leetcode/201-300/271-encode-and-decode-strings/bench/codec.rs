// Benchmark workload for LeetCode #271 — Encode and Decode Strings.
//
// Algorithm-for-algorithm mirror of codec.kara. See that file's header for what
// this lane measures and for the two parity decisions (hand-rolled decimal in
// every language; every buffer hoisted out of the punch loop).

fn main() {
    let count: i64 = 50000;
    let rounds: i64 = 250;

    // ---- build once: a flat corpus --------------------------------------
    let mut src: Vec<u8> = Vec::new();
    let mut off: Vec<i64> = Vec::new();
    let mut len: Vec<i64> = Vec::new();
    let mut state: i64 = 271271;
    for _ in 0..count {
        state = (state * 1103515245 + 12345) & 2147483647;
        let n = (state / 65536) % 25;
        off.push(src.len() as i64);
        len.push(n);
        for _ in 0..n {
            state = (state * 1103515245 + 12345) & 2147483647;
            src.push((97 + (state / 65536) % 26) as u8);
        }
    }

    // ---- hoisted working buffers ----------------------------------------
    let enc_cap = src.len() as i64 + count * 3;
    let mut enc: Vec<u8> = vec![0u8; enc_cap as usize];
    let mut dout: Vec<u8> = vec![0u8; src.len()];

    // ---- punch -----------------------------------------------------------
    let mut sink: i64 = 0;
    for _ in 0..rounds {
        let mut w: i64 = 0;
        for k in 0..count {
            let n = len[k as usize];
            if n >= 10 {
                enc[w as usize] = (48 + n / 10) as u8;
                w += 1;
            }
            enc[w as usize] = (48 + n % 10) as u8;
            w += 1;
            enc[w as usize] = 35; // '#'
            w += 1;
            let base = off[k as usize];
            for p in 0..n {
                enc[(w + p) as usize] = src[(base + p) as usize];
            }
            w += n;
        }
        let encoded_len = w;

        let mut rp: i64 = 0;
        let mut dp: i64 = 0;
        let mut items: i64 = 0;
        let mut check: i64 = 0;
        while rp < encoded_len {
            let mut n: i64 = 0;
            while enc[rp as usize] != 35 {
                n = n * 10 + (enc[rp as usize] as i64 - 48);
                rp += 1;
            }
            rp += 1;
            for p in 0..n {
                dout[(dp + p) as usize] = enc[(rp + p) as usize];
            }
            check = (check * 31 + n) % 1000000007;
            rp += n;
            dp += n;
            items += 1;
        }
        sink = (sink * 131 + check + items) % 1000000007;
    }

    println!("{sink}");
}
