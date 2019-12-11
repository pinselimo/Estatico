# TerraTec Connect N3 Hack Part 2

## Opening doors, exploring the jungle
Having my UART stick connected to my computer I started screen to try out different bitrates, ending up at 115.200 bit/s which finally had me seeing meaningful ASCII on my screen and entering my home field: the software.

![Boot screen](images/conn_2.jpg)

### Opening doors and finding keys aka the interesting part

The first output booting up we got was U-Boot booting up the linux based OS on, as i guessed, an Atheros chip. The exact model is strangely sometimes called a AR7241 (Virian) and sometimes its predecessor the AR7240 (Python).  
Luckily a one second windows to interrupt the booting process is offered to us:

~~~uboot
PB93 (ar7241 - Virian) U-boot
DRAM:
sri
ar7240_ddr_initial_config(133): virian ddr1 init
____________________________________________________

Hit any key to stop autoboot:  1  0
## Booting image at 9f300000 ...
   Image Name:   Linux Kernel Image
   Created:      2011-06-14  10:12:25 UTC
   Image Type:   MIPS Linux Kernel Image (lzma compressed)
   Data Size:    783960 Bytes = 765.6 kB
   Load Address: 80002000
   Entry Point:  80211000
   Verifying Checksum ... OK
   Uncompressing Kernel Image ... OK
No initrd
## Transferring control to Linux (at address 80211000) ...
## Giving linux memsize in bytes, 16777216

Starting kernel ...

Booting AR7240(Python)…
~~~

So I did, and ended up in the U-Boot boot manager. I looked at the environment variables set at boot time and changed them.

Boot variables:

~~~bash
arg 4: init=/sbin/init
arg 6: virian # still strange thing going on with the processor generation
~~~

Changing the boot variables to: ```arg 4: init=/sbin/sh```  
had the kernel panic, so i tried:  ```arg 4: init=/bin/sh```

Et voilá we boot into the shell as root user:

![Root](images/conn_4.jpg)

Unfortunately we also end up having a read only file system, so no password change via passwd but we can inspect the /etc/passwd and ```/etc/shadow``` file:

![Passwd](images/conn_15.jpg)

As we can see, there are some users w/o password and the root and Admin user share root privileges and the same hash. As with many of these devices, googling the hash reveals the password behind it way too easy. So now we can boot up the device normally, using the init process and login as root having a r/w file system.

### Exploring the jungle, looking for holes and bugs

The first question i faced was, which gen's processor this thing runs under the hood, hidden away under the shield:

~~~bash
system type             : Atheros AR7240 (Python)

#looks as if we’re running the old version

processor               : 0

cpu model               : MIPS 24K V7.4
~~~

Let’s look at the processes running after startup, ps spits out:

~~~bash
217 root        124 S   /usr/sbin/telnetd
220 root         56 D   /bin/factoryreset /dev/freset
221 root        392 S   my_httpd
222 root        288 S   netusb_wd CONNECT N3
228 root        328 S   netusb br0 CONNECT
231 root        276 S   awdp br0 CONNECT
229 root            SW  [thread_func_ex]
240 root        184 S   /sbin/getty ttyS0 115200
245 root        184 S   udhcpc -b -i br0 -s /etc/udhcpc.script
285 root        372 S   -sh
314 root        188 R   ps
~~~

Interesting to us are netusb and awdp, the last one of which i still don’t know anything about, but netusb rings the alarm bells in every security enthusiast’s mind, as there was a hole discovered in the software mid 2015 caused by a buffer overflow.

NetUSB is a service, nomen est omen, providing USB over the local network. So it seems likely that it mirrors the USB DVB-S stick coming from the Cypress controller in the LAN, the driver on the client’s Windows machine then acts as an interface between a virtual USB device and the netusb device in the network.

In the next post we’ll look into what’s happening on the network!
