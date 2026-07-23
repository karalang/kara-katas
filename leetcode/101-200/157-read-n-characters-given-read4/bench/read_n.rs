struct Reader {
    pos: i64,
    chk: i64,
}

fn read4(src: &[i64], rd: &mut Reader) -> i64 {
    let m = src.len() as i64;
    let mut cnt = 0i64;
    while cnt < 4 && rd.pos < m {
        rd.pos += 1;
        cnt += 1;
    }
    cnt
}

fn read_n(src: &[i64], rd: &mut Reader, want: i64) -> i64 {
    let mut total = 0i64;
    let mut acc = rd.chk;
    let mut eof = false;
    while total < want && !eof {
        let start = rd.pos;
        let cnt = read4(src, rd);
        if cnt == 0 {
            eof = true;
        } else {
            let take = if total + cnt <= want { cnt } else { want - total };
            let mut k = 0i64;
            while k < take {
                acc = (acc * 1103515245 + src[(start + k) as usize] + 1) & 2147483647;
                k += 1;
            }
            total += take;
        }
    }
    rd.chk = acc;
    total
}

fn main() {
    let size: i64 = 50000;
    let want: i64 = 7;
    let passes: i64 = 3200;

    let mut src = vec![0i64; size as usize];
    let mut state: i64 = 12345;
    for c in 0..size {
        state = (state * 1103515245 + 12345) & 2147483647;
        src[c as usize] = state % 26;
    }

    let mut rd = Reader { pos: 0, chk: 0 };
    for pass in 0..passes {
        let idx = (pass * 131 + 7) % size;
        src[idx as usize] = (src[idx as usize] + 1) % 26;
        rd.pos = 0;
        let mut cont = true;
        while cont {
            let got = read_n(&src, &mut rd, want);
            if got == 0 {
                cont = false;
            }
        }
    }
    println!("{}", rd.chk);
}
