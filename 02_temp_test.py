from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

temp = sense.get_temperature()
sense.show_message('Temp: {0:0.1f} *c'.format(temp), scroll_speed=0.05)
sense.clear()
