import urllib
import urllib2
from bs4 import BeautifulSoup
from diseasome.src import diseasome

def main():
    #download_malacards_data()
    #get_malacards_data()
    output_disease_genes()
    return

def download_malacards_data():
    url = 'http://www.genecards.org/cgi-bin/listdiseasecards.pl'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'type' : 'full',
		'no_limit' : '1' }
    headers = { 'User-Agent' : user_agent }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    html_doc = response.read()
    f = open("../../data/genecards/download.html", 'w')
    f.write(html_doc)
    f.close()
    return

def get_malacards_data():
    html_doc = open("../../data/genecards/download.html") #.read()
    soup = BeautifulSoup(html_doc, "xml")
    gene_to_diseases = {}
    disease_to_genes = {}
    for tag in soup.find_all('td', class_="geneSymbol"):
	gene = tag.a.string.encode()
	#print gene
	tag_count = 0
	#print "==td==", gene
	for tag_td in tag.next_siblings:
	    #print tag_td.string
	    if str(tag_td.string).strip() == "":
		continue
	    tag_count += 1
	    #print tag_td, tag_count
	    for tag_a in tag_td.find_all("a", class_=""):
		if tag_count == 3:
		    try:
		    	disease = tag_a.string.replace(u'\xa0', u' ').encode()
		    except:
		    	print tag_a.string
		    #disease = tag_a.string.encode("ascii","ignore")
		    disease = disease.replace('"', '').rstrip(",").lower()
		    score = tag_a.attrs["title"]
		    idx = score.find(":")
		    score = float(score[idx+1:])
		    if score > 1.0:
			#print gene, disease, score
			gene_to_diseases.setdefault(gene, []).append(disease)
			disease_to_genes.setdefault(disease, []).append(gene)
    #print len(gene_to_diseases)
    #print gene_to_diseases["AADAC"]
    return disease_to_genes, gene_to_diseases

def output_disease_genes():
    geneid_to_names, name_to_geneid = diseasome.get_geneid_symbol_mapping()
    disease_to_genes, gene_to_diseases = get_malacards_data()
    f = open("../../data/genecards/disease_to_genes.tsv", 'w')
    count = 0
    #all_geneids = set()
    for disease, genes in disease_to_genes.iteritems():
	#if disease.lower().find("diabetes") != -1:
	#    all_geneids |= set(geneids)
	geneids = [ name_to_geneid[gene] for gene in genes if gene in name_to_geneid ]
	if len(geneids) > 5:
	    count += 1
	f.write("\t%s\t%s\n" % (disease, "\t".join(geneids)))
    f.close()
    print count
    #print all_geneids
    return

if __name__ == "__main__":
    main()

