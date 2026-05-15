qemu-system-arm \
    -machine mps2-an385 \
    -cpu cortex-m3 \
    -kernel kernel \
    -monitor none \
    -nographic \
    -serial stdio \
    -semihosting \
    -semihosting-config enable=on,target=native \
    -s -S
