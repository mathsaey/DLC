# About 

This is the repository for the project of the Compilers course of Mathijs Saey at the Vrije Universiteit Brussel. The goal of this project is to create a compiler. Specifically, we create a compiler that transforms DL, a novel dataflow language, into [DIS](http://mathsaey.github.io/DVM/md_doc__d_i_s.html), the low-level dataflow language of [DVM](https://github.com/mathsaey/DVM), the virtual machine of our masters thesis.

# DL

DL, or Dataflow Language, is a toy language designed for the exploration of compiler implementations. The language is still under development, and will likely change during the development of this compiler, but an early sample can already be found below.

    func fac(n)
    	if n > 0
    		then return n * main(n - 1)
    		else return 1
    
    func main(n)
    	let
    		fac     := fac(n) ;
    		other  := (33 + 3) - 35
    	in 
    		return fac * other    