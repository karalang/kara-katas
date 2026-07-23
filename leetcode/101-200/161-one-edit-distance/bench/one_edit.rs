fn tails_equal(s: &[i64], l: &[i64], ss: i64, se: i64, ls: i64, le: i64) -> bool {
    let mut a = ss;
    let mut b = ls;
    while a < se && b < le {
        if s[a as usize] != l[b as usize] {
            return false;
        }
        a += 1;
        b += 1;
    }
    a == se && b == le
}

fn check(s: &[i64], so: i64, m: i64, l: &[i64], lo: i64, n: i64) -> bool {
    if n - m > 1 {
        return false;
    }
    let mut i = 0i64;
    while i < m {
        if s[(so + i) as usize] != l[(lo + i) as usize] {
            if m == n {
                return tails_equal(s, l, so + i + 1, so + m, lo + i + 1, lo + n);
            }
            return tails_equal(s, l, so + i, so + m, lo + i + 1, lo + n);
        }
        i += 1;
    }
    n - m == 1
}

fn is_one_edit(a: &[i64], oa: i64, la: i64, b: &[i64], ob: i64, lb: i64) -> bool {
    if la <= lb {
        return check(a, oa, la, b, ob, lb);
    }
    check(b, ob, lb, a, oa, la)
}

fn main() {
    let pairs: i64 = 4000;
    let l: i64 = 48;
    let reps: i64 = 3000;
    let stride = l + 2;
    let cap = pairs * stride;

    let mut buf_a = vec![0i64; cap as usize];
    let mut buf_b = vec![0i64; cap as usize];
    let mut len_a = vec![0i64; pairs as usize];
    let mut len_b = vec![0i64; pairs as usize];

    let mut state: i64 = 12345;
    for pi in 0..pairs {
        let oa = pi * stride;
        let ob = pi * stride;
        for k in 0..l {
            state = (state * 1103515245 + 12345) & 2147483647;
            buf_a[(oa + k) as usize] = state % 26;
        }
        len_a[pi as usize] = l;
        state = (state * 1103515245 + 12345) & 2147483647;
        let kind = state % 4;
        if kind == 0 {
            for j in 0..l {
                buf_b[(ob + j) as usize] = buf_a[(oa + j) as usize];
            }
            state = (state * 1103515245 + 12345) & 2147483647;
            let pos = state % l;
            buf_b[(ob + pos) as usize] = (buf_a[(oa + pos) as usize] + 1) % 26;
            len_b[pi as usize] = l;
        } else if kind == 1 {
            state = (state * 1103515245 + 12345) & 2147483647;
            let pos = state % (l + 1);
            for j in 0..pos {
                buf_b[(ob + j) as usize] = buf_a[(oa + j) as usize];
            }
            state = (state * 1103515245 + 12345) & 2147483647;
            buf_b[(ob + pos) as usize] = state % 26;
            for t in pos..l {
                buf_b[(ob + t + 1) as usize] = buf_a[(oa + t) as usize];
            }
            len_b[pi as usize] = l + 1;
        } else if kind == 2 {
            state = (state * 1103515245 + 12345) & 2147483647;
            let pos = state % l;
            let mut w = 0i64;
            for j in 0..l {
                if j != pos {
                    buf_b[(ob + w) as usize] = buf_a[(oa + j) as usize];
                    w += 1;
                }
            }
            len_b[pi as usize] = l - 1;
        } else {
            for j in 0..l {
                buf_b[(ob + j) as usize] = buf_a[(oa + j) as usize];
            }
            state = (state * 1103515245 + 12345) & 2147483647;
            let p1 = state % l;
            state = (state * 1103515245 + 12345) & 2147483647;
            let p2 = (p1 + 1 + state % (l - 1)) % l;
            buf_b[(ob + p1) as usize] = (buf_a[(oa + p1) as usize] + 1) % 26;
            buf_b[(ob + p2) as usize] = (buf_a[(oa + p2) as usize] + 1) % 26;
            len_b[pi as usize] = l;
        }
    }

    let mut sink: i64 = 0;
    for rep in 0..reps {
        let idx = rep % pairs;
        let col = (rep * 7 + 3) % l;
        let oa = idx * stride;
        buf_a[(oa + col) as usize] = (buf_a[(oa + col) as usize] + 1) % 26;
        for i in 0..pairs {
            let o = i * stride;
            if is_one_edit(&buf_a, o, len_a[i as usize], &buf_b, o, len_b[i as usize]) {
                sink += 1;
            }
        }
    }
    println!("{}", sink);
}
