# TerraTec Connect N3 Hack Part 3

## Looking at traffic; finding solutions

After getting root access to the Connect N3 device and looking into all of its hard- and software, there seemed nothing broken on the device itself other than the crappy implementation of NetUSB. Now that we know enough about the device, let’s look at the driver and what’s happening on the local network.

### Sitting around looking at traffic

I installed the driver for the Connect N3 on a virtual Windows 7 machine, and looked at what was happening on the network while the "CONNECT N3.exe" was looking for a device to pair.

Although it sent UDP packets to the broadcast about every second, no response was sent by the device (also not after repeating the messages on my local network with the N3 being accessible via http).  
After I had sent the UDP packet to the device itself, I received a response, which I repeated back to the driver again. The driver’s response to my simulated device were some TCP packets to which my implementation remained quiet.

Looking at the ifconfig of the device I realised, that the MASK variable was set to 255.0.0.0 instead of the actual value 255.255.255.0 Yet changing it yielded no improvements.

When I tried installing the driver on a separate Windows 10 machine, unfortunately I could not see any UDP packages of the driver being sent to the broadcast, so the problem was likely to be compatibility with the newest version of Windows. Given the implementation of this program, security issues with it and poor update policy of TerraTec I wouldn’t have wondered much about issues like that.

### Just never settle for poor results

After I had messed around a lot with compatibility mode and running stuff as admin in Windows and had finally come to the conclusion, that i might have to reverse engineer the driver or just solder an USB connector to the traces giving me at least the DVB-S stick part of the device, off which i could stream into the network via a Raspberry PI, I finally made up my mind thinking:

> "I ought also just have a look at good ol’ Task Manager."

And guess what, "CONNECT N3.exe" was shown to have 0.1 Mb network traffic about every second, quite in the same frequency as it was sending UDP packets in my Windows 7 VM, they just never reached the network!  
For a quick test, I enabled the mobile hotspot on my Smartphone, connected two machines to it and as I started the driver on the Windows one, i could see the UDP packets fly through the network on the other, brilliant!

So what prevents the driver from sending UDP packets into my network? What is the big difference between the LAN and the VirtualBox's or the Smartphone's network?

> It’s the IP space!

While on most local networks the DHCP server hands out IPs on the 192.168.1.x range in this specific one it was using the second local IP space 10.0.0.x. Likely terratecs software developers hadn’t taken that into account and therefore the driver will only discover devices when residing on a 192… IP!

### Finding solutions

Of course changing the IP space in the router’s configuration solved all my problems, the little python script I had written earlier immediately received the UDP packets and verified them and soon afterwards the device was found.  
But what if the netmask and therefore broadcast address on the device would’ve stayed wrong initially, for some problems all the work I’ve done might be helpful anyway, so I blogged about it.
