#Appropriate import statements here

drug_names = set(open('drug_names','r').read().splitlines())

#Query cloudant for drug name lists

interaction_matrix = [ for drug_one in drug_names] 
					   for drug_two in drug_names]]

#Visualization code here
