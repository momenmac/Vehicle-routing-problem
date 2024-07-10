class DeliveryPoint:
    def __init__(self, x, y, demand):
        self.x = x
        self.y = y
        self.demand = demand

    def __repr__(self):
        return f"DeliveryPoint(x={self.x}, y={self.y}, demand={self.demand})"
