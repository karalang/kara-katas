fn main() {
    let n: i64 = 3000;
    let passes: i64 = 40000;
    let vrange: i64 = 50;
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
        let target = p % vrange;
        for r in 0..n {
            nxt[r as usize] = if r + 1 < n { r + 1 } else { -1 };
        }
        let mut head: i64 = 0;
        while head != -1 && val[head as usize] == target {
            head = nxt[head as usize];
        }
        if head != -1 {
            let mut prev = head;
            let mut cur = nxt[head as usize];
            while cur != -1 {
                if val[cur as usize] == target {
                    nxt[prev as usize] = nxt[cur as usize];
                } else {
                    prev = cur;
                }
                cur = nxt[cur as usize];
            }
        }
        let mut pass_sum: i64 = 0;
        let mut c = head;
        while c != -1 {
            pass_sum += val[c as usize];
            c = nxt[c as usize];
        }
        sink += pass_sum;
    }
    println!("{}", sink);
}
