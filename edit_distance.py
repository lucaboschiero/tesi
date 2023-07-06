ref = ["", "Conferma Email", ""]
hyp = ["Registrazione", "Conferma Email", "Autenticazione", "Acquisto"]

indexes= [] #This vector contains the indexes of the elements that match

# Search in the two sequences the common elements
for i in range(min(len(ref), len(hyp))) : 
    if ref[i] == hyp[i] : 
        indexes.append(i)

# Find the indices of empty string elements in ref and hyp
ref_empty_indices = [i for i, element in enumerate(ref) if element == ""]
indexes.extend(ref_empty_indices)

# Print the length of ref_empty_indices
removed_element = len(ref_empty_indices)
print("Removed element in both sequences: ", removed_element)

# Print the matches obtained with the length of the vector indexes
matches = len(indexes)
print("Matches: ", matches)

ratio = (2 * matches) / (len(hyp) + len(ref))
print("Similarity Ratio: ", ratio) 
#print("Distance: ", len(ref) + removed_element - matches)
print(indexes)