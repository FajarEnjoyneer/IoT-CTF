target remote :1234
set architecture arm
# Find address of "Input flag:" string
# 0x13571 was our estimate
# Break on semihosting calls if possible, but let's just trace.
break *0x11fd1
continue
# Now we are at entry point.
# Let's search for the "Input flag:" string in memory.
find 0x10000, 0x20000, "Input flag:"
