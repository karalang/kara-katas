// Build-once + punch Floyd two-phase cycle-entry detection over an index-pool of
// K lists (see linked_list_cycle_ii.kara). nxt[i] = next global index or -1.
fn detect(nxt: &[i64], head: i64) -> i64 {
    let mut slow = head;
    let mut fast = head;
    // Phase 1: find a meeting point (or fall off the end -> -1). The loop only
    // exits via `break` once slow == fast, so no separate `met` flag is needed.
    loop {
        fast = nxt[fast as usize];
        if fast < 0 {
            return -1;
        }
        fast = nxt[fast as usize];
        if fast < 0 {
            return -1;
        }
        slow = nxt[slow as usize];
        if slow == fast {
            break;
        }
    }
    slow = head;
    while slow != fast {
        slow = nxt[slow as usize];
        fast = nxt[fast as usize];
    }
    slow - head
}

fn main() {
    let k_lists: i64 = 1000;
    let len: i64 = 60;
    let passes: i64 = 3000;
    let cycpct: i64 = 50;
    let pool = k_lists * len;

    let mut nxt: Vec<i64> = vec![0; pool as usize];
    let mut target: Vec<i64> = Vec::new();
    let mut tail: Vec<i64> = Vec::new();

    let mut state: i64 = 12345;

    for k in 0..k_lists {
        let base = k * len;
        for j in 0..len - 1 {
            nxt[(base + j) as usize] = base + j + 1;
        }
        let t = base + len - 1;
        tail.push(t);

        state = (state * 1103515245 + 12345) & 2147483647;
        let coin = (state >> 16) % 100;
        state = (state * 1103515245 + 12345) & 2147483647;
        let tl = (state >> 16) % len;
        target.push(base + tl);

        if coin < cycpct {
            nxt[t as usize] = base + tl;
        } else {
            nxt[t as usize] = -1;
        }
    }

    let mut sink: i64 = 0;
    for pass in 0..passes {
        let idx = pass % k_lists;
        let ti = tail[idx as usize];
        if nxt[ti as usize] < 0 {
            nxt[ti as usize] = target[idx as usize];
        } else {
            nxt[ti as usize] = -1;
        }

        for kk in 0..k_lists {
            let e = detect(&nxt, kk * len);
            sink += e + 1;
        }
    }

    println!("{}", sink);
}
