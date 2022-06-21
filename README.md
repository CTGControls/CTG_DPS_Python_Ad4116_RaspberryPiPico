# Example code showing the python SPI read from the Analog Devices AD4116 Evaluation Board problem 

The hardware I am testing with:
1. [Raspberry Pi Pico RP2040 PRODUCT ID: 4883](https://www.adafruit.com/product/4883)
2. [Analog Devices AD4116 Evaluation Board ](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/EVAL-AD4116.html)


### Some reads from AD4116 showing all are good read:
```diff
+ get_register: got [ 0x80 0x00 0x55 ] from reg [ 0x30 ] using command [ 0x70  ]
+ get_register: got [ 0x80 0x00 0x55 ] from reg [ 0x30 ] using command [ 0x70  ]
+ get_register: got [ 0x80 0x00 0x55 ] from reg [ 0x30 ] using command [ 0x70  ]
+ get_register: got [ 0x80 0x00 0x55 ] from reg [ 0x30 ] using command [ 0x70  ]
+ get_register: got [ 0x80 0x00 0x55 ] from reg [ 0x30 ] using command [ 0x70  ]
+ get_register: got [ 0x80 0x00 0x55 ] from reg [ 0x30 ] using command [ 0x70  ]
+ get_register: got [ 0x80 0x00 0x55 ] from reg [ 0x30 ] using command [ 0x70  ]
```

### Siglent SDS 1104x-e Digital Storage Oscilloscope showing the the correct data a commad 0x70 and a read of 0x800055 
![SPI Message](/../main/res/SDS00002.jpg)
