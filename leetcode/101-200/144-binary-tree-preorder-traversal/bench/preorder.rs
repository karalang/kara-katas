fn main() {
    let n: i64 = 50000;
    let passes: i64 = 400;
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

    let mut stack = vec![0i64; nu];
    let mut sink: i64 = 0;
    for p in 0..passes {
        let idx = (p % n) as usize;
        val[idx] += 1;

        let mut sp = 0usize;
        stack[sp] = 0;
        sp += 1;
        let mut pos: i64 = 0;
        let mut acc: i64 = 0;
        while sp > 0 {
            sp -= 1;
            let node = stack[sp] as usize;
            acc += val[node] * (pos + 1);
            pos += 1;
            let r = right[node];
            let l = left[node];
            if r >= 0 { stack[sp] = r; sp += 1; }
            if l >= 0 { stack[sp] = l; sp += 1; }
        }
        sink += acc;
    }
    println!("{}", sink);
}
