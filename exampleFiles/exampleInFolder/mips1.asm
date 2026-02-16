
.data

msg: .asciiz "Hello World!"

.text

li $v0, 4            # service 4 is print string
la $a0, msg  	     # pseudo-instruction to load the address of the label g
syscall
