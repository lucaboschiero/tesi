import editdistance
import itertools

def edit(ref, hyp):

    ref2 = ref.copy()
    hyp2 = hyp.copy()
    negative_values = []
    negative_indexes =[]

    for i in range(len(ref2)):
        if isinstance(ref2[i], list):
            negative_values.append(ref2[i])
            num_elements = len(ref2[i])
            # Estendi la lista negative_indexes con gli indici duplicati
            negative_indexes.extend([i] * num_elements)
            ref2[i] = ''
    
    negative_values = list(itertools.chain.from_iterable(negative_values))

    maxi = max(len(ref2),len(hyp2))

    for i in range(len(ref)-1,-1,-1):
        if ref2[i] == "":
            ref2.pop(i)
            hyp2.pop(i)

    print("new ref", ref2)
    print("new hyp", hyp2)
    ed = editdistance.eval(ref2, hyp2)
    print("Edit distance",ed)

    for i in range(len(negative_values)):
        value = abs(negative_values[i])
        index = negative_indexes[i]
        # Utilizza value e index all'interno del tuo ciclo
        print("Index: ", index, "value: ", value, "hyp[", index, "]: ", hyp[index])
        if(hyp[index] == value):
            ed = ed + 1

    print("Edit distance",ed)
    ed_ratio = ed/maxi
    #print("Edit distance ratio", ed_ratio)
    ed_simil = 1 - ed_ratio
    #print("Similarity ratio", ed_simil)

