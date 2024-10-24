# **Data Generator Scripts for RoboCall**

## *Download Data*

### *Help*: Shows help menu and exit.

```
python data_download.py -h
```

### *Download All Data*: Download both RoboCall and Legitimate Human Call `AUDIO` data.
*( Need Username and Password for downloading Legitimate Human Call `AUDIO` data. [Click Here](https://ca.talkbank.org/access/CallHome/eng.html) for Registration. )*

```
python data_download.py -f ALL -o <output_dir_path>
```

### *Download Legit Human Call Data*: Downloads Legit Human Call Audio Data Only and exit.

```
python data_download.py -f HUMAN -o <output_dir_path>
```

### *Download RoboCall Data*: Downloads RoboCall Audio Data and exit.

```
python data_download.py -f ROBO -o <output_dir_path>
```


## *Generate Spectrograms*

> For `Linux` based environment

```
ulimit -n 4096
```
