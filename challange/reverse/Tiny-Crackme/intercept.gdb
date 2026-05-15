target remote :1234
set architecture arm
break *0x13234
continue
# After reaching the breakpoint, print the memory at sp+8
x/32bx $sp+8
# Also print the target at r0
x/32bx $r0
