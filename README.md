# WhatDo
My what to do app


## Compilation:

Setup build directory:

```sh
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS=1 ..
```

Secondary release build:
```sh
mkdir build-release
cd build-release
cmake -DCMAKE_BUILD_TYPE=Release ..
```

Compile:

```sh
make
```
