To install the matplotlib style (`gadfly_dark.mplstyle`)

1. Run `matplotlib.get_configdir()` to find the config directory.
2. `cd` into the directory and make a `stylelib` directory inside it if it does
        not exist.
3. Place the `gadfly_dark.mplstyle` file inside this directory.
4. Use `pyploy.style.use('gadfly_dark')` in your script to select this
    colorscheme.
