#!/usr/bin/env python

class Link:
    def __init__(self, incomingId: str, outgoingId: str, viaLaneId: str) -> None:
        self.incomingId = incomingId
        self.outgoingId = outgoingId
        self.viaLaneId = viaLaneId

    def __repr__(self):
        return ("Link(incomingId='%s', outgoingId=%s, viaLaneId=%s)" %
                (self.incomingId, self.outgoingId, self.viaLaneId))
