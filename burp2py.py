import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputfile', nargs=1, help='Burp request file to parse')
parser.add_argument('-o', '--output', nargs=1, help='Output file name')
args = parser.parse_args()

def read_file(inputfile):
        with open(inputfile, 'r') as f:
                return f.read()

def write_file(outputfile, code):
        with open(outputfile, 'w') as f:
                f.write(code)

def gen_code(url, method, headers, data):
        headers_str = '{\n'
        for k,v in headers.items():
                headers_str += f'\t\t"{k}": "{v}",\n'
        headers_str += '\t}'
        code = f'''import requests

with requests.Session() as s:
\ts.headers = {headers_str}
'''
        if data:
                data_str = '{\n'
                for k,v in data.items():
                        data_str += f'\t\t"{k}": "{v}",\n'
                data_str += '\t}'
                code += f'''
\tdata = {data_str}
\tres = s.{method.lower()}('{url}', data=data)
\tprint(res.status_code)
'''
        else:
                code += f'''
\tres = s.{method.lower()}('{url}')
\tprint(res.status_code)
'''
        return code

def parse_file(burpreq):
        burplines = burpreq.split('\n')
        method = burplines[0].split(' ')[0]
        path = burplines[0].split(' ')[1].strip()
        url = 'https://' + burplines[1].split(':')[1].strip().replace('www.', '') + path
        headers = {}
        i = 0
        while burplines[i] != '':
                for i in range(2, len(burplines)):
                        if ':' in burplines[i]:
                                k = burplines[i].split(': ')[0]
                                v = burplines[i].split(': ')[1].strip()
                                headers[k] = v
        body_split = burplines.index('')
        try:
                body = burplines[body_split+1]
                keyval = body.split('&')
                data = {}
                for kv in keyval:
                        kv = kv.split('=')
                        data[kv[0]] = kv[1]
        except Exception:
                data = False
        return url, method, headers, data

if __name__ == "__main__":
        burpreq = read_file(args.inputfile[0])
        url, method, headers, data = parse_file(burpreq)
        code = gen_code(url, method, headers, data)
        outputfile = args.output[0]
        if outputfile:
                write_file(outputfile, code)
                print(f'Ouput written in {outputfile}')
        else:
                print(code)
        
