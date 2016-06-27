import sys
import requests

def get_category(query, idx=0):
    db = "mesh"
    stem_url = r"http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    mesh_db = stem_url + "esearch.fcgi?db=%s&term=%s&retmode=json"
    record_db = stem_url + "esummary.fcgi?db=%s&id=%s&retmode=json"
    record_list = requests.get(mesh_db % (db, query)).json()
    try:
        mesh_id = record_list['esearchresult']['idlist'][idx]
    except KeyError:
        print record_list
    record_data = requests.get(record_db % (db, mesh_id)).json()
    treenum = record_data['result'][mesh_id]['ds_idxlinks'][idx]['treenum']
    meshterm = record_data['result'][mesh_id]['ds_meshterms'][idx]
    return treenum

def main(outfile, index_file):
	with open(outfile, "r") as of, open(index_file, "w") as xf:
		for line in of:
			if line.isspace():
				continue
			elif line.startswith('#'):
				print("Processing file " + line.lstrip("#"))
				xf.write(line)
				xf.write("\n")
			else:
				term = line.split("|")[1].lstrip("*")
				try:
					xf.write("|".join((term, get_category(term))))
				except IndexError:
					print(term)
				xf.write("\n")


if __name__ == "__main__":
	outfile = sys.argv[1]
	lead, tail = outfile.rsplit(".", 1)
	index_file = lead + "_indexed." + tail
	main(outfile, index_file)
	sys.exit(0)