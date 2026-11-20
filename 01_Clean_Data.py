#! /usr/bin/python3
import sys

# This program filters only the fields of interest from the input file into the output file and removes data that was a part of a pan-cancer analysis
# Duplicate SNPs are kept as they could be reported in multiple publications

# Specify user input with usage statement
if len(sys.argv)!=4:
	print('This program filters only the fields of interest in the output file\nUsage: 01_Clean_Data.py input_file_name output_file_name snp_output_name\n01_Clean_Data.py BTC_GWAS.tsv BTC_GWAS_Cleaned.tsv BTC_SNP_List.txt')
	sys.exit()
else:
	InputfileName=sys.argv[1]
	OutfileName=sys.argv[2]
	SNPListName=sys.argv[3]

# Initialize dictionary with the fields of interest as the header
SNPdict: dict={
	"SNPS": ["DISEASE/TRAIT", 
	         "MAPPED_TRAIT", 
	         "P-VALUE", 
			 "CHR_ID", 
			 "CHR_POS", 
			 "REPORTED GENE(S)", 
			 "MAPPED_GENE", 
			 "UPSTREAM_GENE_ID", 
			 "DOWNSTREAM_GENE_ID", 
			 "PUBMEDID"]
}

# Make a dictionary of all SNPs in input file with only fields of interest and progress meter
# Remove associations with "Cancer" as the DISEASE/TRAIT
Pos = {}
LineNumber: int=0
Infile = open(InputfileName, "r")
dt_pos = 0
for i in Infile:
	Columns = i.strip("\n").split("\t")
	if Columns[0]=="DATE ADDED TO CATALOG":
		for s in SNPdict:
			Pos[Columns.index(s)] = []
			for j in SNPdict[s]:
				if j=="DISEASE/TRAIT":
					dt_pos = Columns.index(j)
				Pos[Columns.index(s)].append(Columns.index(j))
	else:
		if Columns[dt_pos].strip() == "Cancer":
			continue
		for p in Pos:
			if Columns[p] not in SNPdict:
				SNPdict[Columns[p]]=[]
			data=[]
			for j in Pos[p]:
				data.append(Columns[j])
			SNPdict[Columns[p]].append(data)
	LineNumber+=1
	if LineNumber%10==0:
		Status=str(LineNumber)+' finished'
		sys.stderr.write(Status+'\r')
Infile.close()

# Sort SNPs while retaining the header
SNPdict = dict(
    list(SNPdict.items())[:1] +
    sorted(list(SNPdict.items())[1:])
)

# Write cleaned SNPs and other arguments to Outfile and list of SNPs with duplicates to SNPList
Outfile = open(OutfileName, "wt")
SNPList = open(SNPListName, "wt")
for s in SNPdict:
	if s == "SNPS":
		Outstring = s
		for j in SNPdict[s]:
			Outstring += "\t"+j
		Outstring += "\n"
		Outfile.write(Outstring)
	else:
		for i in SNPdict[s]:
			Outstring = s
			sout = s+"\n"
			SNPList.write(sout)
			for j in i:
				Outstring += "\t"+j
			Outstring += "\n"
			Outfile.write(Outstring)
Outfile.close()
SNPList.close()

print("Complete. Check output files.")
