
small util to do some cpu temperature testing

# Requirements

```shell
apt install coreutils grep stress-ng tmux lm-sensors s-tui
```
# Run

At the end, a small graph will be printed

```shell
$ ./run-stress.sh 
performance
[exited]
 55.0°:   (5)                                                                                                        
 56.0°:   (0)                                                                                                        
 57.0°:   (0)                                                                                                        
 58.0°:   (0)                                                                                                        
 59.0°:   (0)                                                                                                        
 60.0°:   (5)                                                                                                        
 61.0°:   (5)                                                                                                        
 62.0°:   (5)                                                                                                        
 63.0°:   (5)                                                                                                        
 64.0°:   (5)                                                                                                        
 65.0°:  (10) █                                                                                                      
 66.0°:  (10) █                                                                                                      
 67.0°:  (20) ██                                                                                                     
 68.0°: (260) ████████████████████████████                                                                           
 69.0°: (934) ███████████████████████████████████████████████████████████████████████████████████████████████████████
 70.0°: (115) ████████████
```


