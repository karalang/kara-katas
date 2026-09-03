// Benchmark mirror — LeetCode 310, Minimum Height Trees.
// Same four CSR trees, same LCG, same leaf-peeling, same checksum-driven tree
// selection and masked sink as peel.kara. See ../README.md § Benchmarks.

fn main() {
    let n: i64 = 60000;
    let trees: i64 = 4;
    let passes: i64 = 950;

    let mut all_off: Vec<i64> = Vec::new();
    let mut all_nbr: Vec<i64> = Vec::new();
    let mut state: i64 = 20310;
    let mut deg: Vec<i64> = vec![0; n as usize];
    let mut pa: Vec<i64> = vec![0; n as usize];
    let mut cursor: Vec<i64> = vec![0; n as usize];

    for t in 0..trees {
        let window = 1 + t * 3;
        for i in 0..n as usize { deg[i] = 0; }
        pa[0] = 0;
        for i in 1..n {
            let mut w = window; if w > i { w = i; }
            state = (state * 1103515245 + 12345) % 2147483648;
            let p = i - 1 - state % w;
            pa[i as usize] = p; deg[i as usize] += 1; deg[p as usize] += 1;
        }
        let base = all_off.len() as i64;
        let mut running = all_nbr.len() as i64;
        for k in 0..n as usize { all_off.push(running); running += deg[k]; }
        all_off.push(running);
        for k in 0..n as usize { cursor[k] = all_off[(base as usize) + k]; }
        while (all_nbr.len() as i64) < running { all_nbr.push(0); }
        for i in 1..n {
            let p = pa[i as usize];
            let ci = cursor[i as usize] as usize; all_nbr[ci] = p; cursor[i as usize] += 1;
            let cp = cursor[p as usize] as usize; all_nbr[cp] = i; cursor[p as usize] += 1;
        }
    }

    let mut checksum: i64 = 0;
    let mut degree: Vec<i64> = vec![0; n as usize];
    let mut alive: Vec<i64> = vec![0; n as usize];
    let mut layer: Vec<i64> = vec![0; n as usize];
    let mut next: Vec<i64> = vec![0; n as usize];

    for p in 0..passes {
        let which = (p + checksum) % trees;
        let base = (which * (n + 1)) as usize;

        let mut lcount: i64 = 0;
        for i in 0..n as usize {
            let d = all_off[base + i + 1] - all_off[base + i];
            degree[i] = d; alive[i] = 1;
            if d == 1 { layer[lcount as usize] = i as i64; lcount += 1; }
        }

        let mut remaining = n;
        while remaining > 2 {
            remaining -= lcount;
            let mut ncount: i64 = 0;
            for k in 0..lcount as usize {
                let v = layer[k];
                alive[v as usize] = 0;
                let mut j = all_off[base + v as usize];
                while j < all_off[base + v as usize + 1] {
                    let w = all_nbr[j as usize];
                    if alive[w as usize] == 1 {
                        degree[w as usize] -= 1;
                        if degree[w as usize] == 1 { next[ncount as usize] = w; ncount += 1; }
                    }
                    j += 1;
                }
            }
            for c in 0..ncount as usize { layer[c] = next[c]; }
            lcount = ncount;
        }

        let mut acc: i64 = 0;
        for i in 0..n as usize { if alive[i] == 1 { acc += i as i64; } }
        checksum = (checksum + acc) & 0x3FFFFFFF;
    }
    println!("checksum {}", checksum);
}
