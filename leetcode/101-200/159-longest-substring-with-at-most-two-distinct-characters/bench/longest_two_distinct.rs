fn longest(buf: &[i64], lo: i64, hi: i64, alphabet: i64) -> i64 {
    let mut counts = [0i64; 8];
    for a in 0..alphabet {
        counts[a as usize] = 0;
    }
    let mut distinct = 0i64;
    let mut left = lo;
    let mut best = 0i64;
    let mut right = lo;
    while right < hi {
        let c = buf[right as usize];
        if counts[c as usize] == 0 {
            distinct += 1;
        }
        counts[c as usize] += 1;
        while distinct > 2 {
            let lc = buf[left as usize];
            counts[lc as usize] -= 1;
            if counts[lc as usize] == 0 {
                distinct -= 1;
            }
            left += 1;
        }
        let w = right - left + 1;
        if w > best {
            best = w;
        }
        right += 1;
    }
    best
}

fn main() {
    let size: i64 = 20000;
    let alphabet: i64 = 8;
    let width: i64 = 96;
    let reps: i64 = 100;

    let mut buf = vec![0i64; size as usize];
    let mut state: i64 = 12345;
    for c in 0..size {
        state = (state * 1103515245 + 12345) & 2147483647;
        buf[c as usize] = state % alphabet;
    }


    let ranges = size - width;
    let mut sink: i64 = 0;
    for rep in 0..reps {
        let idx = (rep * 131 + 7) % size;
        buf[idx as usize] = (buf[idx as usize] + 1) % alphabet;
        let mut start = 0i64;
        while start < ranges {
            sink += longest(&buf, start, start + width, alphabet);
            start += 1;
        }
    }
    println!("{}", sink);
}
