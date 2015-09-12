import os
filenames = []

drug_is_file = open("Master_File_for_Drugs.txt","a") 
# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("archive cleaned"):
    path = root.split('/')
        
    full_drug_experience = ""
    for file in files:
        cool = "archive cleaned/" + os.path.basename(root) + "/" + file
        with open(cool,"r") as fid:
            file_experience = fid.read().replace('\n', '')
            full_drug_experience += file_experience
            full_drug_experience += " " #add spacing
            
        filenames.append(cool)
    drug_is_file.write(full_drug_experience)
    drug_is_file.write("\n")
drug_is_file.close()
        
doc_is_file = open("Master_File_for_Docs.txt","a") 

for item in filenames:
    with open (item, "r") as fid:
        jack = fid.read().replace('\n', '')
        doc_is_file.write(jack)
        doc_is_file.write("\n")
doc_is_file.close()    #      
    #for file in files:
    #    print len(path)*'---', file