import simplefix

"""
Message Header
8	BeginString	Y
FIX.4.4 (Always unencrypted, must be first field in message)

9	BodyLength	Y
(Always unencrypted, must be second field in message)

35	MsgType	Y
(Always unencrypted, must be third field in message)

49	SenderCompID	Y
(Always unencrypted)

56	TargetCompID	Y
(Always unencrypted)"""

"""
D = Order Single <D>

E = Order List <E>

F = Order Cancel Request <F>
"""
def create_tradeId():
    tradeId = ''
    pass

def create_fix_header(order):
    header = simplefix.FixMessage()
    header.append_pair(8, "FIX.4.4")
    header.append_pair(35, order)
    header.append_pair(49, "SENDER")
    header.append_pair(56, "TARGET")
    header.append_pair(34, 4684, header=True)
    header.append_time(52, header=True)
    return header

def create_body(message, symbol, side, ordertype, qty):
    message.append_pair(55, symbol)
    message.append_time(60)
    message.append_pair(54, side)
    message.append_pair(40, ordertype)
    message.append_pair(38, qty)
    return message

def createNewOrderSinge(symbol, side, ordertype, qty):
    order='D'
    header = create_fix_header(order)
    new_order = create_body(header,symbol,side, ordertype, qty)
    new_order_encoded = new_order.encode(new_order)
    return new_order
