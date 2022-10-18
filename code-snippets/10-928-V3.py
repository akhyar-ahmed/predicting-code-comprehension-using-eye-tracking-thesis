# https://raw.githubusercontent.com/TheAlgorithms/Python/master/sorts/pigeon_sort.py
def UpOPlfoWUX(OFKXNxbmYH: list[int]) -> list[int]:
    if len(OFKXNxbmYH) == 0:
        return OFKXNxbmYH

    KROgWBCZqM, inPrrsZLDn = min(OFKXNxbmYH), max(OFKXNxbmYH)

    pQQFYYeuoH = inPrrsZLDn - KROgWBCZqM + 1
    iXKqVaJWdI, AlaxlYoSMM = [0] * pQQFYYeuoH, [0] * pQQFYYeuoH

    for XBiaNdSkpk in OFKXNxbmYH:
        MJjTOegEgj = XBiaNdSkpk - KROgWBCZqM
        iXKqVaJWdI[MJjTOegEgj] = XBiaNdSkpk
        AlaxlYoSMM[MJjTOegEgj] += 1

    MJjTOegEgj = 0
    for XBiaNdSkpk in range(pQQFYYeuoH):
        while AlaxlYoSMM[XBiaNdSkpk] > 0:
            OFKXNxbmYH[MJjTOegEgj] = iXKqVaJWdI[XBiaNdSkpk]
            MJjTOegEgj += 1
            AlaxlYoSMM[XBiaNdSkpk] -= 1

    return OFKXNxbmYH
# # # # # delimiter # # # # # # #
print(UpOPlfoWUX([0, 7, 4, 1, 1]))