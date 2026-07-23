fn list_length(next: &[i64], head: i64) -> i64 {
    let mut n = 0i64;
    let mut cur = head;
    while cur != -1 {
        n += 1;
        cur = next[cur as usize];
    }
    n
}

fn advance(next: &[i64], head: i64, k: i64) -> i64 {
    let mut cur = head;
    let mut i = 0i64;
    while i < k {
        cur = next[cur as usize];
        i += 1;
    }
    cur
}

fn intersection(next: &[i64], head_a: i64, head_b: i64) -> i64 {
    let la = list_length(next, head_a);
    let lb = list_length(next, head_b);
    let mut a = head_a;
    let mut b = head_b;
    if la > lb {
        a = advance(next, a, la - lb);
    } else {
        b = advance(next, b, lb - la);
    }
    while a != -1 && b != -1 {
        if a == b {
            return a;
        }
        a = next[a as usize];
        b = next[b as usize];
    }
    -1
}

fn main() {
    let n: i64 = 100003;
    let heads = n / 8;
    let passes: i64 = 280;

    let mut order = vec![0i64; n as usize];
    for k in 0..n {
        order[k as usize] = (k * 48271) % n;
    }

    let mut next = vec![-1i64; n as usize];
    for j in 0..n - 1 {
        next[order[j as usize] as usize] = order[(j + 1) as usize];
    }

    let mut sink: i64 = 0;
    for p in 0..passes {
        let sa = p % heads;
        let sb = (p * 131 + 7) % heads;
        let ha = order[sa as usize];
        let hb = order[sb as usize];
        let idx = intersection(&next, ha, hb);
        sink += idx;
    }
    println!("{}", sink);
}
