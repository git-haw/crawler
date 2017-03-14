from grab import Grab


if __name__ == '__main__':
    g = Grab()
    resp = g.go('http://www.haw358.top/home/')
    print(resp.body)
