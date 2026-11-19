#! /usr/bin/python3
import sys

# Specify user input with usage statement
if len(sys.argv)!=3:
	print ('Usage: 01_Clean_Data.py input_file_name output_file_name\n01_Clean_Data.py BTC_GWAS.tsv BTC_GWAS_Cleaned.tsv')
	sys.exit()
else:
	InputfileName=sys.argv[1]
	OutfileName=sys.argv[2]

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
Pos = {}
LineNumber: int=0
Infile = open(InputfileName, "r")
for i in Infile:
	Columns = i.strip("\n").split("\t")
	if Columns[0]=="DATE ADDED TO CATALOG":
		for s in SNPdict:
			Pos[Columns.index(s)] = []
			for j in SNPdict[s]:
				Pos[Columns.index(s)].append(Columns.index(j))
	else:
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

# Write cleaned SNPs to Outfile
Outfile = open(OutfileName, "wt")
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
			for j in i:
				Outstring += "\t"+j
			Outstring += "\n"
			Outfile.write(Outstring)
Outfile.close()

print("Complete. Check output file.")
