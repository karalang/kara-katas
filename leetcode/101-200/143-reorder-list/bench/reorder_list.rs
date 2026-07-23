// Build-once + punch reorder-list over an index pool (see reorder_list.kara).
// Each pass generates the interleaved order, rewires nxt, and walks it, folding a
// position-weighted checksum into the sink.
fn main() {
    let n: i64 = 100000;
    let k: i64 = 1000;
    let valmod: i64 = 1000;

    let mut vals: Vec<i64> = vec![0; n as usize];
    let mut nxt: Vec<i64> = vec![0; n as usize];
    let mut order: Vec<i64> = vec![0; n as usize];

    let mut state: i64 = 12345;
    for i in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        vals[i as usize] = (state >> 16) % valmod;
    }

    let mut sink: i64 = 0;
    for p in 0..k {
        let pi = p % n;
        vals[pi as usize] = (vals[pi as usize] + 1) % valmod;

        let mut lo = 0i64;
        let mut hi = n - 1;
        let mut idx = 0i64;
        let mut take_lo = true;
        while lo <= hi {
            if take_lo {
                order[idx as usize] = lo;
                lo += 1;
            } else {
                order[idx as usize] = hi;
                hi -= 1;
            }
            take_lo = !take_lo;
            idx += 1;
        }

        let mut r = 0i64;
        while r + 1 < n {
            nxt[order[r as usize] as usize] = order[(r + 1) as usize];
            r += 1;
        }
        nxt[order[(n - 1) as usize] as usize] = -1;

        let mut cur = order[0];
        let mut pos = 0i64;
        while cur >= 0 {
            let w = (pos % 997) + 1;
            sink += w * vals[cur as usize];
            pos += 1;
            cur = nxt[cur as usize];
        }
    }

    println!("{}", sink);
}
