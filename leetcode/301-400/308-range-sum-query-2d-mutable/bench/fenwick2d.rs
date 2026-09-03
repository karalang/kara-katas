// Benchmark mirror — LeetCode 308, Range Sum Query 2D (Mutable).
// Same 2D Fenwick tree, same LCG-generated operation script, same masked sink
// as fenwick2d.kara. See ../README.md § Benchmarks.

fn main() {
    let n: i64 = 256;
    let stride: i64 = n + 1;
    let ops: i64 = 100000;
    let passes: i64 = 54;

    let mut tree: Vec<i64> = vec![0; ((n + 1) * stride) as usize];
    let mut data: Vec<i64> = vec![0; (n * n) as usize];
    let mut kind: Vec<i64> = Vec::with_capacity(ops as usize);
    let mut o1: Vec<i64> = Vec::with_capacity(ops as usize);
    let mut o2: Vec<i64> = Vec::with_capacity(ops as usize);
    let mut o3: Vec<i64> = Vec::with_capacity(ops as usize);
    let mut o4: Vec<i64> = Vec::with_capacity(ops as usize);

    let mut state: i64 = 20308;
    for _ in 0..ops {
        state = (state * 1103515245 + 12345) % 2147483648; let t = state % 2;
        state = (state * 1103515245 + 12345) % 2147483648; let a = state % n;
        state = (state * 1103515245 + 12345) % 2147483648; let b = state % n;
        state = (state * 1103515245 + 12345) % 2147483648; let c = state % n;
        state = (state * 1103515245 + 12345) % 2147483648; let d = state % n;
        kind.push(t);
        if t == 0 {
            o1.push(a); o2.push(b); o3.push(c % 2001 - 1000); o4.push(0);
        } else {
            if a <= c { o1.push(a); o3.push(c); } else { o1.push(c); o3.push(a); }
            if b <= d { o2.push(b); o4.push(d); } else { o2.push(d); o4.push(b); }
        }
    }

    let mut checksum: i64 = 0;
    for _ in 0..passes {
        for k in 0..ops as usize {
            if kind[k] == 0 {
                let r = o1[k];
                let c = o2[k];
                let delta = o3[k] - data[(r * n + c) as usize];
                data[(r * n + c) as usize] = o3[k];
                let mut x = r + 1;
                while x <= n {
                    let mut y = c + 1;
                    while y <= n {
                        tree[(x * stride + y) as usize] += delta;
                        y += y & -y;
                    }
                    x += x & -x;
                }
            } else {
                let r1 = o1[k];
                let c1 = o2[k];
                let r2 = o3[k] + 1;
                let c2 = o4[k] + 1;
                let mut total: i64 = 0;
                for qi in 0..4 {
                    let mut px = r2;
                    let mut py = c2;
                    let mut sign: i64 = 1;
                    if qi == 1 { px = r1; sign = -1; }
                    if qi == 2 { py = c1; sign = -1; }
                    if qi == 3 { px = r1; py = c1; }
                    let mut sub: i64 = 0;
                    let mut x = px;
                    while x > 0 {
                        let mut y = py;
                        while y > 0 {
                            sub += tree[(x * stride + y) as usize];
                            y -= y & -y;
                        }
                        x -= x & -x;
                    }
                    total += sign * sub;
                }
                checksum = (checksum + total) & 0x3FFFFFFF;
            }
        }
    }
    println!("checksum {}", checksum);
}
