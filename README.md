# RyzenAdj Presets

[RyzenAdj](https://github.com/FlyGoat/RyzenAdj) is a great tool for tuning AMD Ryzen Mobile processors, but it does not come with the ability to manage presets. This tool fixes it.

Presets can be defined in the `presets/` folder as `.txt` files. Note that each file can only contain a single-line command.

```plain
Usage:
  ryzenadj-preset  # prints the current preset
  ryzenadj-preset current  # prints the current preset name in raw
  ryzenadj-preset switch <mode>  # switch to another mode
  ryzenadj-preset reapply  # reapply current mode
```

This is meant to be added to `PATH` and invoked through other automation means.
