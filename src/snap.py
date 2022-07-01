from gpiozero import Button, LED
from picamera import PiCamera
from time import sleep
from datetime import datetime

TIME_INTERVAL = .75


camera = PiCamera()

led = LED(17)
button = Button(2)

while True:
    button.wait_for_press()

    camera.rotation = 180
    camera.start_preview()


    for i in range(2):
        led.on()
        sleep(TIME_INTERVAL)
        led.off()
        sleep(TIME_INTERVAL)

    led.on()
    sleep(TIME_INTERVAL)
    led.off()
    now = datetime.now()
    fileName = 'data/captures/{}.jpg'.format(now.strftime("%m-%d-%yT%H-%M-%S"))
    camera.capture(fileName)
    camera.stop_preview()

    print("snapped")
