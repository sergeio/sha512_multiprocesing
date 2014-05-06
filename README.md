SHA512 Multiprocessing
======================


This is a result of my having read this writeup on the [minimum viable block
chain](http://www.igvita.com/2014/05/05/minimum-viable-block-chain/), and
wanting to play around with python's multiprocessing functionality.  For some
reason, I haven't had a good excuse to play with it before.

Results
-------

I learned that daemonized subprocesses cannot spawn child processes of their
own, and that threads in python block until they hit IO.


### Example ###

Let's time finding a hash with 5 leading zeroes using 1 and 2 processes:

```bash
$ time python sha512_zeroes.py 5 1
(5, 1839773, '00000a6e66e4f6b265dd66a431cad21e65d0af4f9a88f83838545248ae2eaf326327b357cdc856ad10e94070afb2e559c4b374667f5bdd58aa5b3bdeec27cf5f')
python sha512_zeroes.py 5 1  4.28s user 0.03s system 96% cpu 4.477 total

$ time python sha512_zeroes.py 5 2
(5, 1839773, '00000a6e66e4f6b265dd66a431cad21e65d0af4f9a88f83838545248ae2eaf326327b357cdc856ad10e94070afb2e559c4b374667f5bdd58aa5b3bdeec27cf5f')
python sha512_zeroes.py 5 2  4.57s user 0.02s system 179% cpu 2.549 total
```

Cool. 6 leading zeroes?

```bash
$ time python sha512_zeroes.py 6 1
(6, 6899310, '0000004c06b9bead1a5e584ec47e0f17af699189d39ad8788b7abe3ec0dc4c31ff13f06f4932af2d833e1e00e70593a0ca3ae2f2641450fe83a7227ed4890f71')
python sha512_zeroes.py 6 1  15.31s user 0.06s system 94% cpu 16.198 total
$ time python sha512_zeroes.py 6 2
(6, 6899310, '0000004c06b9bead1a5e584ec47e0f17af699189d39ad8788b7abe3ec0dc4c31ff13f06f4932af2d833e1e00e70593a0ca3ae2f2641450fe83a7227ed4890f71')
python sha512_zeroes.py 6 2  16.97s user 0.06s system 175% cpu 9.689 total
```

Pretty decent speedup. Let's try a machine with a few more cores:

```bash
$ time python sha512_zeroes.py 6 1
(6, 6899310, '0000004c06b9bead1a5e584ec47e0f17af699189d39ad8788b7abe3ec0dc4c31ff13f06f4932af2d833e1e00e70593a0ca3ae2f2641450fe83a7227ed4890f71')
python sha512_zeroes.py 6 1  20.44s user 0.03s system 95% cpu 21.469 total
$ time python sha512_zeroes.py 6 6
(6, 6899310, '0000004c06b9bead1a5e584ec47e0f17af699189d39ad8788b7abe3ec0dc4c31ff13f06f4932af2d833e1e00e70593a0ca3ae2f2641450fe83a7227ed4890f71')
python sha512_zeroes.py 6 6  22.88s user 0.13s system 338% cpu 6.791 total
```

**Cool!**
