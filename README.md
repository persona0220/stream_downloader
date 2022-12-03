Scripts to download live streaming videos
=========================================

1. Open `stream_downloader.py` and put the `LINK_TO_M3U8` and `HEADER` url of
   a video you want to download.
   You can get the m3u8 file through _inspect element_ of a webpage.

2. Run `stream_downloader`.
```
	$ python3 stream_downloader.py -n VIDEO_NAME_TO_SAVE
```

Options
-------

- When you want to pause download and resume downloading from the last video sequence,
give a sequence id `--start`
```
	$ python3 stream_downloader.py -n MOVIE --start 300
```
- m3u8 file would be updated after downloading `--batch_size` of ts files
```
	$ python3 stream_downloader.py -n MOVIE --batch_size 100
```


Manual
======
Following is a code block to download m3u8 video manually step-by-step.

1. Download `m3u8` file.
You can get the m3u8 file through _inspect element_ on webpage.
Some platform doesn't use m3u8 but just use raw link for ts, then you can skip
this step.
```
$ wget [URL.m3u8]
```

2. Run `make_link.py` to generate links. It will generate `links` file.
Use `make_link.py` when you know the link address for ts files. If the link is
stored within m3u8 file, you can use `make_link_from_m3u8.py`.

```
$ python3 make_link.py
```

3. Run `script.sh` to downlaod `ts` files. You may want to specify `FROM` value
   to resume download from the last file you already get.
```
$ ./script.sh
```

4. Under `tsfiles` directory, run `rename.sh` to rename ts files.
```
$ cd tsfiles
$ ./rename.sh
```

5. Merge ts files into one large output.
```
$ cat *.ts > result_output.mkv
```
