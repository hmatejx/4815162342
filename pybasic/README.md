# Modified BASIC Interpreter

**Disclaimer: The BASIC interpreter included in this project is mostly not my work**. Specificaly, I cloned the code of [this commit](https://github.com/richpl/PyBasic/commit/45207e8b5b5ed689b2f487794cbb5ff1ab12320e).

This version is a heavily modified/customized version of [the PyBasic interpreter](https://github.com/richpl/PyBasic) by [@richpl](https://github.com/richpl). The relevant modifications are listed in the next section.

The documentation of the core BASIC dialect can be found at the [original source](https://github.com/richpl/PyBasic/blob/4742271bc17ae16bf38ec911e2c69cb69bd9dbf4/README.md). 

## Modifications to the original interpreter

I inserted the respective hooks into all I/O calls, e.g. print, input, getch, etc. so that the interpreter can interact with a computer simulator, such as the Appple II simulator implemented in this project. I have also slightly refactored the code to enable the necessary interfacing.

In addition, I enriched the BASIC dialect with serveral additional BASIC statements.

### Playing sound files

```
> REM SND fname, volume (float)
> 10 SND "DHARMA/DHARMA.MP3", 1
```

### Loading image files

```
> REM IMG fname, x, y, scale (float; optional), speed (float; optional)
> 10 IMG "DHARMA/SWANLOGO.PNG", 228, 36, 3, 3
```

### Move cursor to a horizontal / vertical position

Note that these functions allow floating-point positioning...

```
> REM HTAB X (float)
> REM VTAB Y (float)
> 10 HTAB 12 : VTAB 20
```

### Pause

```
> REM PAUSE time (in milliseconds)
> 10 PAUSE 1000
```

### Clear screen

```
> 10 CLRSCR
```

## Testing of functionality

The repository contains a test BASIC file `REGRESSION.BAS` that can be loaded and executed to test the functionality. The expected output is provided below.

```
λ python -m pybasic.interpreter
]load "PROG/REGRESSION.BAS"
Program read from file
]run
*** Testing basic arithmetic functions ***
Expecting the sum to be 300:
300
Expecting the product to be 20000:
20000
Expecting the sum to be 20100:
20100
Expecting sum to be 40000
40000
Should print the larger value of J which is 200
200
*** Testing subroutine behaviour ***
Calling subroutine
Executing the subroutine
Exited subroutine
Now testing nested subroutines
This should be printed first
This should be printed second
*** Testing loops ***
This loop should count to 5 in increments of 1:
1
2
3
4
5
This loop should count back from 10 to 1 in decrements of 2:
10
8
6
4
2
These nested loops should print 11, 12, 13, 21, 22, 23:
11
12
13
21
22
23
*** Testing arrays ***
This should print 555
555
*** Finished ***
```

## License

PyBasic is made available under the GNU General Public License, version 3.0 or later (GPL-3.0-or-later).

The same holds for this derivative work.
