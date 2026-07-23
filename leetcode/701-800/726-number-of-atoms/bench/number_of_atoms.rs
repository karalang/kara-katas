use std::collections::HashMap;

fn is_upper(b: u8) -> bool { b >= b'A' && b <= b'Z' }
fn is_lower(b: u8) -> bool { b >= b'a' && b <= b'z' }
fn is_digit(b: u8) -> bool { b >= b'0' && b <= b'9' }

fn draw_hi(state: &mut i64) -> i64 {
    *state = (*state * 1103515245 + 12345) & 2147483647;
    *state >> 16
}

fn emit_element(buf: &mut Vec<u8>, dpos: &mut Vec<i64>, state: &mut i64) {
    let du = draw_hi(state);
    buf.push((b'A' as i64 + du % 6) as u8);
    if (du / 6) % 2 == 0 {
        let dl = draw_hi(state);
        buf.push((b'a' as i64 + dl % 3) as u8);
    }
    let dc = draw_hi(state);
    buf.push((b'1' as i64 + dc % 9) as u8);
    dpos.push(buf.len() as i64 - 1);
}

fn emit_mult(buf: &mut Vec<u8>, dpos: &mut Vec<i64>, state: &mut i64) {
    let dm = draw_hi(state);
    buf.push((b'0' as i64 + 2 + dm % 8) as u8);
    dpos.push(buf.len() as i64 - 1);
}

fn main() {
    let num_chunks: i64 = 20000;
    let passes: i64 = 400;
    let id_range: i64 = 24;

    let mut buf: Vec<u8> = Vec::new();
    let mut dpos: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;

    for _ in 0..num_chunks {
        let tt = draw_hi(&mut state) % 5;
        if tt == 0 {
            emit_element(&mut buf, &mut dpos, &mut state);
        } else if tt == 1 {
            emit_element(&mut buf, &mut dpos, &mut state);
            emit_element(&mut buf, &mut dpos, &mut state);
        } else if tt == 2 {
            buf.push(b'(');
            emit_element(&mut buf, &mut dpos, &mut state);
            emit_element(&mut buf, &mut dpos, &mut state);
            buf.push(b')');
            emit_mult(&mut buf, &mut dpos, &mut state);
        } else if tt == 3 {
            buf.push(b'(');
            emit_element(&mut buf, &mut dpos, &mut state);
            buf.push(b'(');
            emit_element(&mut buf, &mut dpos, &mut state);
            emit_element(&mut buf, &mut dpos, &mut state);
            buf.push(b')');
            emit_mult(&mut buf, &mut dpos, &mut state);
            buf.push(b')');
            emit_mult(&mut buf, &mut dpos, &mut state);
        } else {
            buf.push(b'(');
            emit_element(&mut buf, &mut dpos, &mut state);
            emit_element(&mut buf, &mut dpos, &mut state);
            emit_element(&mut buf, &mut dpos, &mut state);
            buf.push(b')');
            emit_mult(&mut buf, &mut dpos, &mut state);
        }
    }

    let n = buf.len() as i64;
    let ndig = dpos.len() as i64;

    let mut nid: Vec<i64> = Vec::new();
    let mut counts: Vec<i64> = Vec::new();
    let mut pst: Vec<i64> = Vec::new();
    let mut sink: i64 = 0;
    for p in 0..passes {
        let pos = dpos[(p % ndig) as usize] as usize;
        buf[pos] = (b'1' as i64 + ((buf[pos] as i64 - b'1' as i64 + 1) % 9)) as u8;

        nid.clear();
        counts.clear();
        pst.clear();

        let mut i = 0i64;
        while i < n {
            let b = buf[i as usize];
            if b == b'(' {
                pst.push(nid.len() as i64);
                i += 1;
            } else if b == b')' {
                i += 1;
                let mut mult = 0i64;
                let mut have = false;
                while i < n && is_digit(buf[i as usize]) {
                    mult = mult * 10 + (buf[i as usize] - b'0') as i64;
                    have = true;
                    i += 1;
                }
                if !have { mult = 1; }
                let start = pst.pop().unwrap();
                let mut k = start;
                while k < nid.len() as i64 {
                    counts[k as usize] *= mult;
                    k += 1;
                }
            } else if is_upper(b) {
                let up = (b - b'A') as i64;
                i += 1;
                let mut low = 0i64;
                if i < n && is_lower(buf[i as usize]) {
                    low = (buf[i as usize] - b'a') as i64 + 1;
                    i += 1;
                }
                let id = up * 4 + low;
                let mut c = 0i64;
                let mut have2 = false;
                while i < n && is_digit(buf[i as usize]) {
                    c = c * 10 + (buf[i as usize] - b'0') as i64;
                    have2 = true;
                    i += 1;
                }
                if !have2 { c = 1; }
                nid.push(id);
                counts.push(c);
            } else {
                i += 1;
            }
        }

        let mut map: HashMap<i64, i64> = HashMap::new();
        for e in 0..nid.len() {
            let id = nid[e];
            *map.entry(id).or_insert(0) += counts[e];
        }

        let mut checksum = 0i64;
        for id2 in 0..id_range {
            checksum += id2 * *map.get(&id2).unwrap_or(&0);
        }
        sink += checksum;
    }
    println!("{}", sink);
}
