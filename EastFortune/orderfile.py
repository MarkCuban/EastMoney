import json
import sys


def map_to(d):
    if isinstance(d, dict):

        res = {}

        for k, v in d.items():
            if isinstance(v, dict) or isinstance(v, list):
                v = map_to(v)
            elif isinstance(v, unicode):
                v = v.encode('utf-8')
            # c = type(v)
            res[k] = v

    elif isinstance(d, list):

        res = []

        for k in d:
            if isinstance(k, dict) or isinstance(k, list):
                res.append(map_to(k))
            elif isinstance(k, unicode):
                res.append(k.encode('utf-8'))

    return res


def main(input_name, output_name, sortskey):
    with open(input_name, 'rb') as f:

        data = f.readlines()

    # print 'data is ', data
    res = []

    for d in data:
        res.append(json.loads(d))

    x = sorted(res, key=lambda x: x[sortskey])

    with open(output_name, 'wb') as fres:

        for re in x:
            re = map_to(re)
            json.dump(re, fres, ensure_ascii=False)
            fres.write('\n')


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print 'Usage: python input_name output_name key'
        exit()

    main(sys.argv[1], sys.argv[2], sys.argv[3])
