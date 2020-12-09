use std::fs::File;
use std::io::{self, BufRead, Error};

const AOCDEBUG: bool = false;

type AOCResult = std::result::Result<(), Error>;

struct AOCProcessor {
    input: String,
    lookback: usize,
    lookback_vec: Vec<i64>,
    lookback_sum_vec: Vec<i64>,
    result_a: i64,
    result_b: i64,
}

impl AOCProcessor {
    pub fn new(input: String) -> AOCProcessor {
        AOCProcessor {
            input,
            lookback: 25,
            lookback_vec: Vec::new(),
            lookback_sum_vec: Vec::new(),
            result_a: 0,
            result_b: 0,
        }
    }

    pub fn process(&mut self) -> AOCResult {
        self.initialize();

        let file = match File::open(&self.input) {
            Ok(file) => file,
            Err(error) => return Err(error),
        };

        for line in io::BufReader::new(file).lines() {
            if let Ok(line) = line {
                self.process_line_a(&line[..]);
            }
        }

        if self.result_a > 0 {
            let file = match File::open(&self.input) {
                Ok(file) => file,
                Err(error) => return Err(error),
            };

            for line in io::BufReader::new(file).lines() {
                if let Ok(line) = line {
                    self.process_line_b(&line[..]);
                }
            }
        }

        self.finalize();

        Ok(())
    }

    pub fn initialize(&mut self) {
        self.lookback_vec.clear();
    }

    fn process_line_a(&mut self, line: &str) {
        fn n_is_valid(n: i64, v: &Vec<i64>) -> bool {
            for i in 0..(v.len()) {
                for j in (i + 1)..(v.len()) {
                    if n == v.get(i).unwrap() + v.get(j).unwrap() {
                        return true;
                    }
                }
            }

            false
        }

        if self.result_a == 0 && line.len() > 0 {
            let n = line.parse::<usize>().unwrap() as i64;
            if self.lookback_vec.len() >= self.lookback {
                while self.lookback_vec.len() > self.lookback {
                    self.lookback_vec = self.lookback_vec.drain(1..).collect();
                }
                let is_valid = n_is_valid(n, &self.lookback_vec);
                if AOCDEBUG {
                    println!("lookback_vec: {:?}", self.lookback_vec);
                    println!("n:{} -> {}", n, is_valid);
                }
                if !is_valid && self.result_a == 0 {
                    self.result_a = n;
                }
            }
            self.lookback_vec.push(n);
        }
    }

    fn process_line_b(&mut self, line: &str) {
        if self.result_a > 0 && self.result_b == 0 && line.len() > 0 {
            let n = line.parse::<usize>().unwrap() as i64;
            self.lookback_sum_vec.push(n);

            let mut sum_found = false;
            while self.lookback_sum_vec.len() > 0 {
                let l_s: i64 = self.lookback_sum_vec.iter().sum();
                if l_s < self.result_a {
                    break;
                } else if l_s == self.result_a {
                    sum_found = true;
                    break;
                }
                self.lookback_sum_vec = self.lookback_sum_vec.drain(1..).collect();
            }
            if sum_found {
                let sum_min: i64 = self.lookback_sum_vec.iter().map(|x| *x).min().unwrap();
                let sum_max: i64 = self.lookback_sum_vec.iter().map(|x| *x).max().unwrap();
                self.result_b = sum_min + sum_max;
                if AOCDEBUG {
                    println!("lookback_sum_vec: {:?}", self.lookback_sum_vec);
                    println!("sum:{}", self.result_a);
                    println!("min:{}, max:{}", sum_min, sum_max);
                    println!("result_b:{}", self.result_b);
                }
            }
        }
    }

    pub fn finalize(&mut self) {
        self.finalize_a();
        self.finalize_b();
    }

    fn finalize_a(&mut self) {
        println!("result_a: {}", self.result_a);
        println!("result_b: {}", self.result_b);
    }

    fn finalize_b(&mut self) {}
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
