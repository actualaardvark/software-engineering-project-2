# Bishop
## Description
Bishop is the primary backend component of Chessboard. It provides system monitoring as well as hosting for the Pawn frontend.
## Compiling
Bishop is written in the [Crystal](https://crystal-lang.org/) programming language and uses the [Shards](https://crystal-lang.org/reference/latest/man/shards/index.html) package manager to resolve dependencies and compile the software. Bishop also has SQLite as a dependency. After installing `shards`, `crystal`, and `sqlite` from your package manager, you can use the following commands:
### Installing Dependency Shards
```bash
shards install # Only needs to be run once, unless the dependencies are changed.
```
### Compiling for Release
```bash
shards build --release --progress -Dpreview_mt
```
### Running a Development build
```bash
shards run --progress -Dpreview_mt --debug
```
