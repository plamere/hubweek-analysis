import sys
import os
import time

import simplejson as json
import pyen


en = pyen.Pyen()
en.trace = False


def wait_for_analysis(id):
    while True:
        response = en.get('track/profile', id=id, bucket=['audio_summary'])
        if response['track']['status'] <> 'pending':
            break
        time.sleep(1)
    return response['track']

def is_too_big(path):
    statinfo = os.stat(path)
    return statinfo.st_size > 1024 * 1024 * 10

def perform_analysis(file):
    json_path = file.replace('.wav', '.json')

    if not os.path.exists(json_path):
        if is_too_big(file):
            print 'too big', file
            return

        try:
            print 'analyzing', os.path.basename(file)
            f = open(file, 'rb')
            response = en.post('track/upload', track=f, filetype='wav')
            f.close()
            trid = response['track']['id']
            track = wait_for_analysis(trid)
            out = {
                'trid': trid,
                'path': file,
                'file': os.path.basename(file),
                'summary': track
            }
            print '  writing', json_path
            rfile = open(json_path, 'w')
            print >>rfile, json.dumps(out)
            rfile.close()
        except json.scanner.JSONDecodeError:
            print 'trouble analyzing', file
            print 'skipping'
            print
        except requests.exceptions.ProxyError:
            print 'proxy trouble analyzing', file
            print 'skipping'
            print


    else:
        print 'skipping', os.path.basename(file)
    return


def recurse(path):
    if os.path.isfile(path):
        if path.endswith('.wav'):
            perform_analysis(path)
    elif os.path.isdir(path):
        # print 'recursing', path
        contents = os.listdir(path)
        for file in contents:
            new_path = os.path.join(path, file)
            recurse(new_path)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        recurse(sys.argv[1])
    else:
        print 'usage', 'analyze.py path'
