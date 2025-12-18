# Placeholder implementations for undefined functions and variables
viewOverlay = "overlay"
viewPSS = "pss"
Response = {viewOverlay: "response_overlay", viewPSS: "response_pss"}
Request = {viewOverlay: "request_overlay", viewPSS: "request_pss"}
IgnoreRequest = {viewOverlay: "ignore_overlay", viewPSS: "ignore_pss"}

def selectPeer(viewType):
    return f"peer_for_{viewType}"

def selectLinks(viewType, peer):
    return [f"link1_{viewType}", f"link2_{viewType}"]

def sendTo(peer, msgType, data=None):
    print(f"Sending to {peer}: {msgType}, {data}")

def recvFromAny(block):
    # Chỉ trả về yêu cầu một lần, sau đó trả về None để thoát
    if block:
        return "some_sender", Request[viewOverlay], ["link1", "link2"]
    return None, None, None

def updateOwnView(viewType, msgData):
    print(f"Updating {viewType} with {msgData}")

def timeToMaintain(viewType):
    return True

def maintainViews():
    peer = {viewOverlay: None, viewPSS: None}

    for viewType in [viewOverlay, viewPSS]:
        peer[viewType] = None
        if timeToMaintain(viewType):
            peer[viewType] = selectPeer(viewType)
            links = selectLinks(viewType, peer[viewType])
            sendTo(peer[viewType], Request[viewType], links)

    # Thêm biến để theo dõi số lần nhận yêu cầu, tránh lặp vô hạn
    request_count = 0
    max_requests = 2  # Giới hạn số lần xử lý yêu cầu

    while True:
        block = (peer[viewOverlay] != None) or (peer[viewPSS] != None)
        sender, msgType, msgData = recvFromAny(block and request_count < max_requests)

        if msgType == None:
            return

        for viewType in [viewOverlay, viewPSS]:
            if msgType == Response[viewType]:
                updateOwnView(viewType, msgData)
            elif msgType == Request[viewType]:
                request_count += 1  # Tăng đếm yêu cầu
                if peer[viewType] == None:
                    links = selectLinks(viewType, sender)
                    sendTo(sender, Response[viewType], links)
                    updateOwnView(viewType, msgData)
                else:
                    sendTo(sender, IgnoreRequest[viewType])
                    # Đặt peer về None để tránh lặp lại
                    peer[viewType] = None
            elif msgType == IgnoreRequest[viewType]:
                peer[viewType] = None

        # Thoát nếu đã xử lý đủ số yêu cầu
        if request_count >= max_requests:
            return

if __name__ == "__main__":
    maintainViews()