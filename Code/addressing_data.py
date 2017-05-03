import json

def address(filename):
	total = []
	with open(filename) as fp:
		raw_data = fp.read()
	items = raw_data.split("\n\n")
	i = 0
	j = 0
	for item in items:
		d = {}
		domains = item.split("\n")
		if len(domains) == 5:
			d["base_information"] = domains[0]
			d["abstract"] = domains[3]
			d["keywords"] = domains[4]
		else:
			print len(domains)
			print i
			j += 1
		total.append(d)
		i += 1
	return total, j

if __name__ == '__main__':
	data_path = "../Data/IR.txt"
	result_path = "../Data/IR_edited.json"

	result, j = address(data_path)
	print j
	with open(result_path, "w") as fp:
		json.dump(result, fp, indent=4)
