import os
import re
import sys
import subprocess
import logging

from urllib.parse import urlparse
from argparse import ArgumentParser
from threading import Thread

# m3u8 can be found 'inspect element->network' tab
LINK_TO_M3U8 = "https://livecloud.akamaized.net/navertv/lip2_kr2/anmss1200/UiOA18Efu6BaFEK2gWhbrh75Z1isVvucV4lBZA4DnM96WrRiL8MF4j6ouvDO_g3k4OWk2r_1sxE0boeN/hdntl=exp=1670089355~acl=*%2fUiOA18Efu6BaFEK2gWhbrh75Z1isVvucV4lBZA4DnM96WrRiL8MF4j6ouvDO_g3k4OWk2r_1sxE0boeN%2f*~data=hdntl~hmac=fac43127ef54248cb0970cc8984fce9d1d3eb8fb17766d241011aaf1f2a4fa35/chunklist_1080.m3u8"

# link to download ts files
HEADER = "https://livecloud.akamaized.net/navertv/lip2_kr2/anmss1200/UiOA18Efu6BaFEK2gWhbrh75Z1isVvucV4lBZA4DnM96WrRiL8MF4j6ouvDO_g3k4OWk2r_1sxE0boeN/hdntl=exp=1670089355~acl=*%2fUiOA18Efu6BaFEK2gWhbrh75Z1isVvucV4lBZA4DnM96WrRiL8MF4j6ouvDO_g3k4OWk2r_1sxE0boeN%2f*~data=hdntl~hmac=fac43127ef54248cb0970cc8984fce9d1d3eb8fb17766d241011aaf1f2a4fa35/"

def prepare_logs() -> None:
    LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
    LOG_LEVEL = logging.DEBUG

    logging.addLevelName(
        logging.CRITICAL,
        '\033[1;31m%s\033[1;0m' % logging.getLevelName(logging.CRITICAL),
    )
    logging.addLevelName(
        logging.ERROR,
        '\033[1;31m%s\033[1;0m' % logging.getLevelName(logging.ERROR),
    )
    logging.addLevelName(
        logging.WARNING,
        '\033[1;33m%s\033[1;0m' % logging.getLevelName(logging.WARNING),
    )
    logging.addLevelName(
        logging.INFO,
        '\033[1;32m%s\033[1;0m' % logging.getLevelName(logging.INFO),
    )
    logging.addLevelName(
        logging.DEBUG,
        '\033[1;35m%s\033[1;0m' % logging.getLevelName(logging.DEBUG),
    )

    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)


class M3U8Downloader():
    def __init__(self,
        m3u8_url: str,
        dirname: str):

        # index to merge m3u8 stream
        self.start = -1
        self.end = -1
        self.current = 0
        self.dirname = dirname
        self.merged_m3u8 = self.dirname + '/merged.m3u8'
        self.m3u8_url = m3u8_url

        # create directory for this downloader
        if not os.path.exists(self.dirname):
            os.mkdir(self.dirname)
            os.mkdir(self.dirname+"/tsfiles")
        else:
            logging.warning(f"{self.dirname} already exist!")

        # init m3u8 file
        if not os.path.exists(self.merged_m3u8):
            # Create new file
            with open(self.merged_m3u8, 'w') as f:
                logging.info("new merged.m3u8 created!")
        else:
            p = re.compile('_([0-9]+).ts')
            with open(self.merged_m3u8, 'r') as f:
                lines = f.readlines()
                self.start = int(p.findall(lines[0])[0])
                self.end = int(p.findall(lines[-1])[0])
                logging.info(f"merged.m3u8 already exist: ({self.start}, {self.end})")

        self.update_m3u8()


    def update_m3u8 (self):
        # download
        result = subprocess.run(["wget", self.m3u8_url, "-P", self.dirname+'/chunklist'], capture_output=True)

        # get filename
        if result.returncode == 0:
            p = re.compile("- .(.*). saved")
            new_m3u8_file = p.findall(result.stderr.decode())
            new_m3u8_file = new_m3u8_file[0]
        else:
            logging.error("Failed to download m3u8 file!")
            sys.exit()

        f = open(new_m3u8_file, "r")
        f2 = open(self.merged_m3u8, "a") # append

        lines = f.readlines()
        p = re.compile('_([0-9]+).ts')

        updated = False
        for line in lines:
            seq_num = p.findall(line)
            if seq_num:
                seq_num = int(seq_num[0])

                if self.start == -1:
                    # this is the first m3u8 file
                    self.start = seq_num

                # update last sequence number
                if self.end < seq_num:
                    line = line.split('?', 1)[0] + "\n"
                    f2.write(line)
                    self.end = seq_num
                    updated = True

        if updated:
            logging.debug(f"{new_m3u8_file} is appended: ({self.start}, {self.end})")

        f.close()
        f2.close()


    def download_next_ts_files (self, batch: int):
        # regex to get filenumber
        p = re.compile('_([0-9]+).ts')

        count = 0
        with open(self.merged_m3u8, "r") as fp:
            for i, line in enumerate(fp):
                if i < self.current-self.start:
                    continue
                else:
                    link = HEADER + line.rstrip()
                    result = subprocess.run(["wget", link, "-O", f"{self.dirname}/tsfiles/video_{self.current:07d}.ts"],
                            capture_output=True)
                    self.current += 1

                    count += 1
                    if count >= batch:
                        break

                logging.debug(f"{line.rstrip()} downloaded")


def main(argv: [str]) -> int:
    parser = ArgumentParser()

    parser.add_argument(
        '--start', '-s',
        type=int,
        help='An integer of the media sequence to continue downloading'
    )

    parser.add_argument(
        '--batch_size', '-b',
        type=int, default=100,
        help='m3u8 would be updated after downloading batch size of ts files'
    )

    parser.add_argument(
        '--project_name', '-n',
        required=True,
        help='directory name'
    )

    args = parser.parse_args()
    prepare_logs()

    downloader = M3U8Downloader(LINK_TO_M3U8, args.project_name)
    if args.start and args.start > downloader.start:
        downloader.current = args.start
    else:
        downloader.current = downloader.start

    # Can be multithread?
    while True:
        # update m3u8
        downloader.update_m3u8()

        # download BATCH number of ts files from args.start
        downloader.download_next_ts_files(args.batch_size)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
