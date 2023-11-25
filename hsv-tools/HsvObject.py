import json
import numpy as np


class HsvObject:
    def __init__(self, filename = 'hsvo.json'):
        self.filename = filename
        self.hsv = np.array([[[0, 0, 0]]])
        print(self.hsv)
        self.hsvL = (np.array([[0, 0, 0]]), 0, 0)
        self.hsvU = (np.array([[0, 0, 0]]), 0, 0)
        self.points = []
        self.hsv_points = []

    def save_Object(self):
        out = {
            'hsv'       : {
                'h': int(self.hsv[0][0][0]),
                's': int(self.hsv[0][0][1]),
                'v': int(self.hsv[0][0][2])
            },
            'hsvL'      : {
                'h': int(self.hsvL[0][0][0]),
                's': int(self.hsvL[0][0][1]),
                'v': int(self.hsvL[0][0][2]),
                'f': self.hsvL[1],
                'd': self.hsvL[2]
            },
            'hsvU'      : {
                'h': int(self.hsvU[0][0][0]),
                's': int(self.hsvU[0][0][1]),
                'v': int(self.hsvU[0][0][2]),
                'f': self.hsvU[1],
                'd': self.hsvU[2]
            },
            'points'    : self.points,
            'hsv_points': [{ 'h': int(p[0][0][0]), 's': int(p[0][0][1]), 'v': int(p[0][0][2]) } for p in
                           self.hsv_points]
        }
        encoded = json.JSONEncoder().encode(out)
        with open(self.filename, 'w') as f:
            f.write(encoded)

    # convertir L a diccionario, para guardarlo como json

    def load_limit_points(self):
        with open(self.filename) as f:
            points = json.loads(f.read())
        return points

    def hsvLimits(self, hsv):
        lower = (hsv[0] - 10, 100, 100)
        upper = (hsv[0] + 10, 255, 255)
        return lower, upper


def load_object(filename = 'hsvo.json'):
    hsvObject = HsvObject(filename)
    with open(filename) as f:
        points = f.read()
        result = json.JSONDecoder().decode(points)
        hsvObject.hsv = np.array([[[result['hsv']['h'], result['hsv']['s'], result['hsv']['v']]]])
        hsvObject.hsvL = (np.array([[result['hsvL']['h'], result['hsvL']['s'], result['hsvL']['v']]]), result['hsvL']['f'], result['hsvL']['d'])
        hsvObject.hsvU = (np.array([[result['hsvU']['h'], result['hsvU']['s'], result['hsvU']['v']]]), result['hsvU']['f'], result['hsvU']['d'])
        hsvObject.points = result['points']
        hsvObject.hsv_points = np.array([[[p['h'], p['s'], p['v']]] for p in result['hsv_points']])
        print(hsvObject.hsv)
    return hsvObject


if __name__ == '__main__':
    hsvo = HsvObject()
    hsvo.save_Object()
    load_object()
    # print( h, l , u)
