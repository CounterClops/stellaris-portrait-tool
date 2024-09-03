# stellaris-portrait-tool
A basic tool I've used to generate basic portrait packs for usage with friends. You still need to do a bit of work to get the config files as you want, but this tool allows me to quickly and easily bulk convert my PNG images to DDS, and then generate the desired portrait config files, with their correct filepath. Just takes a lot of the tediousness out of it.

## Features
- Bulk convert PNG images to DDS
- Bulk generate portrait config files based on created DDS files

## Install
### Requirements
- Python >= 3.10
- [ImageMagick](https://imagemagick.org/)

### Example of using the tool
In the below examples I've made spt available in the path, this can be as simple as putting the SDT folder from this project into the directory you're running the command from.

You can run the tool with something like the below.
```
python spt -s source/ -o output/ --file-conflict replace --generate-configs --config-prefix "example"
```

You can get a list of available options with
```
python sdt --help
```

## Notes for using this tool
This tool assumes that you've organised your original portrait files. The way I'd suggest doing it for this tool is like the below. So you will need to organise your base PNG files, but I feel like this makes basic project management a bit easier anyway.

### Source
```
.
└── gfx
    └── models
        └── portraits
            ├── new_human
                ├── human_pop_00.png
                └── human_ruler_00.png
            ├── tau
                ├── tau_pop_00.png
                ├── tau_pop_01.png
                └── tau_ruler_00.png
            └── orks
                ├── bigga/
                    ├── ork_leader_00.png
                    ├── ork_leader_01.png
                    └── ork_leader_02.png
                ├── ork_pop_00.png
                ├── ork_ruler_00.png
                └── ork_ruler_01.png
```
If you then run the tool with the example given prior under **Example of using the tool** with the above sturcture inside the source/ folder, you'd get the below output
### Output
```
.
└── gfx
    ├── models
        └── portraits
            ├── new_human
                ├── human_pop_00.dds
                └── human_ruler_00.dds
            ├── tau
                ├── tau_pop_00.dds
                ├── tau_pop_01.dds
                └── tau_ruler_00.dds
            └── orks
                ├── bigga/
                    ├── ork_leader_00.dds
                    ├── ork_leader_01.dds
                    └── ork_leader_02.dds
                ├── ork_pop_00.dds
                ├── ork_ruler_00.dds
                └── ork_ruler_01.dds
    └── portraits
        └── portraits
            ├── example_new_human.txt
            ├── example_tau.txt
            ├── example_orks.txt
            └── example_orks_bigga.txt
```