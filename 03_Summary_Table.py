#! /usr/bin/python3
import sys

# This program uses a function to build a summary table of fields of interest

# Specify user input with usage statement
if len(sys.argv)!=4:
	print ('This program uses a function to build a summary table of fields of interest\nUsage: 03_Summary_Table.py input_file_name input_2_file_name output_file_name\n03_Summary_Table.py BTC_GWAS_Cleaned.tsv HCC_GWAS_Cleaned.tsv Summary_Table.txt')
	sys.exit()
else:
	BTCfileName=sys.argv[1]
	HCCfileName=sys.argv[2]
	OutfileName=sys.argv[3]

# Make a function to count items or unique items if requested
def CountUnique(FileName, field, isunq):
	uniqueList = list()
	ind = 0
	count = 0
	with open(FileName, "r") as Infile:
		for line in Infile:
			Columns = line.strip().split("\t")
			if Columns[0]=="SNPS":
				ind = Columns.index(field)
				continue
			if isunq == True:
				if Columns[ind] not in uniqueList:
					uniqueList.append(Columns[ind])
					count += 1
			else:
				uniqueList.append(Columns[ind])
				count += 1
		out = {
			field: [count, uniqueList]
		}
	return out

# Build a summary table
BTC = list()
HCC = list()

## Total records
BTC.append(CountUnique(BTCfileName, "SNPS", False)["SNPS"][0])
HCC.append(CountUnique(HCCfileName, "SNPS", False)["SNPS"][0])

## Unique SNPs
BTC.append(CountUnique(BTCfileName, "SNPS", True)["SNPS"][0])
HCC.append(CountUnique(HCCfileName, "SNPS", True)["SNPS"][0])

## Unique Publications
BTC.append(CountUnique(BTCfileName, "PUBMEDID", True)["PUBMEDID"][0])
HCC.append(CountUnique(HCCfileName, "PUBMEDID", True)["PUBMEDID"][0])

# Write the summary table to the outfile
Outfile = open(OutfileName, "wt")
Outfile.write("Field\tBTC\tHCC\n")
rownames = [
	"Total association records",
	"Unique SNPs", 
	"Distinct Publications"
]
for i in range(len(rownames)):
	Outstring = rownames[i]+"\t"+str(BTC[i])+"\t"+str(HCC[i])+"\n"
	Outfile.write(Outstring)
Outfile.close()
print("Complete. Check output file.")