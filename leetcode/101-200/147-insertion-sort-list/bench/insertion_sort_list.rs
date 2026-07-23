fn main() {
    let n: i64 = 3000;
    let passes: i64 = 60;
    let vr: i64 = 100000;

    let mut val = vec![0i64; n as usize];
    let mut nxt = vec![-1i64; n as usize];
    let mut state: i64 = 12345;
    for i in 0..n as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        val[i] = state % vr;
    }

    let mut sink: i64 = 0;
    for _p in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let idx = (state % n) as usize;
        state = (state * 1103515245 + 12345) & 2147483647;
        val[idx] = state % vr;

        let mut head: i64 = -1;
        for i in 0..n {
            let iu = i as usize;
            let v = val[iu];
            if head == -1 {
                head = i;
                nxt[iu] = -1;
            } else if val[head as usize] >= v {
                nxt[iu] = head;
                head = i;
            } else {
                let mut prev = head;
                let mut scanning = true;
                while scanning {
                    let np = nxt[prev as usize];
                    if np == -1 {
                        scanning = false;
                    } else if val[np as usize] < v {
                        prev = np;
                    } else {
                        scanning = false;
                    }
                }
                nxt[iu] = nxt[prev as usize];
                nxt[prev as usize] = i;
            }
        }

        let mut cur = head;
        let mut pos: i64 = 1;
        while cur != -1 {
            sink += pos * val[cur as usize];
            pos += 1;
            cur = nxt[cur as usize];
        }
    }
    println!("{}", sink);
}
