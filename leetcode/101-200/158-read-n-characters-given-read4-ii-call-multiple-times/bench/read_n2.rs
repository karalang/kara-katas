struct Reader {
    pos: i64,
    chk: i64,
    buf_start: i64,
    buf_len: i64,
    buf_pos: i64,
}

fn read4(src: &[i64], rd: &mut Reader) -> i64 {
    let m = src.len() as i64;
    rd.buf_start = rd.pos;
    let mut cnt = 0i64;
    while cnt < 4 && rd.pos < m {
        rd.pos += 1;
        cnt += 1;
    }
    rd.buf_len = cnt;
    rd.buf_pos = 0;
    cnt
}

fn read_n(src: &[i64], rd: &mut Reader, want: i64) -> i64 {
    let mut total = 0i64;
    let mut acc = rd.chk;
    let mut eof = false;
    while total < want && !eof {
        if rd.buf_pos >= rd.buf_len {
            let cnt = read4(src, rd);
            if cnt == 0 {
                eof = true;
            }
        }
        if !eof {
            let c = src[(rd.buf_start + rd.buf_pos) as usize];
            acc = (acc * 1103515245 + c + 1) & 2147483647;
            rd.buf_pos += 1;
            total += 1;
        }
    }
    rd.chk = acc;
    total
}

fn main() {
    let size: i64 = 50000;
    let want: i64 = 3;
    let passes: i64 = 2600;

    let mut src = vec![0i64; size as usize];
    let mut state: i64 = 12345;
    for c in 0..size {
        state = (state * 1103515245 + 12345) & 2147483647;
        src[c as usize] = state % 26;
    }

    let mut rd = Reader {
        pos: 0,
        chk: 0,
        buf_start: 0,
        buf_len: 0,
        buf_pos: 0,
    };
    for pass in 0..passes {
        let idx = (pass * 131 + 7) % size;
        src[idx as usize] = (src[idx as usize] + 1) % 26;
        rd.pos = 0;
        rd.buf_len = 0;
        rd.buf_pos = 0;
        rd.buf_start = 0;
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
