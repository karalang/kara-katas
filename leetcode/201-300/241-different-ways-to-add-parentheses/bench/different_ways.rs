// Benchmark harness for LeetCode #241 — Different Ways to Add Parentheses.
// Mirrors different_ways.kara algorithm-for-algorithm, including the
// deliberately unmemoized recursion.

fn tokenize(expr: &[u8]) -> Vec<i64> {
    let mut tok: Vec<i64> = Vec::new();
    let mut i = 0usize;
    let n = expr.len();
    while i < n {
        let b = expr[i] as i64;
        if b == 43 || b == 45 || b == 42 {
            tok.push(b);
            i += 1;
        } else {
            let mut v: i64 = 0;
            while i < n {
                let d = expr[i] as i64;
                if (48..=57).contains(&d) {
                    v = v * 10 + (d - 48);
                    i += 1;
                } else {
                    break;
                }
            }
            tok.push(v);
        }
    }
    tok
}

fn ways(tok: &[i64], lo: i64, hi: i64) -> Vec<i64> {
    let mut res: Vec<i64> = Vec::new();
    if lo == hi {
        res.push(tok[lo as usize]);
        return res;
    }
    let mut k = lo + 1;
    while k < hi {
        let op = tok[k as usize];
        let left = ways(tok, lo, k - 1);
        let right = ways(tok, k + 1, hi);
        for &l in &left {
            for &r in &right {
                if op == 43 {
                    res.push(l + r);
                } else if op == 45 {
                    res.push(l - r);
                } else {
                    res.push(l * r);
                }
            }
        }
        k += 2;
    }
    res
}

fn main() {
    let np: i64 = 6;
    let nops: i64 = 11;
    let iters: i64 = 30;

    let ops = ["+", "-", "*"];

    let mut toks: Vec<Vec<i64>> = Vec::new();
    for j in 0..np {
        let mut e = String::new();
        for t in 0..=nops {
            e.push_str(&format!("{}", (t % 9) + 1));
            if t < nops {
                e.push_str(ops[((t + j) % 3) as usize]);
            }
        }
        toks.push(tokenize(e.as_bytes()));
    }

    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 5) % np) as usize;
        let tk = &toks[idx];
        let vals = ways(tk, 0, tk.len() as i64 - 1);
        for v in vals {
            sink += v;
        }
    }
    println!("{}", sink);
}
