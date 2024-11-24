# Network Ready Python

The NRP code is like instruction along with code for the compiler to run.

## Specifying Remote Machines

This part of NRP code should come first in whole NRP code and start and end with " *** "

for example :-
```
***
# these are remote flask hosts where the distributed code should run
"http://someip:port/",
"http://localhost:5000/",
"http://10.24.36.2:3000/",
***
```

## Req file for environment

After specifying hosts we specify path of requirments.txt file for environment setup at remote machines.
This part should come after remote machine config block i.e after a " *** " .

It must start with " >>> " and end with " >>> "
```
>>>
#this will be the path to requirments.txt file give full path not relative
/home/avinash/development/someproject/req.txt
>>>
```

## Imports

After specifying requirments file for environment we need to give imports block, this block should contain all the import statements both for sequential and parallel blocks at one place.

It must start with " ^^^ " and end with " ^^^ " , must be only after a " >>> ".

```
>>>
#this will be all the import used in all seq and par blocks
import collections
import numpy
import random
import custommodule
>>>
```

## Sequential and Parallel blocks

After the imports , we code the seq and par blocks.

- Always a seq block comes first before par block.
- No two blocks can be of same type.
- The code can end with seq or parallel block but must start with a seq block

A seq block starts and ends with " - - - "
A parallel block starts and ends with " ||| "

So, the compiler executes seq block at main machine and send the parallel block to all the remote machines to execute.

```
---
# this is a sequential code
??b=2
$$a=np.array([x*??b for x in range(100000)])
---

|||
# this is a parallel code
$$a=np.array([x*??b for x in $$a])
??b=??b*2
|||

```

## Special NRP Variables

You can use as normal variables like in python with rules of python variable naming.
But,

### $$variable_name :- 
- This is the variable which will be split across the remote machines to execute parallel operation on this variable.
- There can be multiple variables of this type
- After $$ part the variable_name must follow python conventions
- This must be a List,Numpy array or Pandas dataframe only ( other distributable types comming soon)

### ??variable_name :-
- This is the variable used to pass information between blocks, this will not be distributed among remote machines but will be sent to all remote machine with same value as in previous block.
- There can be multiple variables of this type
- After ?? part the variable_name must follow python conventions
- This can be anything which python supports and must be serializable by pickle.

### Normal python variables :-
- These will have same scope as python gives but only inside one block
- These variables cannot be accessed in other blocks ( use ?? variables for that )

## Looping 

This tool was made keeping in mind Machine Learning and it needs looping the training process.

we can loop any pair of sequential and parallel blocks and the no of times the blocks to be looped must specified after the block tokens

for example :- 

```
---3
#some seq code
---

# can include multiple blocks in between

|||
#some par code
|||3

```

The no of times the loop runs must be specified in first and last block,but

1. The first block must be sequential block
2. The last block must be parallel block

This looping feature also supports recursional looping,that means there can be loops inside loops .

for example :- 

```
---3
#some seq code
---

|||
# par code 2
|||

---2
# seq code 2
---

|||
# par code 3
|||2

---
# seq code 3
---

|||
#some par code
|||3

```

So , in this example the seq code 2 and par code 3 will be run 6 times total, that is everytime outer loop run the inner loop runs for 2 times .

## Example NRP txt file

```
***
# these are host on which servernodes are running
"http://localhost:3000/",
"http://localhost:5000/",
"http://localhost:4000/",
***

>>>
#this will be the path to the requirments.txt file 
/home/avinash/development/ReddyNet_V2.0/reqfake.txt
>>>

^^^
# this will be import statements
import collections
import math
import random
import fastapi
import numpy as np
^^^

---
# this is a sequential code
??b=2                        #value of ??b will be 2 and will be passed to next block
$$a=np.array([x*??b for x in range(100000)])
---

|||
# this is a parallel code
$$a=np.array([x*??b for x in $$a])
??b=??b*2                        #value of ??b will be 4
|||

---3                             # this will runt the blocks 3 times
# this is a sequential code
$$a=np.array([x*??b for x in $$a])
??b=??b*2                        #value of ??b will be 8
---

|||
# this is a parallel code
$$a=np.array([x*??b for x in $$a])
|||3

---
# this is a sequential code
print($$a[:10])
print("done")
---
```

This is example showing distributed big array multiplication, althoug a single machine can easily handle this but as the array grows bigger NRP could solve the compute problem with distributed multiplcation on remote machines.

This same idea can be used for distributing other things like Ml models or Dataset processing over different remote machine, although there might be network overhead and serialization problems.

This is an example NRP file for training a model distributed on 3 machines :- [ML example](Examples/ml_example.txt)









