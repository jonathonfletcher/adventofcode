use std::fs::File;
use std::io::{self, BufRead, Error};

const AOCDEBUG: bool = false;

type AOCResult = std::result::Result<(), Error>;

struct AOCProcessor {
    input: String,
    ts: i64,
    busses: Vec<i64>,
    valid_busses: Vec<bool>,
    result_a: i64,
    result_b: i64,
}

impl AOCProcessor {
    pub fn new(input: String) -> AOCProcessor {
        AOCProcessor {
            input,
            ts: 0,
            busses: Vec::new(),
            valid_busses: Vec::new(),
            result_a: 0,
            result_b: 0,
        }
    }

    pub fn process(&mut self) -> AOCResult {
        self.initialize();

        let _ = match File::open(&self.input) {
            Ok(file) => {
                for line in io::BufReader::new(file).lines() {
                    if let Ok(line) = line {
                        self.process_line(&line[..]);
                    }
                }
            }
            Err(error) => return Err(error),
        };

        self.finalize();

        Ok(())
    }

    pub fn initialize(&mut self) {}

    pub fn finalize(&mut self) {
        if AOCDEBUG {
            println!("{}", self.ts);
            println!("{:?}", self.busses);
            println!("{:?}", self.valid_busses);
        }
        self.finalize_a();
        self.finalize_b();
    }

    fn process_line(&mut self, line: &str) {
        if line.len() > 0 {
            if self.ts == 0 {
                self.ts = line.parse::<i64>().unwrap();
            } else {
                for id in line.split(',') {
                    if id.ne("x") {
                        self.valid_busses.push(true);
                        self.busses.push(id.parse::<i64>().unwrap());
                    } else {
                        self.valid_busses.push(false);
                        self.busses.push(0);
                    }
                }
            }
        }
    }

    fn finalize_a(&mut self) {
        let max_id: i64 = self.busses.iter().map(|x| *x).max().unwrap() as i64;
        let mut departure_ts: i64 = self.ts;
        let mut departure_id: i64 = 0;
        for ts in self.ts..(self.ts + max_id) {
            let mut row: Vec<char> = Vec::new();
            for idx in 0..self.busses.len() {
                if self.valid_busses[idx] {
                    let id = self.busses[idx];
                    if ts % id == 0 {
                        row.push('D');
                        if ts > self.ts {
                            departure_ts = ts;
                            departure_id = id;
                        }
                    } else {
                        row.push('.');
                    }
                }
            }
            if AOCDEBUG {
                println!("{} {:?}", ts, row);
            }
            if departure_id > 0 {
                break;
            }
        }
        if AOCDEBUG {
            println!(
                "{} - {} -> {}, {} -> {}",
                departure_ts,
                self.ts,
                departure_ts - self.ts,
                departure_id,
                departure_id * (departure_ts - self.ts)
            );
        }
        self.result_a = departure_id * (departure_ts - self.ts);
        println!("result_a:{}", self.result_a);
    }

    /*
        17,x,13,19 is 3417
        [0, 17], [2, 13], [3, 19]

        (ts + 0) % 17 == 0
        (ts + 2) % 13 == 0 && (ts + 0) % 17 == 0
        (ts + 3) % 19 == 0 && (ts + 0) % 17 == 0 && (ts + 2) % 13 == 0

        while (ts + 0) % 17 > 0 {
            ts += 1;
        }
        while (ts + 2) % 13 > 0 {
            ts += 1 * 17;
        }
        while (ts + 3) % 19 > 0 {
            ts += 1 * 17 * 13;
        }
    */

    fn finalize_b(&mut self) {
        let mut min_ts: i64 = 0;
        let mut ts_step: i64 = 1;
        for idx in 0..self.busses.len() {
            if self.valid_busses[idx] {
                let id = self.busses[idx];
                while (min_ts + idx as i64) % id > 0 {
                    min_ts += ts_step;
                }
                if AOCDEBUG {
                    println!(
                        "(ts:{} + offset:{}) % id:{} == 0 (step:{})",
                        min_ts, idx as i64, id, ts_step
                    );
                }
                ts_step *= id;
            }
        }
        self.result_b = min_ts;
        println!("result_b:{}", self.result_b);
    }
}

fn main() {
    let mut processor = AOCProcessor::new(String::from("input.txt"));
    match processor.process() {
        Ok(()) => {
            println!("DONE");
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
