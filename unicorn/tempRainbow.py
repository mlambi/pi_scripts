import colorsys
import unicornhat as uh

uh.set_layout(uh.PHAT)
uh.brightness(0.5)


for x in range(8):
    # setting the value of temp = x will give a numric range of 0-7
    # this is a good range for us to explore the output of C temps
    # which will typically be between 0-37 (rounding to 40)
    # if we were reading a thermometer we would *2 the reading
    temp = (x * 10)
    print(f"Temp = {temp}")

    # the problem is that the color wheel is inverse
    # to the temperature gradient.  i.e. 70 is blue and 0 is red
    # subtracting from 100 should give us the inverse
    # h = 100 - temp
    # not working???
    h = temp
    print(f"h = {h}")

    # the hue value passed to colorsys has to be between 0-1
    # divide by 100 to get a decimal
    hue = h / 100
    print(f"Hue = {hue}")

    # rgb values for unicornhat need to be in the range of 0-255
    # the next line will generate and normalize the values
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
    print(f"R = {r}, G = {g}, B = {b}")

    # finally, we run through the y range and set each x (row)
    # to the generated value for each column (y)
    for y in range(4):
        uh.set_pixel(x, y, r, g, b)

uh.show()

# this is a cheap way to get the program to pause
# i need to learn something better, CTL-c to exit
input()
