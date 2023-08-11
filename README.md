# HS Shift

This repository contains a typology calculator for Harmonic Serialism based on the Fusional Reduction algorithm (FRed) (Brasoveanu & Prince 2011). The component programs are:

*    con.py defines the constraints Align-R, NonFinality, *Link, *Float, Max(link), Dep(link), Max, and MaxLinked as Classes
*    fred.py provides a implementation of FRed
*    gen.py defines the candidate generation function, which can delete features, locally add or remove autosegmental links, and, if toggled, implement autosegmental shift as a single step operation
*    compare_typologies.py summarizes the differences between typologies
*    typologizer.py is the main module

To use this software, provide URs and CON to typologizer.py and run the script with Python 3. The results reported in the paper below are provided in the typologies/ folder.

Lamont, Andrew. to appear. Shift is derived. Journal of Linguistics. [https://www.dropbox.com/s/r3a1899zn260ri2/Shift%20is%20derived.pdf?dl=0](https://www.dropbox.com/s/r3a1899zn260ri2/Shift%20is%20derived.pdf?dl=0)
