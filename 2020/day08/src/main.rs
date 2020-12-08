use std::fs::File;
use std::io::{self, BufRead, Error};

mod machine;

type AOCResult = std::result::Result<(), Error>;

struct AOCProcessor {
    input: String,
    machine: machine::AOCMachine,
}

impl AOCProcessor {
    pub fn new(input: String) -> AOCProcessor {
        AOCProcessor {
            input,
            machine: machine::AOCMachine::new(),
        }
    }

    pub fn process(&mut self) -> AOCResult {
        let file = match File::open(&self.input) {
            Ok(file) => file,
            Err(error) => return Err(error),
        };

        self.initialize();
        for line in io::BufReader::new(file).lines() {
            if let Ok(line) = line {
                self.process_line(&line[..]);
            }
        }
        self.finalize();

        Ok(())
    }

    pub fn initialize(&mut self) {
        self.machine.reboot();
    }

    fn process_line(&mut self, line: &str) {
        if line.len() > 0 {
            let tokens: Vec<&str> = line.split_ascii_whitespace().collect();
            if tokens.len() == 2 {
                let operation = tokens[0];
                let argument = tokens[1];
                match self
                    .machine
                    .load_instruction(operation, argument.parse::<i32>().unwrap())
                {
                    Err(error) => {
                        panic!("{}", error);
                    }
                    _ => {}
                }
            }
        }
    }

    pub fn finalize(&mut self) {
        self.finalize_a();
        self.finalize_b();
    }

    fn finalize_a(&mut self) {
        let mut machine = self.machine.clone();
        if machine.run() {}
        println!("finalize_a: accumulator:{}", machine.get_accumulator());
    }

    fn finalize_b(&mut self) {
        let mut original_machine = self.machine.clone();
        original_machine.reset();

        let mut found_bug = false;
        let mut found_accumulator = 0;
        if !found_bug {
            for idx in 0..original_machine.nop_v.len() {
                let mut machine = original_machine.clone();
                machine.reset();
                machine.set_machine_operation(
                    *machine.nop_v.get(idx).unwrap(),
                    machine::AOCMachineOperation::JMP,
                );
                if machine.run() {
                    found_bug = true;
                    found_accumulator = machine.get_accumulator();
                    break;
                }
            }
        }
        if !found_bug {
            for idx in 0..original_machine.jmp_v.len() {
                let mut machine = original_machine.clone();
                machine.reset();
                machine.set_machine_operation(
                    *machine.jmp_v.get(idx).unwrap(),
                    machine::AOCMachineOperation::NOP,
                );
                if machine.run() {
                    found_bug = true;
                    found_accumulator = machine.get_accumulator();
                    break;
                }
            }
        }
        if found_bug {
            println!("finalize_b: accumulator:{}", found_accumulator);
        }
    }
}

fn main() {
    let mut p = AOCProcessor::new(String::from("input.txt"));

    match p.process() {
        Ok(()) => {
            println!("DONE");
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
