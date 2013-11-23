import os
import sys
import re
import urllib2
import urlparse
import string
import time

path = "M:\99/"

sys.argv = [sys.argv[0], 'http://www.seemore.co.kr/']
tocrawl = [sys.argv[1]]
crawled = []

linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
mapping = file("mapping.txt", "w")

count = 0
num_pages = 0

new_dir = path + "\data"
os.mkdir(new_dir,0755);
t0 = time.clock()
def getPageContents(link):
	global mapping
	global count
	global num_pages
	try:
		write1 = 1
		write2 = 1
		write3 = 1
		write4 = 1
		
		div = 0
		title = 0
		f = urllib2.urlopen(link)
		
		for line in f:
			if title == 0: 
				if "<title" in line:
					n_line = re.search(r'<[^<>]*>([^<>]*)<[^<>]*>', line)
					count = count + len(n_line.group(1))
					file_name = path+"\\data\\" + str(count) + ".txt"
					mapping.write(file_name)
					mapping.write('\t')
					mapping.write(link)
					mapping.write("\n")
					outfile = file(file_name, "w")
					num_pages += 1
					title = 1

			if "<script" in line:
				write1 = 0
			if "<SCRIPT" in line:
				write1 = 0
			if "<style" in line:
				write2 = 0
			if "<STYLE" in line:
				write2 = 0
			if "<div" in line:
				write3 = 0
			if "<DIV" in line:
				write3 = 0
			if "<rdf" in line:
				write4 = 0
			if "<RDF" in line:
				write4 = 0
			if write1 == 1 and write2 == 1:
				if write4 == 1 :
					n_line = re.sub(r'<[^>]*>', r'', line)
					n_line = re.sub(r'<[^>]*', r'', n_line)
					n_line = re.sub(r'[^>]*>', r'', n_line)
					n_line = n_line.strip()
					count =  count + len(n_line)
					if len(n_line) > 1:
						outfile.write(n_line)
						outfile.write('\n')
				
			if "</script" in line:
				write1 = 1
			if "</SCRIPT" in line:
				write1 = 1
			if "</style" in line:
				write2 = 1
			if "</STYLE" in line:
				write2 = 1
			if "</div" in line:
				write3 = 1
			if "</DIV" in line:
				write3 = 1
			if "</rdf" in line:
				write4 = 1
			if "</RDF" in line:
				write4 = 1
		outfile.close()
	except:
		print "error"
		return


				
for crawling in tocrawl:
	
	if count > 999999999999900000:
		break

	print count, crawling
	
	url = urlparse.urlparse(crawling)
	getPageContents(crawling)
	
	try:
		response = urllib2.urlopen(crawling)
	except:
		continue
	msg = response.read()
	links = linkregex.findall(msg)
	crawled.append(crawling)
	for link in (links.pop(0) for _ in xrange(len(links))):
		if link.startswith('/'):
			link = 'http://' + url[1] + link
		elif link.startswith('#'):
			link = 'http://' + url[1] + url[2] + link
		elif not link.startswith('http'):
			link = 'http://' + url[1] + '/' + link
		if (link not in crawled)and(link not in tocrawl):
			link_s = link[:-1]
			if (link_s not in crawled) and (link_s not in tocrawl):
				tocrawl.append(link)
	
	
mapping.close()
t = time.clock() - t0
print "TIME: ", t
print "END"
