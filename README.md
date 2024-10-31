# 2024 Team SH20 Project

## Members

- 2840506 Heng Zhen Yao test push
- 2671747 Dulmant Jan
- 2777042 Levack Fraser Wiremu I am Fraser Levack <h4> 🦈 </h4>
- 2802089 Tee Zhi Xi "Hello World!"
- 2618972 McIntyre Aaron "Hello World"
- 2768903 Nelson Freddie hello universe

## Requirements

- python 3.12
- django 5.1.2

## Contributing

Commit messages should follow the guidelines described [here](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)

Once you have cloned the repository, you can run the `setup.ps1` script setup python and it's dependencies, as well as pre-commit hooks.

```powershell
.\scripts\setup.ps1
```

The python virtual environment will be created in `C:\Users\Public\sh20-main-venv`, it will be automatically activated by the setup script. However you can also activate it using:

```powershell
.\scripts\activate-venv.ps1
```

And deactivate it using:

```powershell
deactivate
```

All code is ran through the black formatter, and the flake8 linter by the pre-commit hooks. The pre-commit hooks will run these checks before allowing you to commit. You may also run these tools from the command line using:

```powershell
black .
```

```powershell
flake8 .
```

You are now ready to start developing!
