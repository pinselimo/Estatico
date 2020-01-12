# Revealing race conditions through provocation

## Learning through frustration

Sometimes race conditions are so rare, you never encounter them during the test phase.
We tend to agree that users should not experience them either.
Unfortunately, there are just too many of them out there!

### A multithreaded problem

I am running an algorithm on the GPU which itself already works threaded.
In my case, for the singular problem some 9000 threads are incorporated.
In blocks of 128 I believe, but this doesn't matter.
For itself, the algorithm works perfectly.
The only problem is that I need to solve this algorithm some 4000 times. Quick.
Clearly the solution is to run not 9000 threads, but 9000 times 4000 threads.

If we just separate the data and threads wisely, this can be well organised.
To our all great relief, nVidia built multi-dimensional thread and block indexing into CUDA.
But what is even more, they provided us with 2-dimensional arrays.
So indexing and data organisation are definitely not a big issue!

### Running into an issue nevertheless

This is where I've found myself having a hard time wrapping my head around the following phenomenon:

Running the (singular) algorithm on the GPU skipping each block with the wrong Y-index seemed to run without any errors.
However, running all blocks in parallel without any memory overlap, caused some.
These were well defined, but seemed to happen in arbitrary places.
Well defined in this case means the following: For a subset of the results, all of them would have the same error.

![Example for the constant error](images/cuda_constant_error.png)

At first I thought the cause for this problem was some oversight of remaining memory overlap for blocks on the y-axis.
However, even after close inspection (i.e. some frustrating time staring at my screen) I couldn't seem to find the issue.

### The reason, a solution

> I had discovered rare race conditions. The other blocks just served as provocation handle!

As can be read in the [CUDA C Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#thread-hierarchy) the execution order of thread blocks is not defined.
By adding additional blocks even if they are defined on a separate axis, the order of block execution is altered.
The kernel will take a longer time to execute, which also streches out the possibility of blocks being executed 'too late'.

In practice, this finding can be turned into a quite useful method.
Any typical pitfall of multithreaded programming can be forced through provocation.
Probably, this is already good practice somewhere, otherwise I propose it here!
