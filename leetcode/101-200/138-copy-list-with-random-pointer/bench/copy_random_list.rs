fn main() {
    let n: i64 = 3000;
    let k: i64 = 40000;
    let nu = n as usize;

    let mut oval = vec![0i64; nu];
    let mut onext = vec![0i64; nu];
    let mut ornd = vec![0i64; nu];
    let mut state: i64 = 12345;
    for i in 0..nu {
        state = (state * 1103515245 + 12345) & 2147483647;
        oval[i] = (state >> 16) % 1000;
        onext[i] = if (i as i64) + 1 < n { i as i64 + 1 } else { -1 };
        state = (state * 1103515245 + 12345) & 2147483647;
        let r = state >> 16;
        ornd[i] = if r % 4 == 0 { -1 } else { r % n };
    }

    let mut map = vec![0i64; nu];
    let mut nval = vec![0i64; nu];
    let mut nnext = vec![0i64; nu];
    let mut nrnd = vec![0i64; nu];

    let mut sink: i64 = 0;
    for p in 0..k {
        let ii = (p % n) as usize;
        ornd[ii] = (p * 37 + 11) % n;

        for i in 0..nu {
            nval[i] = oval[i];
            map[i] = i as i64;
        }
        for i in 0..nu {
            nnext[i] = if onext[i] == -1 { -1 } else { map[onext[i] as usize] };
            nrnd[i] = if ornd[i] == -1 { -1 } else { map[ornd[i] as usize] };
        }
        let mut checksum: i64 = 0;
        for i in 0..nu {
            checksum += nval[i] + nnext[i] * 7 + nrnd[i] * 13;
        }
        sink += checksum;
    }
    println!("{}", sink);
}
