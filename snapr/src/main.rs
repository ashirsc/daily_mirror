use std::thread;
use std::time::Duration;

use rppal::gpio::{Gpio, InputPin, OutputPin, Trigger};

fn blink(led: &mut OutputPin, num_intervals: i32, interval_duration: Duration) {
    
    for _ in 0..num_intervals - 1 {
        led.set_high();
        thread::sleep(interval_duration);
        led.set_low();
        thread::sleep(interval_duration);
    }
    led.set_high();
    thread::sleep(interval_duration);
    led.set_low();
}

fn main() {
    let gpio = Gpio::new().expect("Failed to initialize GPIO");
    let mut red_led = gpio.get(17).expect("Failed to get pin 17").into_output();
    red_led.set_low();
    let mut button: InputPin = gpio.get(2).expect("Failed to get pin 2").into_input();
    button.set_interrupt(Trigger::RisingEdge);

    let mut press_count: u32 = 0;
    println!("Staring loop");
    loop {
        button
            .poll_interrupt(false, None)
            .expect("Failed to poll button");
        press_count += 1;
        println!("Button pressed {} times", press_count);
        button.set_interrupt(Trigger::Disabled);
        blink(&mut red_led, 3, Duration::from_millis(500));
        button.set_interrupt(Trigger::RisingEdge);
    }
}
