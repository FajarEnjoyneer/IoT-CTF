
target remote :1234
set architecture arm
break *0x13234
continue
# After reaching the breakpoint, dump the transformation result
x/32bx $sp+8
# And the target
x/32bx $r0
detach
quit
