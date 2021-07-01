# Text to API tool for checkpoint management API
Quick write for generating api comands from text:
```
$ cat example1.txt
group_name_1
1.1.1.1
2.2.2.2
3.3.3.3

group_name_2
1.1.1.4
2.2.2.5
3.3.3.6
$ ./cptext2api.py example1.txt 
add host name group_name_1.1 ip-address 1.1.1.1 ignore-warnings true
add host name group_name_1.2 ip-address 2.2.2.2 ignore-warnings true
add host name group_name_1.3 ip-address 3.3.3.3 ignore-warnings true
add group name group_name_1 members.1 group_name_1.1 members.2 group_name_1.2 members.3 group_name_1.3 ignore-warnings true
```
Code is extensible with input and output plugins.

