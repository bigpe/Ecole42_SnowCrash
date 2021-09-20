## SnowCrash

Find exploits in OS

[Download image](https://projects.intra.42.fr/uploads/document/document/2944/SnowCrash.iso) (Ubuntu Linux)

[More information about project in subject file.](https://cdn.intra.42.fr/pdf/pdf/19578/en.subject.pdf)

### Prepare

Break process is automated, at first obtain dependencies

You need CLI:
- Wireshark
- JohnTheRipper

For MacOS (Install deps from brew and python deps by pip3):

```shell
./install
```

CLI deps standalone:

**Use a package manager for your system** 

Python deps standalone:

```shell
pip3 install -r requirements.txt
```

### Usage

- Edit utils/config.py and specify VM host and port

You can delete all flag files for the purity of the experiment flags will be writen after level successfully broken
```shell
./remove_flags
```

You can run break process for all levels together, step by step

```shell
./break_all
```

Or run one by one, e.g.
```shell
cd level12/Ressources && python3 break.py
```
