LINK_FILE=links
FROM=1

tail -n +$FROM ${LINK_FILE} | while read line
do
	wget -O ./tsfiles/video_$FROM.ts $line
	let FROM+=1
done
