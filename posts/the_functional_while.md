# The functional while 1 loop

## Invention of the century just short of Haskells forM_

Ok, this one is short and stupidly simple.
As some might know, I like to come up with Haskellish functional solutions for problems nobody had in Python.

### Today: How to get rid of the ```while``` loop

Say you want to download some data from an infamously inconsistent server.
Downloading, processing and storing the data is all done within one process called ```proc```.
However, you already know that 99% of the time, it will leave you with a timeout.
So you write a while loop which executes the request until it is successful.
It looks something like this:

~~~python
while 1:
    proc()
    if result_there():
        break
~~~

or maybe, if you're a little more tidy:

~~~python
while not success:
    success = proc()
~~~

or, if you're really lazy in writing code:

~~~python
while not proc():
    pass
~~~

But what if I tell you, you can win the local "who used the least lines of code"-competition with a simple trick?

<!--Say we are brave functional programming monks (Hughes, 1990) coming from the vast meadows of Haskell land
where eager computation needs a to be forced**!** *(Some might not get the joke)*-->

### But first: Some hatred for the while loop

...and an explanation why we don't even need a substitute for it.

Pure functional programming incorporates no side effects.
This means there is no variables, there is no mutable state, there is no I/O.
Since there is no mutable state, there is no ```for``` loops.
The whole concept of a ```for``` loop is to alter state in place.
(*Tipp:* Use Comprehensions and Generator-Expressions instead!)

But what about the more primitive ```while``` loop, doesn't it just evaluate a predicate?
Well yes, but what's the use case? To calculate the same result over and over again just for good measure?
See when you calculate a solution in FP, you've got **the** solution.
Since your function cannot depend on any external variables, you gotta change the input in order to change the result.
You want to go over a list of inputs and safe all results? Use a fabulous list-comprehension instead! (Or a generator expression)

### And now: Something just proven to be useless

How can we run a process over and over again until it succeeds without a ```while``` loop?
Just use a wise combination of ```any``` and ```count``` (or any other infinite expression really):

~~~python
any(proc() for _ in count())
~~~

Why does this work?
```any``` (and ```all```) are shortcutted.
This means, in order to save some computation time, they will stop iteratiing once they've:

+ ```any```: Come across the value ```True```
+ ```all```: Come across the value ```False```

Hence, there's also a very similar approach to subsitute a loop executing all processes until one fails:

~~~python
all(proc() for _ in count())
~~~

And probably there's many other applications one can come up with.
One important side note though: If you find yourself wondering why only half of your processes in your static blog software were ever executed - Maybe you've used an ```any``` to check if one process found something worth of updating and ```any``` shortcutted out of executing the rest ;)
