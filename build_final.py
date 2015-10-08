import sys
import os
import simplejson as json

all = []

def recurse(path):
    if os.path.isfile(path):
        if path.endswith('.json'):
            f = open(path)
            js = f.read()
            obj = json.loads(js)
            if 'path' in obj:
                obj['s3_key'] = obj['path'].replace('spotify/', '').replace('.mp3', '.wav')
                del obj['path']
                del obj['file']
            else:
                print 'no path in', path

            f.close()
            all.append(obj)
    elif os.path.isdir(path):
        # print 'recursing', path
        contents = os.listdir(path)
        for file in contents:
            new_path = os.path.join(path, file)
            recurse(new_path)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        recurse(sys.argv[1])
        f = open('indaba_analysis.json', 'w')
        print >>f, json.dumps(all, indent=4)
        f.close()
    else:
        print 'usage', 'build_final.py path'
