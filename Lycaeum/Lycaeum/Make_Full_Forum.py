import os

drug_names = open('deduplicated-curated-drug-names','r').read().splitlines()

multi_references = open('Two_or_more_drug_references','w') 
# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("forums"):
    path = root.split('/')
    for file in files:            
        substance_mentioned = []
        cool = "forums/" + os.path.basename(root) + "/" + file
        with open(cool,"r") as fid:
            #print file_experience
            file_experience = fid.read().replace('\n', '')
        for word in file_experience.split():
            if word in drug_names :
                if word not in substance_mentioned:
                    substance_mentioned.append(word)
        if len(substance_mentioned) > 1:
            multi_references.write(file_experience + '\n')
            
