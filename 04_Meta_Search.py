#! /usr/bin/python3
import sys

# This program searches for meta information associated with a given SNP in the input files and returns it in the output file

# Specify user input with usage statement
if len(sys.argv)!=5:
	print ('This program searches for meta information associated with a given SNP\nUsage: 04_Meta_Search.py input_file_name input_2_file_name SNP output_file_name\n04_Meta_Search.py BTC_GWAS_Cleaned.tsv HCC_GWAS_Cleaned.tsv rs738408 rs738408_Meta_Table.txt')
	sys.exit()
else:
	BTCfileName=sys.argv[1]
	HCCfileName=sys.argv[2]
	SNPName=sys.argv[3]
	OutfileName=sys.argv[4]

# Define function to find meta information given SNP
def findMeta(FileName, SNP):
	meta = dict()
	with open(FileName, "r") as Infile:
		for line in Infile:
			Columns = line.strip().split("\t")
			if Columns[0]=="SNPS":
				meta["SNPS"]=Columns[1:]
			else:
				if Columns[0]==SNP:
					if SNP not in meta:
						meta[SNP]=list()
					data = Columns[1:]
					meta[SNP].append(data)
	return meta

# Write meta information to outfile
Outfile = open(OutfileName, "wt")
BTC = findMeta(BTCfileName, SNPName)
Outstring = "SNPS"
for m in BTC["SNPS"]:
	Outstring += "\t"+m
Outstring += "\n"
Outfile.write(Outstring)
if SNPName in BTC:
	for i in BTC[SNPName]:
		Outstring = SNPName
		for j in i:
			Outstring += "\t"+j
		Outstring += "\n"
		Outfile.write(Outstring)
HCC = findMeta(HCCfileName, SNPName)
if SNPName in HCC:
	for i in HCC[SNPName]:
		Outstring = SNPName
		for j in i:
			Outstring += "\t"+j
		Outstring += "\n"
		Outfile.write(Outstring)
Outfile.close()

print("Complete. Check output file.")
