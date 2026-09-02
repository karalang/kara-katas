// Benchmark mirror — LeetCode 307, Range Sum Query (Mutable).
// Same Fenwick tree, same LCG-generated operation script, same masked sink as
// fenwick.kara. See ../README.md § Benchmarks.

fn main() {
    let n: i64 = 65536;
    let ops: i64 = 200000;
    let passes: i64 = 110;

    let mut tree: Vec<i64> = vec![0; (n + 1) as usize];
    let mut data: Vec<i64> = vec![0; n as usize];
    let mut kind: Vec<i64> = Vec::with_capacity(ops as usize);
    let mut opa: Vec<i64> = Vec::with_capacity(ops as usize);
    let mut opb: Vec<i64> = Vec::with_capacity(ops as usize);

    let mut state: i64 = 20307;
    for _ in 0..ops {
        state = (state * 1103515245 + 12345) % 2147483648;
        let t = state % 2;
        state = (state * 1103515245 + 12345) % 2147483648;
        let x = state % n;
        state = (state * 1103515245 + 12345) % 2147483648;
        let y = state % n;
        kind.push(t);
        if t == 0 {
            opa.push(x);
            opb.push(y % 2001 - 1000);
        } else if x <= y {
            opa.push(x);
            opb.push(y);
        } else {
            opa.push(y);
            opb.push(x);
        }
    }

    let mut checksum: i64 = 0;
    for _ in 0..passes {
        for k in 0..ops as usize {
            if kind[k] == 0 {
                let i = opa[k];
                let delta = opb[k] - data[i as usize];
                data[i as usize] = opb[k];
                let mut x = i + 1;
                while x <= n {
                    tree[x as usize] += delta;
                    x += x & -x;
                }
            } else {
                let mut total: i64 = 0;
                let mut hi = opb[k] + 1;
                while hi > 0 {
                    total += tree[hi as usize];
                    hi -= hi & -hi;
                }
                let mut lo = opa[k];
                while lo > 0 {
                    total -= tree[lo as usize];
                    lo -= lo & -lo;
                }
                checksum = (checksum + total) & 0x3FFFFFFF;
            }
        }
    }
    println!("checksum {}", checksum);
}
