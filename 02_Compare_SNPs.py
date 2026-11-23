#! /usr/bin/python3
import sys

# This program allows exploratory comparison between two GWAS association tables, cleaned or not
# Multiple options based on what the user is interested in
# Modified to allow multiple entries of an SNP to be counted

# Specify user input with usage statement
if len(sys.argv)!=5 or int(sys.argv[3]) not in range(0,5):
	print ('This program facilitates exploratory comparison between two GWAS association tables\nUsage: 02_Compare_SNPs.py ID_list_1 ID_list_2 Choice(0-4) output_file\nChoices:\n\t(0) Summary Table\n\t(1) Find the union\n\t(2) Find the intersection\n\t(3) Find ids unique to list 1\n\t(4) Find ids unique to list 2\n02_Compare_SNPs.py BTC_SNP_List.txt HCC_SNP_List.txt 0 BTC_HCC_summary.txt\n')
	sys.exit()
else:
	IDList1Name=sys.argv[1]
	IDList2Name=sys.argv[2]
	Choice=sys.argv[3]
	OutfileName=sys.argv[4]

# Make a dictionary of all IDs in the format AllIDs{ID:[In List1, In List2]}
AllIDs={}
IDList1=open(IDList1Name, "r")
for i in IDList1:
	i=i.strip()
	if i not in AllIDs:
		AllIDs[i]=[1,0]
	else:
		AllIDs[i][0]+=1
IDList1.close()
IDList2=open(IDList2Name, "r")
for i in IDList2:
	i=i.strip()
	if i not in AllIDs:
		AllIDs[i]=[0,1]
	else:
		AllIDs[i][1]+=1
IDList2.close()

# Output summary of occurances
if Choice == "0":
	Outfile=open(OutfileName, "wt")
	Header: str="SNP\tBTC\tHCC\n"
	Outfile.write(Header)
	for k in AllIDs:
		Outstring: str=k+"\t"+str(AllIDs[k][0])+"\t"+str(AllIDs[k][1])+"\n"
		Outfile.write(Outstring)
	Outfile.close()
	print("Complete. Check output file.")

# Choice 1: Union
elif Choice == "1":
	Outfile=open(OutfileName, "wt")
	for k in AllIDs:
		Outstring: str=k+"\n"
		Outfile.write(Outstring)
	Outfile.close()
	print("Complete. Check output file.")

# Choice 2: Intersection
elif Choice == "2":
	Outfile=open(OutfileName, "wt")
	for k in AllIDs:
		if AllIDs[k][0]>=1 and AllIDs[k][1]>=1:
			Outstring: str=k+"\n"
			Outfile.write(Outstring)
	Outfile.close()
	print("Complete. Check output file.")

# Choice 3: IDs unique to list 1
elif Choice == "3":
	Outfile=open(OutfileName, "wt")
	for k in AllIDs:
		if AllIDs[k][0]>=1 and  AllIDs[k][1]==0:
			Outstring: str=k+"\n"
			Outfile.write(Outstring)
	Outfile.close()
	print("Complete. Check output file.")

# Choice 4: IDs unique to list 2
else:
	Outfile=open(OutfileName, "wt")
	for k in AllIDs:
		if AllIDs[k][0]==0 and  AllIDs[k][1]>=1:
			Outstring: str=k+"\n"
			Outfile.write(Outstring)
	Outfile.close()
	print("Complete. Check output file.")