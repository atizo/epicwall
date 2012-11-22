# ArtNet Setup

### Run ola daemom
`olad -l 3`

### Find artnet device
`ola_dev_info`

### Patch Artnet Device as Input (e.g. patch device 1, port 0 to a new universe (1) as in/output)
`ola_patch -i -d 1 -p 0 -u 1`

### Check if you receive data for universe 1
`ola_dmxmonitor -u 1`