import editdistance
import itertools

def edit(ref, hyp):

    ref2 = ref.copy()
    hyp2 = hyp.copy()

    #maxi = max(len(ref2),len(hyp2))

    for i in range(len(ref)-1,-1,-1):
        if ref2[i] == "" or ref2[i] == 0:
            ref2.pop(i)
            hyp2.pop(i)

    #print("new ref", ref2)
    #print("new hyp", hyp2)
    ed = editdistance.eval(ref2, hyp2)
    #print("Edit distance",ed)

    return ed
    #ed_ratio = ed/maxi
    #print("Edit distance ratio", ed_ratio)
    #ed_simil = 1 - ed_ratio
    #print("Similarity ratio", ed_simil)

