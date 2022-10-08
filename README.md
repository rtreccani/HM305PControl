# PSUMan to the rescue!
## why?
I acquired a Hanmatek HM305P as an early birthday present, and whilst I can't fault the power delivery and functionality of it (for what it costs at least), the software leaves *a lot* to be desired.

Here's a screencap from the original software

![screencap of ugly software](https://cdn.discordapp.com/attachments/399691384652562434/716690129799872582/unknown.png)

This graphic design is unimpressive to say the least, and to boot, it didn't actually work. No matter how many times and different configurations I tried, I couldn't connect to it. It kept telling me "It is detected that the device is not have electric, the device cannot sample the data, please open the power and then excute the operation"

So I did some digging and discovered it uses a standard known as Modbus RTU over serial. The connection chugs along at 9600 baud. 

Luckily there's already a python module known as pymodbus that contains all you need to talk to devices. Within a matter of 10 minutes I could control the power button, and shortly afterwards, I have now the following features:
* set and get the master power switch status, as well as toggle
* set and get the voltage setpoint, and get the real voltage
* set and get the current setpoint, and get the real current

Currently the UI looks like this

![screencap of slightly less ugly software](https://media.discordapp.net/attachments/399691384652562434/787681840826810408/unknown.png)

I'd love to make it more visually appealing, but my QT knowledge is minimal. I'm working on adding a graph of voltage and current.
Watch this space if you have this PSU


If you want to control it remotely, see PSUManControlServer.py

Note: I found further related information at:
http://nightflyerfireworks.com/home/fun-with-cheap-programable-power-supplies
https://www.eevblog.com/forum/testgear/power-supply-ripe-for-the-picking/