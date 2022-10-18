# https://raw.githubusercontent.com/TheAlgorithms/Python/master/data_structures/linked_list/print_reverse.py
class ejYgTyPrgX:
    def __init__(self, KnDxYZOSbI=None):
        self.KnDxYZOSbI = KnDxYZOSbI
        self.nzVJLdIDby = None

    def __repr__(self):
        wRQrlytsaA = []
        ZjZPCbcvdl = self
        while ZjZPCbcvdl:
            wRQrlytsaA.append(f"{ZjZPCbcvdl.KnDxYZOSbI}")
            ZjZPCbcvdl = ZjZPCbcvdl.nzVJLdIDby
        return "->".join(wRQrlytsaA)


def RWbsnrROlw(gNPTzKjGeB: list):
    if not gNPTzKjGeB:
        raise Exception("The Elements List is empty")

    VGeseUoPqS = kVzPkBOPxK = ejYgTyPrgX(gNPTzKjGeB[0])
    for i in range(1, len(gNPTzKjGeB)):
        VGeseUoPqS.nzVJLdIDby = ejYgTyPrgX(gNPTzKjGeB[i])
        VGeseUoPqS = VGeseUoPqS.nzVJLdIDby
    return kVzPkBOPxK


def hJMnxCCpUZ(JfIrPSBxpB: ejYgTyPrgX) -> None:
    if JfIrPSBxpB is not None and isinstance(JfIrPSBxpB, ejYgTyPrgX):
        hJMnxCCpUZ(JfIrPSBxpB.nzVJLdIDby)
        print(JfIrPSBxpB.KnDxYZOSbI)
# # # # # delimiter # # # # # # #
dZdHNxVkYl = RWbsnrROlw([1, 3, 2])
hJMnxCCpUZ(dZdHNxVkYl)
