# Python's referential transparency

## Part 1 - A rant

Python's Generator functions and expressions introduced lazy evaluation syntax into an previously mostly eagerly evaluated ecosystem. Laziness was first introduced in functional programming languages and that's for a reason. To assure a function can be evaluated at any time, yet yield the same result requires referential transparency.

This poses the question: Is there any thing close to referential transparency in Python?
There's not even constants, so an easy shot is to just answer: Nope.

Let's look at an example for that. We'll define a pair of functions. One named ```f``` is a normal Python function; ```g``` however is a generator function, the lazy equivalent of a normal Python function:

~~~python
>>> def f(x):
...     return x*x
...
>>> def g(xs):
...     for x in xs:
...         yield f(x)
...
~~~

Let's call ```g``` and see what happens. Since it is lazy we can easily call it on an infinite structure. Calling it like that also proofs its laziness once and for all.

~~~python
>>> from itertools import count
>>> gen = g(count())
>>> [next(gen) for _ in range(10)]
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
~~~

Defining ```gen``` does not blow up our computer, so we are indeed not evaluating eagerly. But what happens once we change ```f``` to be the identity function?

~~~python
>>> f = lambda x: x
>>> next(gen)
10
~~~

## Now that sucks

There's no referential transparency. Or is there?
Well it comes down to conventionalism. That's the charm of Python I guess.
Let's change our interpretation of a generator function from being the lazy equivalent of a usual function to being the constructor of such an equivalent.

As the Zen of Python teaches us:
> Namespaces are one honking great idea -- let's do more of those!

Let's redefine ```g``` to create a generator in an confined namespace:

~~~python
>>> def g(f,xs):
     yield from (f(x) for x in xs)
~~~

For convenience the for-loop expression was substituted with a generator expression. The important difference is the introduction of an inner scoped function ```f```. Let's see such a generator in action:

~~~python
>>> gen = g(f,count())
>>> [next(gen) for _ in range(10)]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>>f = lambda x: x+x
>>>next(gen)
10
~~~

Where has the function ```f``` gone to though? *Has it amazingly become the first constant ever to be seen in Python?*

### Of course not

The variable state is just localized (good) and harder to access (really not that good):

~~~python
>>> gen.gi_frame.f_locals
{'xs': count(10), 'f': <function <lambda> at 0x7f82bb3b7710>}
~~~

Here we can also explore a dirty trick Python plays on us to keep us believing in laziness within its realm. The for loop over count has somehow transcended into the count function.
Still as long as we keep ourselves and our users from touching gen's internal state, we can guarante referential transparency now.

**Python is weird.**
