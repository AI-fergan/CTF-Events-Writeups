# MiniMath
#### First assert - 'No numbers allowed.'
This challenge includes one Python script. When we run the script, it asks for an "equation." We can provide any equation we want, but it has one strict condition: the equation cannot contain any numbers! Here are some examples of valid equations:

```python
len("aaa")

len("aaa") * len("aaaaa")

pow(len("aa"), len("aaa")) 
```

* Note: Sometimes, the script may throw the exception Infinite loop detected. This exception is raised by the function `get_cycle` when it cannot find the number it is searching for. This function searches for a number such that the sum of the divisors of one of its divisors equals the sum of the divisors of the number itself.


#### Second assert - 'Not a sociable number.'
Second Assertion - "Not a sociable number."
This assertion occurs when the function `get_cycle` returns fewer than three numbers in the res list. To find a number that makes the function `get_cycle` return three or more numbers, we use brute force, iterating from 1 to 10,000,000.

* Note: The brute force script is in the Python file named `get_sociable_number.py`. 
The result of the brute force search can be found in a comment at the top of the script.

Congrats! Now we have a number that can pass all the tests in the challenge and proceed to the final condition.
Note: You can try this by creating a Python expression that generates the number `101916` without directly using numbers. The following script generates a Python expression that passes all challenge tests up to the final condition:

```python
print('len("%s")' % ("a" * 101916))
```

#### The final condition
This condition checks if the length of the Python line we provide is less than the value stored in a variable called shortest. This variable has the value `1000`, so we need to write a shorter Python line to pass the condition. To achieve this, we can use multiplication to create larger numbers using smaller strings, instead of relying on a single `len()` function. For example:

```python
# This line ret 25
#------------------
len("aaaaaaaaaaaaaaaaaaaaaaaaa")

# Use this
# This line ret 25
#-------------------
len("aaaaa")*len("aaaaa")
```
Now our line is shorter and simpler, to make it even shorter, we can use the `pow()` function:

```python
# This line ret 125
#------------------
len("aaaaa")*len("aaaaaaaaaaaaaaaaaaaaaaaaa")

# Use this
# This line ret 125
#-------------------
pow(len("aaaaa"),len("aaa"))
```

The `solve.py` script calculates the shortest possible Python line that produces the number `101916` and satisfies the challenge's final condition.