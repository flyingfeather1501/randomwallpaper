# randomwallpaper
```
Usage: randomwallpaper [OPTIONS]

Options:
 -t <time>                Set global wait time (default:1m)
 -d <DIR>                 Set wallpaper directory (default:$(xdg-user-dir PICTURES)/Wallpapers)
 -s                       Change wallpaper immediately before sleeping
 -c <config file>         Use config file to set wait time for individual images
 -w <wallpaper handler>   Set wallpaper handler manually (default:auto)
 -l                       List all wallpaper handlers
 -v                       Print out some debug information
 -h or -?                 Show help (this message)
```

## Config file:
The contents after the last space in a line is passed to sleep.
In the example, sleep 1m will run after setting `more specific file name.png` as the wallpaper.

### Config file example:
```
more specific file name.png 1m
less exact file name 3m
file name 5m
```
