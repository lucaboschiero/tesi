import editdistance
import itertools

def edit(ref, hyp):

    ref2 = ref.copy()
    hyp2 = hyp.copy()
    hyp2 = hyp2[:len(ref2)]
    hyp2 = [int(elemento) for elemento in hyp2]
    #print(ref2)
    #print(hyp2)
    maxi = max(len(ref2),len(hyp2))

    for i in range(len(ref)-1,-1,-1):
        if (ref2[i] == "" or ref2[i] == 0) and i<len(hyp):
            ref2.pop(i)
            hyp2.pop(i)

    #print("new ref", ref2)
    #print("new hyp", hyp2)
    ed = editdistance.eval(ref2, hyp2)
    #print("Edit distance",ed)

    ed_ratio = ed/maxi
    #print("Edit distance",ed_ratio)
    return ed_ratio

