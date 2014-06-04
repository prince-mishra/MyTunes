import json
import sys
import re
import codecs

if __name__=="__main__":
	inputfile = sys.argv[1]
	f = open(inputfile, 'r')
	f_json = json.loads(f.read())
	f.close()
	parsed_content= []
	all_ids = []
	first_vid = ''
	playlistjs = ''
	playlistnames = ''
	playlistdescription = ''
	platliststr = ''
	i = 0
	for item in f_json['data']:
		link = item.get('link')
		if link and link.find('https://www.youtube.com/watch?v=') != -1:
			video_id = link.split('?v=')[1][:11]
			video_name = re.escape(item.get('name', ''))
			video_description = re.escape(item.get('description', ''))
			all_ids.append(video_id)

			curjs = "'" + video_id + "',"
			playlistjs += curjs
			curname = "'" + video_name + "',"
			playlistnames += curname
			curdesc = "'" + video_description + "',"
			playlistdescription += curdesc
			item_dict = {'video_id' : video_id, 'video_name' : video_name, 
				'video_description' : video_description}
			parsed_content.append(item_dict)
	if all_ids:
		firstvideo = all_ids[0]
	playlistjs = 'var playlist = [' + playlistjs.strip(',') + '], playlistnames=[' + playlistnames.strip(',') + '], playlistdescription=[' + playlistdescription.strip(',') + '];'
	playliststr = "'" + ','.join(all_ids[1:]) + "'"

	print firstvideo
	#print playlistjs
	print playliststr
	
	
	template_file = codecs.open('../index2.html', 'r', 'utf-8')
	template_data = template_file.read()#.encode("ascii", "ignore")
	template_file.close()
	html = template_data.replace('playlistjs', playlistjs).replace('playliststr', playliststr).replace('firstvideo', firstvideo)
	f = codecs.open('../output.html', 'w', 'utf-8')
	f.write(html)
	f.close()
	


