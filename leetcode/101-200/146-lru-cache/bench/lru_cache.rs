use std::collections::HashMap;

fn main() {
    let cap: i64 = 1024;
    let key_range: i64 = 4096;
    let ops: i64 = 32000000;

    let pool = (cap + 2) as usize;
    let mut nkey = vec![-1i64; pool];
    let mut nval = vec![0i64; pool];
    let mut nprev = vec![-1i64; pool];
    let mut nnext = vec![-1i64; pool];
    nnext[0] = 1;
    nprev[1] = 0;

    let mut map: HashMap<i64, i64> = HashMap::new();
    let mut size: i64 = 0;
    let mut sink: i64 = 0;
    let mut state: i64 = 12345;

    for _ in 0..ops {
        state = (state * 1103515245 + 12345) & 2147483647;
        let h1 = state >> 16;
        state = (state * 1103515245 + 12345) & 2147483647;
        let h2 = state >> 16;
        let key = h2 % key_range;

        if h1 % 2 == 0 {
            let idx = *map.get(&key).unwrap_or(&-1);
            let mut r: i64 = -1;
            if idx >= 0 {
                let iu = idx as usize;
                let pi = nprev[iu] as usize;
                let ni = nnext[iu] as usize;
                nnext[pi] = ni as i64;
                nprev[ni] = pi as i64;
                let first = nnext[0] as usize;
                nprev[iu] = 0;
                nnext[iu] = first as i64;
                nprev[first] = idx;
                nnext[0] = idx;
                r = nval[iu];
            }
            sink += r + 1;
        } else {
            state = (state * 1103515245 + 12345) & 2147483647;
            let v = state >> 16;
            let existing = *map.get(&key).unwrap_or(&-1);
            if existing >= 0 {
                let eu = existing as usize;
                nval[eu] = v;
                let pi = nprev[eu] as usize;
                let ni = nnext[eu] as usize;
                nnext[pi] = ni as i64;
                nprev[ni] = pi as i64;
                let first = nnext[0] as usize;
                nprev[eu] = 0;
                nnext[eu] = first as i64;
                nprev[first] = existing;
                nnext[0] = existing;
            } else {
                let idx: i64;
                if size < cap {
                    idx = 2 + size;
                    size += 1;
                } else {
                    let lru = nprev[1];
                    let lu = lru as usize;
                    let pl = nprev[lu] as usize;
                    let nl = nnext[lu] as usize;
                    nnext[pl] = nl as i64;
                    nprev[nl] = pl as i64;
                    map.remove(&nkey[lu]);
                    idx = lru;
                }
                let iu = idx as usize;
                nkey[iu] = key;
                nval[iu] = v;
                map.insert(key, idx);
                let first = nnext[0] as usize;
                nprev[iu] = 0;
                nnext[iu] = first as i64;
                nprev[first] = idx;
                nnext[0] = idx;
            }
        }
    }
    println!("{}", sink);
}
