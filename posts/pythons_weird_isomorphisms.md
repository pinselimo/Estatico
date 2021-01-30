# Python's weird isomorphisms

## Why the hell is an uncalled method True in an if-clause?

So isomorphisms are a favourite among functional programmers. They allow us to convert types without losses. Strict type systems, common within functional languages, induce some restrictions on us that type conversions allow us to conveniently circumvent. Obviously, Python isn't so strict about types. However, duck typing is a common and somewhat similar concept to isomorphisms used in Python.

### Duck Typing and Isomorphisms

The idea of duck typing is based on a rather simple idea:

> If it walks like a duck and quacks like a duck - then it must be a duck!

Now isomorphisms work quite similarly, while also retaining the mathematical rigor we have come to expect from FP concepts. Two types ```A``` and ```B``` are isomorphisms of one another if there exist two functions ```f :: A -> B``` and ```g :: B -> A``` where ```x == f(g(x))``` and ```y == g(f(y))```.

In plain words: Two types are isomorphic if you can convert one to another and back without losing anything. It's that simple.

In principle the difference between duck typing and isomorphisms is that for the latter we have a proper definition with constraints, while for the prior we have an optimistic wish. Fascinatingly, in an idealistic context they work out to be pretty much the same.

### Pythons weirdness

Speaking of idealistic contexts - Python is not among those. Meanwhile, it is totally based on the concept of an ideal world where developers know all the unwritten (and unchecked) rules and abide.

A fun context to check isomorphisms in Python is when it comes to boolean values:

~~~python
print('Empty lists') if [] else print('No empty lists')
print('Values below zero' if -1 else print('No values below zero')
print('Zero?') if 0 else print('Zero is False')
~~~

ok those are common knowledge. Empty collections are False and Zero (```0```) is also False. Let's look at more stupid ones:

~~~python
print('Objects') if object() else print('No objects')
print('Lambdas') if (lambda x:x) else print('No lambdas')
~~~

Yes, pretty much everything else is considered ```True``` ! Ugh.

### How I realized

Readers will know by now: Every single one of my programming language rants has its background in some hours of fixing a stupid bug. And this is no exception!

This time I encountered a method which should return a boolean value, but was instead never called. Now in every proper (sorry Pythonistas) programming language this would just trigger a well deserved exception - not in Python. It's all happy assuming ```(lambda x:x)``` is ```True```.

And that last line actually serves an ugly solution. It's maybe the only solution:

~~~python
print('Lambda accepted') if ((lambda x:x) == True) else print('Lambda rejected')
~~~

That's right! Objects are considered ```True```, yet not **equal** to ```True```. Welcome to the weird isomorphisms of Python.

So should I stop telling my students that ```if predicate == True:``` is unnecessary explicit? I guess so...

### Nitpicking on the comparison

Of course it can be discussed if the line between duck typing and isomorphisms can be drawn in the way I did. If the object (as in "the ID") stays the same, we can use one of type ```A``` as if it had type ```B``` and vice versa. Without losing information. However, if we perform some form of type casting, this assumption breaks down. Nevertheless, I'd argue casting is a much less famous technique among Python programmers. Probably due to the weak typing.

It's no secret that I tend to prefer the more rigorous concepts FP provides. However, even I have to admit that duck typing is incredibly convenient when you want to [hack on the meta level](https://github.com/pinselimo/Pythas).

### One more thing

Lastly I want to point out, that we have indeed come a far way since the times of Python 2 on this! Back then, the following worked and it still causes me nightmares:

~~~python
>>> True = False
>>> False == True
True
~~~

Philosophically fascinating though!

