# UltraRelay

UltraRelay is a tool for LLMNR poisoning and relaying NTLM credentials. It is based on [Responder](https://github.com/SpiderLabs/Responder) and [impack](https://github.com/SecureAuthCorp/impacket).

Especially, this tool can be used to relay credentials from JAVA http request to local SMB server and achieve RCE.

## Dependency

* [Responder](https://github.com/SpiderLabs/Responder)
* [impack](https://github.com/SecureAuthCorp/impacket)

## Ussage

`python ultrarelay.py -ip 192.168.1.100`

Value of the ip argument is attacker's ip address.

## Demo video

https://www.youtube.com/watch?v=VyoyA2GgKck

## Contact

md5_salt [AT] qq.com