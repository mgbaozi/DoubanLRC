def FormatLRC(lrc):
	str_list = lrc.split('\n')
	lrc = []
	lrc_strated = False;
	for item in str_list:
		if len(item) > 1 and item[1] >= '0' and item[1] <= '9':
			times = []
			while '[' in item:
				try:
					item = item[item.index('[')+1:]
					s, item = item[:item.index(']')], item[item.index(']')+1:]
					lrc_lables = s.split(':')
					list2 = lrc_lables[-1].split('.')
					hh = int(lrc_lables[-3]) if len(lrc_lables) > 2 else 0
					mm = int(lrc_lables[-2]) if len(lrc_lables) > 1 else 0
					ss = int(list2[0]) if len(list2) else 0
					nn = int(list2[1]) if len(list2) > 1 else 0
				except:
					continue
				time = (((hh * 60 + mm) * 60 + ss) * 100 + nn) * 10
				times.append(time)
			item = item.strip()
			if lrc_strated :
				for time in times :
					lrc.append({'time': time, 'lrc': item})
			lrc_strated |= (item == '')
	return lrc
