// ASCII: '+'=43 '-'=45 '('=40 ')'=41 '0'=48 '9'=57
fn calculate(bytes: &[i64], n: i64) -> i64 {
    let mut result = 0i64;
    let mut sign = 1i64;
    let mut stack: Vec<i64> = Vec::new();
    let mut i = 0i64;
    while i < n {
        let b = bytes[i as usize];
        if b >= 48 && b <= 57 {
            let mut num = 0i64;
            while i < n && bytes[i as usize] >= 48 && bytes[i as usize] <= 57 {
                num = num * 10 + (bytes[i as usize] - 48);
                i += 1;
            }
            result = result + sign * num;
        } else if b == 43 {
            sign = 1;
            i += 1;
        } else if b == 45 {
            sign = -1;
            i += 1;
        } else if b == 40 {
            stack.push(result);
            stack.push(sign);
            result = 0;
            sign = 1;
            i += 1;
        } else if b == 41 {
            let saved_sign = stack.pop().unwrap_or(1);
            let saved_result = stack.pop().unwrap_or(0);
            result = saved_result + saved_sign * result;
            i += 1;
        } else {
            i += 1;
        }
    }
    result
}

fn push_number(buf: &mut Vec<i64>, num: i64) {
    if num >= 100 {
        buf.push(48 + num / 100);
        buf.push(48 + (num / 10) % 10);
        buf.push(48 + num % 10);
    } else if num >= 10 {
        buf.push(48 + num / 10);
        buf.push(48 + num % 10);
    } else {
        buf.push(48 + num);
    }
}

fn main() {
    let nums: i64 = 250000;
    let passes: i64 = 80;
    let max_depth: i64 = 16;
    let modulus: i64 = 1000000007;

    let mut buf: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    let mut depth = 0i64;

    state = (state * 1103515245 + 12345) & 2147483647;
    push_number(&mut buf, state % 1000);

    let mut t = 1i64;
    while t < nums {
        state = (state * 1103515245 + 12345) & 2147483647;
        if state % 2 == 0 { buf.push(43); } else { buf.push(45); }

        state = (state * 1103515245 + 12345) & 2147483647;
        let opens = state % 3;
        let mut opened_here = false;
        let mut o = 0i64;
        while o < opens {
            if depth < max_depth {
                buf.push(40);
                depth += 1;
                opened_here = true;
            }
            o += 1;
        }

        if opened_here {
            state = (state * 1103515245 + 12345) & 2147483647;
            if state % 4 == 0 { buf.push(45); }
        }

        state = (state * 1103515245 + 12345) & 2147483647;
        push_number(&mut buf, state % 1000);

        state = (state * 1103515245 + 12345) & 2147483647;
        let closes = state % 3;
        let mut c = 0i64;
        while c < closes {
            if depth > 0 {
                buf.push(41);
                depth -= 1;
            }
            c += 1;
        }
        t += 1;
    }
    while depth > 0 {
        buf.push(41);
        depth -= 1;
    }

    let n = buf.len() as i64;
    let mut sink = 0i64;
    for p in 0..passes {
        buf[0] = 48 + (p % 10);
        let r = calculate(&buf, n);
        sink = ((sink + r) % modulus + modulus) % modulus;
    }
    println!("{}", sink);
}
