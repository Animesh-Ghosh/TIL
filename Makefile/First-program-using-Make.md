# First program using Make.

I created my very first program using a Makefile.

It's really basic but it's a start. Goes something like this:

```make
"Makefile example": Complex.o
	g++ main.cpp Complex.o -o "Makefile example"

Complex.o: Complex.cpp
	g++ Complex.cpp -c
```

A good resource which I found was [this](https://www.youtube.com/playlist?list=PLNmACol6lYY7Dzvg7jKgvMdDaDEDFnNqD) playlist which helped a lot.

Plan on learning more from [GNU make](https://www.gnu.org/software/make/manual/make.html)
