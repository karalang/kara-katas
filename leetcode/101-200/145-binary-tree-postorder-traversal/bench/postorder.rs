fn main() {
    let n: i64 = 50000;
    let passes: i64 = 250;
    let nu = n as usize;

    let mut val = vec![0i64; nu];
    let mut left = vec![-1i64; nu];
    let mut right = vec![-1i64; nu];

    let mut state: i64 = 12345;
    for i in 0..nu {
        state = (state * 1103515245 + 12345) & 2147483647;
        val[i] = state >> 16;
    }

    for i in 1..nu {
        let mut cur = 0usize;
        loop {
            if val[i] < val[cur] {
                if left[cur] < 0 { left[cur] = i as i64; break; }
                else { cur = left[cur] as usize; }
            } else {
                if right[cur] < 0 { right[cur] = i as i64; break; }
                else { cur = right[cur] as usize; }
            }
        }
    }

    let mut s1 = vec![0i64; nu];
    let mut s2 = vec![0i64; nu];
    let mut sink: i64 = 0;
    for p in 0..passes {
        let idx = (p % n) as usize;
        val[idx] += 1;

        let mut s1p = 0usize;
        s1[s1p] = 0;
        s1p += 1;
        let mut s2p = 0usize;
        while s1p > 0 {
            s1p -= 1;
            let node = s1[s1p] as usize;
            s2[s2p] = node as i64;
            s2p += 1;
            let l = left[node];
            let r = right[node];
            if l >= 0 { s1[s1p] = l; s1p += 1; }
            if r >= 0 { s1[s1p] = r; s1p += 1; }
        }
        let mut pos: i64 = 0;
        let mut acc: i64 = 0;
        while s2p > 0 {
            s2p -= 1;
            let node = s2[s2p] as usize;
            acc += val[node] * (pos + 1);
            pos += 1;
        }
        sink += acc;
    }
    println!("{}", sink);
}
