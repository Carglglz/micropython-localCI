from machine import I2C, SoftI2C

i2c = I2C("X", freq=400000)  # create hardware I2c object

print("I2C(HW): ", i2c.scan())
i2cs = SoftI2C(scl="X1", sda="X2", freq=400000)  # create software I2C object

print("I2C(SW): ", i2cs.scan())
