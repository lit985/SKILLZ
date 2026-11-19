#!/usr/bin/env python3
"""Build vCard 3.0 with embedded photo. Usage:
make_vcard.py "First" "Last" [--phone +1..] [--email a@b.c] [--org X] [--url https://..]"""
import argparse, base64, pathlib
p = argparse.ArgumentParser()
p.add_argument("first"); p.add_argument("last")
p.add_argument("--title", default="AI Engineer")
p.add_argument("--phone"); p.add_argument("--email"); p.add_argument("--org"); p.add_argument("--url")
p.add_argument("--photo", default="headshot-600.jpg")
a = p.parse_args()
here = pathlib.Path(__file__).parent

def fold(line):  # RFC 2426: max 75 octets per line, continuation starts with space
    out = [line[:75]]; rest = line[75:]
    while rest: out.append(" " + rest[:74]); rest = rest[74:]
    return "\r\n".join(out)

L = ["BEGIN:VCARD", "VERSION:3.0",
     f"N:{a.last};{a.first};;;", f"FN:{a.first} {a.last}", f"TITLE:{a.title}"]
if a.org:   L.append(f"ORG:{a.org}")
if a.phone: L.append(f"TEL;TYPE=CELL,VOICE:{a.phone}")
if a.email: L.append(f"EMAIL;TYPE=INTERNET,PREF:{a.email}")
if a.url:   L.append(f"URL:{a.url}")
b64 = base64.b64encode((here / a.photo).read_bytes()).decode()
L.append("PHOTO;ENCODING=b;TYPE=JPEG:" + b64)
L.append("END:VCARD")
out = here / f"{a.first}-{a.last}.vcf".replace(" ", "-")
out.write_bytes(("\r\n".join(fold(l) for l in L) + "\r\n").encode())
print(out, out.stat().st_size, "bytes")
