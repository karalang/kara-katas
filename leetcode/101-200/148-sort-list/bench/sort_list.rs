fn split_mid(nxt: &mut [i64], head: i64) -> i64 {
    let mut slow = head;
    let mut fast = nxt[head as usize];
    while fast != -1 {
        fast = nxt[fast as usize];
        if fast != -1 {
            slow = nxt[slow as usize];
            fast = nxt[fast as usize];
        }
    }
    let mid = nxt[slow as usize];
    nxt[slow as usize] = -1;
    mid
}

fn merge(val: &[i64], nxt: &mut [i64], a: i64, b: i64) -> i64 {
    let mut ai = a;
    let mut bi = b;
    let mut head: i64 = -1;
    let mut tail: i64 = -1;
    while ai != -1 && bi != -1 {
        if val[ai as usize] <= val[bi as usize] {
            if head == -1 { head = ai; } else { nxt[tail as usize] = ai; }
            tail = ai;
            ai = nxt[ai as usize];
        } else {
            if head == -1 { head = bi; } else { nxt[tail as usize] = bi; }
            tail = bi;
            bi = nxt[bi as usize];
        }
    }
    let rest = if ai != -1 { ai } else { bi };
    if tail != -1 {
        if rest == -1 { nxt[tail as usize] = -1; } else { nxt[tail as usize] = rest; }
    }
    head
}

fn sort_chain(val: &[i64], nxt: &mut [i64], head: i64) -> i64 {
    if head == -1 { return -1; }
    if nxt[head as usize] == -1 { return head; }
    let mid = split_mid(nxt, head);
    let left = sort_chain(val, nxt, head);
    let right = sort_chain(val, nxt, mid);
    merge(val, nxt, left, right)
}

fn main() {
    let n: i64 = 20000;
    let passes: i64 = 180;
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

        for i in 0..(n - 1) as usize {
            nxt[i] = i as i64 + 1;
        }
        nxt[(n - 1) as usize] = -1;

        let head = sort_chain(&val, &mut nxt, 0);

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
