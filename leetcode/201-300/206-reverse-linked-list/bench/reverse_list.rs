fn main() {
    let n: i64 = 3000;
    let passes: i64 = 40000;
    let vrange: i64 = 100;
    let mut val = vec![0i64; n as usize];
    let mut nxt = vec![-1i64; n as usize];
    let mut state: i64 = 12345;
    for i in 0..n as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        val[i] = state % vrange;
        nxt[i] = -1;
    }

    let mut sink: i64 = 0;
    for p in 0..passes {
        let hit = (p % n) as usize;
        val[hit] += 1;
        for r in 0..n {
            nxt[r as usize] = if r + 1 < n { r + 1 } else { -1 };
        }
        let mut prev: i64 = -1;
        let mut cur: i64 = 0;
        while cur != -1 {
            let saved = nxt[cur as usize];
            nxt[cur as usize] = prev;
            prev = cur;
            cur = saved;
        }
        let head = prev;
        let mut pass_sum: i64 = 0;
        let mut idx: i64 = 0;
        let mut c = head;
        while c != -1 {
            pass_sum += (idx + 1) * val[c as usize];
            idx += 1;
            c = nxt[c as usize];
        }
        sink += pass_sum;
    }
    println!("{}", sink);
}
